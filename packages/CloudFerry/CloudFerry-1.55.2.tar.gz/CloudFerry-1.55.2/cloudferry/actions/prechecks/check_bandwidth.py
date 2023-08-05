# Copyright (c) 2015 Mirantis Inc.
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

import os
import uuid


from cloudferry.lib.base.action import action
from cloudferry.lib.utils import files
from cloudferry.lib.utils import local
from cloudferry.lib.utils import log
from cloudferry.lib.utils import remote_runner
from cloudferry.lib.utils import ssh_util
from cloudferry.lib.utils import utils


LOG = log.getLogger(__name__)


class CheckBandwidth(action.Action):
    """Assesses networking bandwidth between CloudFerry node and controller
    node defined in `[src|dst] host` config variable.

    Process:
     1. Generate file of size `[initial_check] test_file_size` on CF node;
     2. Copy generated file to `[src|dst] host` over network (scp);
     3. Measure time required for file to be copied over;
     4. Calculate networking bandwidth based on measuring above;
     5. If bandwidth is smaller than `[initial_check] claimed_bandwidth` *
        `[initial_check] factor` - stop migration and display error message.

    Config options:
     - `[initial_check] test_file_size` - size of the file to be copied over;
     - `[initial_check] claimed_bandwidth` - expected bandwidth;
     - `[initial_check] factor` - fraction of 1 for the lowest acceptable
        bandwidth, e.g. `factor = 0.5` means expected bandwidth should not get
        below `0.5 * claimed_bandwidth`;
     - `[src|dst] host` - host the file will be copied to.
    """

    def run(self, **kwargs):
        cfg = self.cloud.cloud_config.cloud
        runner = remote_runner.RemoteRunner(cfg.ssh_host, cfg.ssh_user)

        with files.LocalTempDir('check_band_XXXX') as local_dir:
            with files.RemoteTempDir(runner, 'check_band_XXXX') as remote_dir:
                filename = str(uuid.uuid4())
                local_filepath = os.path.join(local_dir.dirname, filename)
                remote_filepath = os.path.join(remote_dir.dirname, filename)
                claimed_bandw = self.cloud.cloud_config.initial_check.\
                    claimed_bandwidth
                filesize = self.cloud.cloud_config.initial_check.test_file_size
                factor = self.cloud.cloud_config.initial_check.factor
                req_bandwidth = claimed_bandw * factor

                scp_download = "scp {ssh_opts} {user}@{host}:{filepath} " \
                               "{dirname}"
                scp_upload = "scp {ssh_opts} {filepath} {user}@{host}:" \
                             "{dirname}"
                dd_command = "dd if=/dev/zero of={filepath} bs=1 count=0 " \
                             "seek={filesize}"
                runner.run(dd_command,
                           filepath=remote_filepath,
                           filesize=filesize)

                LOG.info("Checking download speed... Wait please.")
                period_download = utils.timer(
                    local.run,
                    scp_download.format(
                        ssh_opts=ssh_util.default_ssh_options(),
                        user=cfg.ssh_user,
                        host=cfg.ssh_host,
                        filepath=remote_filepath,
                        dirname=local_dir.dirname
                    )
                )

                LOG.info("Checking upload speed... Wait please.")
                period_upload = utils.timer(
                    local.run,
                    scp_upload.format(
                        ssh_opts=ssh_util.default_ssh_options(),
                        filepath=local_filepath,
                        user=cfg.ssh_user,
                        host=cfg.ssh_host,
                        dirname=remote_dir.dirname
                    )
                )

        # To have Megabits per second
        upload_speed = filesize / period_upload * 8
        download_speed = filesize / period_download * 8

        if upload_speed < req_bandwidth or download_speed < req_bandwidth:
            raise RuntimeError('Bandwidth is not OK. '
                               'Claimed bandwidth: %s Mb/s. '
                               'Required speed: %s Mb/s. '
                               'Actual upload speed: %.2f Mb/s. '
                               'Actual download speed: %.2f Mb/s. '
                               'Aborting migration...' %
                               (claimed_bandw,
                                req_bandwidth,
                                upload_speed,
                                download_speed))

        LOG.info("Bandwith is OK. "
                 "Required speed: %.2f Mb/s. "
                 "Upload speed: %.2f Mb/s. "
                 "Download speed: %.2f Mb/s",
                 req_bandwidth,
                 upload_speed,
                 download_speed)
