# Copyright (c) 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
import logging
import random
import re

from cloudferry import model
from cloudferry.model import image
from cloudferry.model import compute
from cloudferry.lib.os import clients
from cloudferry.lib.os import cloud_db
from cloudferry.lib.os import consts
from cloudferry.lib.os.migrate import base
from cloudferry.lib.utils import remote

from glanceclient import exc as glance_exc

LOG = logging.getLogger(__name__)


class BaseImageMigrationTask(base.MigrationTask):
    # pylint: disable=abstract-method

    @property
    def src_glance(self):
        src_cloud = self.config.clouds[self.migration.source]
        return clients.image_client(src_cloud)

    @property
    def dst_glance(self):
        dst_cloud = self.config.clouds[self.migration.destination]
        return clients.image_client(dst_cloud)


class ReserveImage(BaseImageMigrationTask):
    default_provides = ['dst_object']

    def migrate(self, source_obj, *args, **kwargs):
        # TODO: update image properties related to Snapshots
        # TODO: support image created from URL
        dst_cloud = self.config.clouds[self.migration.destination]
        try:
            self.created_object = self.dst_glance.images.create(
                id=source_obj.primary_key.id,
                name=source_obj.name,
                container_format=source_obj.container_format,
                disk_format=source_obj.disk_format,
                is_public=source_obj.is_public,
                protected=source_obj.protected,
                owner=source_obj.tenant.get_uuid_in(dst_cloud),
                size=source_obj.size,
                properties=source_obj.properties)
        except glance_exc.HTTPConflict:
            img = self.dst_glance.images.get(source_obj.primary_key.id)
            if img.status == 'deleted':
                _reset_dst_image_status(self, source_obj)
                self._update_dst_image(source_obj)
            else:
                self._delete_dst_image(source_obj)
                _reset_dst_image_status(self, source_obj)
                self._update_dst_image(source_obj)

        result = self.load_from_cloud(
            image.Image, dst_cloud, self.created_object)
        return dict(dst_object=result)

    def revert(self, source_obj, *args, **kwargs):
        super(ReserveImage, self).revert(*args, **kwargs)
        if self.created_object is not None:
            self._delete_dst_image(source_obj)

    def _delete_dst_image(self, source_obj):
        dst_glance = self.dst_glance
        image_id = source_obj.object_id.id
        dst_glance.images.update(image_id, protected=False)
        dst_glance.images.delete(image_id)

    def _update_dst_image(self, source_obj):
        dst_cloud = self.config.clouds[self.migration.destination]
        self.created_object = self.dst_glance.images.update(
            source_obj.primary_key.id,
            name=source_obj.name,
            container_format=source_obj.container_format,
            disk_format=source_obj.disk_format,
            is_public=source_obj.is_public,
            protected=source_obj.protected,
            owner=source_obj.tenant.get_uuid_in(dst_cloud),
            size=source_obj.size,
            properties=source_obj.properties)


class _FileLikeProxy(object):
    # TODO: Merge with cloudferry.lib.utils.file_proxy stuff
    def __init__(self, iterable):
        self.iterable = iterable
        self.buf = bytes()

    def _fill_buf(self, size):
        """
        Fill buffer to contain at least ``size`` bytes.
        """
        while True:
            chunk = next(self.iterable, None)
            if chunk is None:
                break
            self.buf += bytes(chunk)
            if size is not None and len(self.buf) >= size:
                break

    def read(self, size=None):
        if size is None or len(self.buf) < size:
            self._fill_buf(size)
        if size is None:
            result, self.buf = self.buf, ''
        else:
            result, self.buf = self.buf[:size], self.buf[size:]
        return result


class UploadImage(BaseImageMigrationTask):
    default_provides = ['need_restore_deleted']

    def migrate(self, source_obj, dst_object, *args, **kwargs):
        if source_obj.status == 'deleted':
            return dict(need_restore_deleted=True)
        image_id = dst_object.object_id.id
        try:
            image_data = _FileLikeProxy(self.src_glance.images.data(image_id))
            self.dst_glance.images.update(image_id, data=image_data)
            return dict(need_restore_deleted=False)
        except glance_exc.HTTPNotFound:
            return dict(need_restore_deleted=True)


