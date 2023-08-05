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

from cloudferry.lib.base import exception
from cloudferry.lib.os.storage.plugins import base
from cloudferry.lib.os.storage.plugins import copy_mechanisms
from cloudferry.lib.utils import files
from cloudferry.lib.utils import remote_runner
from cloudferry.lib.utils import log

LOG = log.getLogger(__name__)


def generate_volume_pattern(volume_template, volume_id):
    try:
        return volume_template % volume_id
    except TypeError:
        msg = "Invalid volume name template '%s' specified in config."
        LOG.error(msg)
        raise exception.InvalidConfigException(msg)


class NFSPlugin(base.CinderMigrationPlugin):
    """Adds support for NFS cinder backends, such as NetApp NFS, and generic
    cinder NFS driver.

    Looks for cinder volume objects on source controller in
    `nfs_mount_point_base` folder based on `volume_name_template` pattern.

    Required configuration:
     - [[src|dst]_storage] volume_name_template
     - [[src|dst]_storage] nfs_mount_point_base
    """

    PLUGIN_NAME = "nfs"

    @classmethod
    def from_context(cls, _):
        return cls()

    def get_volume_object(self, context, volume_id):
        """:raises: VolumeObjectNotFoundError in case object is not found"""
        controller = context.cloud_config.cloud.ssh_host
        user = context.cloud_config.cloud.ssh_user
        password = context.cloud_config.cloud.ssh_sudo_password
        paths = context.cloud_config.storage.nfs_mount_point_bases
        volume_template = context.cloud_config.storage.volume_name_template

        volume_pattern = generate_volume_pattern(volume_template, volume_id)

        rr = remote_runner.RemoteRunner(
            controller, user, ignore_errors=True, sudo=True, password=password)

        for mount_point in paths:
            # errors are ignored to avoid "Filesystem loop detected" messages
            # which don't matter anyways
            find = "find {mount_point} -name '{volume_pattern}' 2>/dev/null"
            res = rr.run(find.format(mount_point=mount_point,
                                     volume_pattern=volume_pattern))

            if res:
                # there should only be one file matching
                path = res.stdout.splitlines().pop()
                return copy_mechanisms.CopyObject(host=controller, path=path)

        msg = ("Volume object for volume '{volume_id}' not found. Either "
               "volume exists in DB, but is not present on storage, or "
               "'nfs_mount_point_bases' is set incorrectly in config")
        raise base.VolumeObjectNotFoundError(msg.format(volume_id=volume_id))


class SharedNFSPlugin(NFSPlugin):
    PLUGIN_NAME = "shared-nfs"

    @staticmethod
    def get_provider_location(context, host, path):
        user = context.cloud_config.cloud.ssh_user
        password = context.cloud_config.cloud.ssh_sudo_password

        rr = remote_runner.RemoteRunner(host, user, password=password,
                                        sudo=True,
                                        ignore_errors=True)

        df = files.remote_df(rr, path=path)
        return df[0]['filesystem'] if df else None
