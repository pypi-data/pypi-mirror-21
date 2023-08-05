# Copyright 2016 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import abc
import logging

from oslo_utils import importutils

from cloudferry.lib.utils import local_db

LOG = logging.getLogger(__name__)

local_db.execute_once("""
CREATE TABLE IF NOT EXISTS stages (
    stage TEXT,
    signature JSON,
    PRIMARY KEY (stage)
)
""")


class Stage(object):
    __metaclass__ = abc.ABCMeta
    dependencies = []

    def __init__(self, config):
        """
        Stage constructor
        :param config: cloudferry.lib.config.Configuration instance
        :return:
        """
        self.config = config

    @abc.abstractmethod
    def signature(self):
        """
        Returns signature for data that will be produced during this stage. If
        the signature differ from the one stored in database, then invalidate
        method will be called.
        :return:
        """
        return

    @abc.abstractmethod
    def execute(self):
        """
        Should contain any code that is required to be executed during this
        stage.
        """
        return

    @abc.abstractmethod
    def invalidate(self, old_signature, new_signature, force=False):
        """
        Should destroy any stale data based on signature difference.
        :param old_signature: old signature stored in DB
        :param new_signature: new signature
        """
        return


def execute_stage(class_name, config, force=False):
    """
    Execute stage specified by `class_name` argument.
    :param class_name: fully qualified stage class name
    :param config: config.Configuration instance
    """

    # Create stage object
    cls = importutils.import_class(class_name)
    assert issubclass(cls, Stage)
    stage = cls(config)

    # Execute dependency stages
    for dependency in stage.dependencies:
        execute_stage(dependency, config)

    # Check if there is data from this stage in local DB
    new_signature = stage.signature()
    old_signature = None
    need_invalidate = False
    need_execute = False
    with local_db.Transaction() as tx:
        row = tx.query_one('SELECT signature FROM stages WHERE stage=:stage',
                           stage=class_name)
        if row is None:
            need_execute = True
        else:
            old_signature = row['signature'].data
            need_invalidate = (old_signature != new_signature)

    # Run invalidate and execute if needed
    with local_db.Transaction() as tx:
        if need_invalidate or force:
            stage.invalidate(old_signature, new_signature, force=force)
            tx.execute('DELETE FROM stages WHERE stage=:stage',
                       stage=class_name)
            need_execute = True
        if need_execute:
            stage.execute()
            tx.execute('INSERT INTO stages VALUES (:stage, :signature)',
                       stage=class_name,
                       signature=local_db.Json(new_signature))
            LOG.info('Stage %s executed successfully', class_name)
        else:
            LOG.info('Skipping stage %s', class_name)
