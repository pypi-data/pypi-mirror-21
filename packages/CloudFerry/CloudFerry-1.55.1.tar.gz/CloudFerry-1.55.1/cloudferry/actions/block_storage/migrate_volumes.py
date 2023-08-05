# Copyright 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import logging

from cinderclient import exceptions as cinder_exceptions
from cinderclient.v1 import volumes as volumes_v1
from cinderclient.v2 import volumes as volumes_v2

from cloudferry.lib.base import exception
from cloudferry.lib.base.action import action
from cloudferry.lib.copy_engines import base as copy_engines_base
from cloudferry.lib.migration import notifiers
from cloudferry.lib.migration import objects
from cloudferry.lib.os.identity import keystone
from cloudferry.lib.os.storage import cinder_db
from cloudferry.lib.os.storage import plugins
from cloudferry.lib.os.storage.plugins import copy_mechanisms
from cloudferry.lib.os.storage.plugins.nfs import generic
from cloudferry.lib.utils import files
from cloudferry.lib.utils import mysql_connector
from cloudferry.lib.utils import remote_runner
from cloudferry.lib.utils import retrying
from cloudferry.lib.utils import utils

LOG = logging.getLogger(__name__)


def _vol_name(vol_id, vol_name):
    return "{name} ({uuid})".format(
        uuid=vol_id,
        name=vol_name or "<no name>")


def vol_name_from_dict(volume_dict):
    return _vol_name(volume_dict['id'], volume_dict['display_name'])


def vol_name_from_obj(volume_object):
    return _vol_name(volume_object.id, volume_object.display_name)


def volume_name(volume):
    if isinstance(volume, dict):
        return vol_name_from_dict(volume)
    elif isinstance(volume, (volumes_v1.Volume, volumes_v2.Volume)):
        return vol_name_from_obj(volume)


class VolumeMigrationView(object):
    def __init__(self, volumes):
        self.volumes = volumes
        self.num_volumes = len(self.volumes)
        self.total_size = sum((v['size'] for v in self.volumes))
        self.size_migrated = 0

    def initial_message(self):
        LOG.info("Starting migration of %s volumes of total %sGB",
                 self.num_volumes, self.total_size)

    def before_migration(self, i, v):
        n = i + 1
        progress = ""

        # avoid division by zero
        if self.num_volumes:
            percentage = float(i) / self.num_volumes
            progress = "{n} of {total}, {percentage:.1%}".format(
                n=n, total=self.num_volumes, percentage=percentage)

        LOG.info("Starting migration of volume '%(name)s' of "
                 "size %(size)dGB, %(progress)s",
                 {'name': volume_name(v),
                  'size': v['size'],
                  'progress': progress})

    def after_migration(self, i, v):
        n = i + 1
        progress = ""
        size_progress = ""

        # avoid division by zero
        if self.num_volumes:
            percentage = float(n) / self.num_volumes
            progress = "{n} of {total}, {percentage:.1%}".format(
                n=n, total=self.num_volumes, percentage=percentage)

        if self.total_size:
            self.size_migrated += v['size']
            size_percentage = float(self.size_migrated) / self.total_size
            size_progress = "{n}GB of {total}GB, {percentage:.1%}".format(
                n=self.size_migrated,
                total=self.total_size,
                percentage=size_percentage)

        LOG.info("Finished migration of volume '%s'", volume_name(v))
        LOG.info("Volume migration status: %(progress)s",
                 {'progress': '; '.join([progress, size_progress])})