class UploadDeletedImage(BaseImageMigrationTask):
    def migrate(self, source_obj, dst_object, need_restore_deleted,
                *args, **kwargs):
        if not need_restore_deleted:
            return
        dst_image_id = dst_object.object_id.id
        with model.Session() as session:
            boot_disk_infos = self._get_boot_disk_locations(
                session, source_obj)

        for boot_disk_info in boot_disk_infos:
            if self.upload_server_image(boot_disk_info, dst_image_id,
                                        source_obj):
                return
        raise base.AbortMigration(
            'Unable to restore deleted image %s: no servers found',
            dst_image_id)

    def _get_boot_disk_locations(self, session, source_obj):
        boot_disk_infos = []
        src_cloud = self.config.clouds[self.migration.source]
        for server in session.list(compute.Server, src_cloud):
            if not server.image or server.image != source_obj:
                continue
            for disk in server.ephemeral_disks:
                if disk.base_path is not None and disk.path.endswith('disk'):
                    assert disk.base_size is not None
                    assert disk.base_format is not None
                    boot_disk_infos.append({
                        'host': server.hypervisor_hostname,
                        'base_path': disk.base_path,
                        'base_size': disk.base_size,
                        'base_format': disk.base_format,
                    })
                    break

        random.shuffle(boot_disk_infos)
        return boot_disk_infos

    def upload_server_image(self, boot_disk_info, dst_image_id, source_obj):
        src_cloud = self.config.clouds[self.migration.source]
        host = boot_disk_info['host']
        image_path = boot_disk_info['base_path']
        image_format = boot_disk_info['base_format']
        image_size = boot_disk_info['base_size']
        cloud = self.config.clouds[self.migration.destination]
        token = clients.get_token(cloud.credential, cloud.scope)
        endpoint = clients.get_endpoint(cloud.credential, cloud.scope,
                                        consts.ServiceType.IMAGE)
        _reset_dst_image_status(self, source_obj)
        with remote.RemoteExecutor(src_cloud, host) as remote_executor:
            curl_output = remote_executor.sudo(
                'curl -X PUT -w "\\n\\n<http_status=%{{http_code}}>" '
                '-H "X-Auth-Token: {token}" '
                '-H "Content-Type: application/octet-stream" '
                '-H "x-image-meta-disk_format: {disk_format}" '
                '-H "x-image-meta-size: {image_size}" '
                '--upload-file "{image_path}" '
                '"{endpoint}/v1/images/{image_id}"',
                token=token, endpoint=endpoint, image_id=dst_image_id,
                image_path=image_path, disk_format=image_format,
                image_size=image_size)
            match = re.search(r'<http_status=(\d+)>', curl_output)
            if match is None or int(match.group(1)) != 200:
                LOG.error('Failed to upload image: %s', curl_output)
                return False
            return True


def _reset_dst_image_status(task, source_obj):
    dst_cloud = task.config.clouds[task.migration.destination]
    with cloud_db.connection(dst_cloud.glance_db) as db:
        db.execute('UPDATE images SET deleted_at=NULL, deleted=0, '
                   'status=\'queued\', checksum=NULL WHERE id=%(image_id)s',
                   image_id=source_obj.primary_key.id)


class ImageMigrationFlowFactory(base.MigrationFlowFactory):
    migrated_class = image.Image

    def create_flow(self, config, migration, obj):
        return [
            ReserveImage(obj, config, migration),
            UploadImage(obj, config, migration),
            UploadDeletedImage(obj, config, migration),
            base.RememberMigration(obj, config, migration),
        ]


class MigrateImageMember(BaseImageMigrationTask):
    default_provides = ['dst_object']

    def migrate(self, source_obj, *args, **kwargs):
        dst_cloud = self.config.clouds[self.migration.destination]
        dst_image_id = source_obj.image.get_uuid_in(dst_cloud)
        dst_tenant_id = source_obj.member.get_uuid_in(dst_cloud)
        self.dst_glance.image_members.create(dst_image_id, dst_tenant_id,
                                             source_obj.can_share)
        image_member = self.load_from_cloud(
            image.ImageMember, dst_cloud, dict(
                image_id=dst_image_id, member_id=dst_tenant_id,
                can_share=source_obj.can_share))
        return dict(dst_object=image_member)

    def revert(self, source_obj, *args, **kwargs):
        super(MigrateImageMember, self).revert(*args, **kwargs)
        dst_cloud = self.config.clouds[self.migration.destination]
        dst_image_id = source_obj.image.get_uuid_in(dst_cloud)
        dst_tenant_id = source_obj.member.get_uuid_in(dst_cloud)
        self.dst_glance.image_members.delete(dst_image_id, dst_tenant_id)


class ImageMemberMigrationFlowFactory(base.MigrationFlowFactory):
    migrated_class = image.ImageMember

    def create_flow(self, config, migration, obj):
        return [
            MigrateImageMember(config, migration, obj),
            base.RememberMigration(config, migration, obj),
        ]