class MigrateVolumes(action.Action):
    """Copies cinder volumes from source to destination cloud sequentially

    All migrated volumes have 'src_volume_id' metadata field which allows
    identifying volumes migrated previously.

    Depends on:
     - `get_volumes_from_source` task
    """

    def __init__(self, init):
        super(MigrateVolumes, self).__init__(init)
        self.src_cinder_backend = plugins.get_cinder_backend(self.src_cloud)
        self.dst_cinder_backend = plugins.get_cinder_backend(self.dst_cloud)
        self.migration_status = notifiers.MigrationStateNotifier()

        for observer in self.init['migration_observers']:
            self.migration_status.add_observer(observer)

        if self._is_nfs_shared():
            self.migrate_func = self.reuse_source_volume
        else:
            self.migrate_func = self.migrate_volume

    def _is_nfs_shared(self):
        src_shared_nfs = isinstance(self.src_cinder_backend,
                                    generic.SharedNFSPlugin)
        dst_shared_nfs = isinstance(self.dst_cinder_backend,
                                    generic.SharedNFSPlugin)
        if src_shared_nfs and dst_shared_nfs:
            return True
        elif src_shared_nfs or dst_shared_nfs:
            msg = ("Invalid configuration of src or dst storage backends. "
                   "In case of shared-nfs both options of the backends must "
                   "be set to have a value of shared-nfs. Source storage "
                   "backend has '{src}' and destination storage backend has "
                   "'{dst}'")
            raise exception.InvalidConfigException(
                msg,
                src=self.cfg.src_storage.backend,
                dst=self.cfg.dst_storage.backend)
        else:
            return False

    def get_cinder_volumes(self, **kwargs):
        cinder_volumes_data = kwargs.get('storage_info')

        if cinder_volumes_data is None:
            LOG.warning("No volumes found in source cloud! Make sure you "
                        "have 'get_volumes_from_source' action enabled in "
                        "scenario. No volumes will be migrated.")
            return {}

        return cinder_volumes_data['volumes']

    def reuse_source_volume(self, src_volume):
        """Creates volume on destination with same id from source"""
        volume_id = src_volume['id']
        original_size = src_volume['size']
        src_volume_object = self.dst_cinder_backend.get_volume_object(
            self.dst_cloud, volume_id)
        LOG.debug("Backing file for source volume on destination cloud: %s",
                  src_volume_object)
        fake_volume = copy.deepcopy(src_volume)
        fake_volume['size'] = 1
        dst_volume, dst_volume_object = self._create_volume(fake_volume)
        user = self.dst_cloud.cloud_config.cloud.ssh_user
        password = self.dst_cloud.cloud_config.cloud.ssh_sudo_password
        rr = remote_runner.RemoteRunner(dst_volume_object.host, user,
                                        password=password, sudo=True,
                                        ignore_errors=True)
        files.remote_rm(rr, dst_volume_object.path)
        dst_cinder = self.dst_cloud.resources[utils.STORAGE_RESOURCE]
        dst_db = cinder_db.CinderDBBroker(dst_cinder.mysql_connector)
        dst_db.update_volume_id(dst_volume.id, volume_id)
        if original_size > 1:
            inc_size = original_size - 1
            project_id = dst_db.get_cinder_volume(volume_id).project_id
            dst_db.inc_quota_usages(project_id, 'gigabytes', inc_size)
            volume_type = (None
                           if dst_volume.volume_type == 'None'
                           else dst_volume.volume_type)
            if volume_type:
                dst_db.inc_quota_usages(project_id,
                                        'gigabytes_%s' % volume_type, inc_size)
        provider_location = self.dst_cinder_backend.get_provider_location(
            self.dst_cloud,
            dst_volume_object.host,
            src_volume_object.path
        )
        dst_db.update_volume(volume_id, provider_location=provider_location,
                             size=original_size)
        return dst_cinder.get_volume_by_id(volume_id)

    def migrate_volume(self, src_volume):
        """Creates volume on destination and copies volume data from source"""
        src_volume_object = self.src_cinder_backend.get_volume_object(
            self.src_cloud, src_volume['id'])
        LOG.debug("Backing file for source volume: %s",
                  src_volume_object)

        dst_volume, dst_volume_object = self._create_volume(src_volume)

        LOG.info("Starting volume copy from %s to %s",
                 src_volume_object, dst_volume_object)
        self.copy_volume_data(src_volume_object, dst_volume_object)

        return dst_volume

    def _create_volume(self, src_volume):
        src_keystone = self.src_cloud.resources[utils.IDENTITY_RESOURCE]
        dst_keystone = self.dst_cloud.resources[utils.IDENTITY_RESOURCE]
        dst_cinder = self.dst_cloud.resources[utils.STORAGE_RESOURCE]

        dst_tenant = keystone.get_dst_tenant_from_src_tenant_id(
            src_keystone, dst_keystone, src_volume['project_id'])
        if dst_tenant is None:
            msg = ("Tenant '{}' does not exist in destination, make sure "
                   "you migrated tenants.").format(
                src_volume['project_id'])
            LOG.warning(msg)
            raise exception.TenantNotPresentInDestination(msg)

        LOG.info("Creating volume of size %sG in tenant %s in destination",
                 src_volume['size'], dst_tenant.name)
        LOG.debug('Volume: %s', src_volume)
        dst_volume = dst_cinder.create_volume_from_volume(src_volume,
                                                          dst_tenant.id)
        LOG.info("Volume created: %s", volume_name(dst_volume))

        # It takes time to create volume object
        timeout = self.cfg.migrate.storage_backend_timeout
        retryer = retrying.Retry(max_time=timeout)
        dst_volume_object = retryer.run(
            self.dst_cinder_backend.get_volume_object,
            self.dst_cloud, dst_volume.id)

        LOG.debug("Backing file for volume in destination: %s",
                  dst_volume_object)

        return dst_volume, dst_volume_object

    def run(self, **kwargs):
        """:returns: dictionary {<source-volume-id>: <destination-volume>}"""

        if self._is_nfs_shared():
            mysql_connector.dump_db(
                self.dst_cloud,
                self.dst_cloud.cloud_config.storage.db_name)

        new_volumes = {}
        volumes = self.get_cinder_volumes(**kwargs)
        volumes = [v['volume'] for v in volumes.itervalues()]

        view = VolumeMigrationView(volumes)
        view.initial_message()

        for i, src_volume in enumerate(volumes):
            view.before_migration(i, src_volume)

            LOG.info("Checking if volume '%s' already present in destination",
                     volume_name(src_volume))
            dst_cinder = self.dst_cloud.resources[utils.STORAGE_RESOURCE]

            dst_volume = dst_cinder.get_migrated_volume(src_volume['id'])

            if dst_volume is not None:
                msg = ("Volume '%s' is already present in destination "
                       "cloud, skipping" % src_volume['id'])
                self.migration_status.skip(
                    objects.MigrationObjectType.VOLUME,
                    src_volume, msg)
            else:
                try:
                    dst_volume = self.migrate_func(src_volume)
                    self.migration_status.success(
                        objects.MigrationObjectType.VOLUME,
                        src_volume,
                        dst_volume.id)
                except (plugins.base.VolumeObjectNotFoundError,
                        retrying.TimeoutExceeded,
                        exception.TenantNotPresentInDestination,
                        cinder_exceptions.ClientException,
                        copy_mechanisms.CopyFailed,
                        copy_engines_base.NotEnoughSpace,
                        mysql_connector.MySQLError) as e:
                    LOG.warning("%(error)s, volume %(name)s will be skipped",
                                {'error': e.message,
                                 'name': volume_name(src_volume)})

                    self.migration_status.fail(
                        objects.MigrationObjectType.VOLUME,
                        src_volume,
                        e.message)

                    dst_volume = dst_cinder.get_migrated_volume(
                        src_volume['id'])
                    if dst_volume is not None:
                        msg = ("Removing volume {name} from destination "
                               "since it didn't migrate properly".format(
                                   name=volume_name(dst_volume)))
                        LOG.info(msg)
                        self.delete_volume(dst_volume)
                finally:
                    if dst_volume is not None:
                        self.dst_cinder_backend.cleanup(self.cloud,
                                                        dst_volume.id)

            view.after_migration(i, src_volume)
            new_volumes[src_volume['id']] = dst_volume
        return new_volumes

    def copy_volume_data(self, src_volume_object, dst_volume_object):
        copier = plugins.copy_mechanism_from_plugin_names(
            self.src_cinder_backend.PLUGIN_NAME,
            self.dst_cinder_backend.PLUGIN_NAME)
        if src_volume_object is not None and dst_volume_object is not None:
            copier.copy(self, src_volume_object, dst_volume_object)

    def delete_volume(self, volume_id):
        dst_storage = self.dst_cloud.resources[utils.STORAGE_RESOURCE]
        cinder_client = dst_storage.get_client()
        cinder_client.volumes.delete(volume_id)
