#!/usr/bin/env python
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

import argparse
import ConfigParser

from cloudferry_devlab import generate_load
from cloudferry_devlab.tests import base
from cloudferry_devlab.tests import config


def main():
    parser = argparse.ArgumentParser(
        description='Script to generate load for Openstack and delete '
                    'generated objects')
    parser.add_argument('--clean', help='Clean objects, described '
                                        'in configuration.ini file',
                        action='store_true')
    parser.add_argument('--env', default='SRC', choices=['SRC', 'DST'],
                        help='Choose cloud: SRC or DST')
    parser.add_argument('--generation-results', default='.',
                        help='Path to store filter, mapping files')
    parser.add_argument('cloudsconf', type=argparse.FileType('r'),
                        help='Please point configuration.ini file location')

    args = parser.parse_args()
    confparser = ConfigParser.ConfigParser()
    confparser.readfp(args.cloudsconf)
    cloudsconf = base.get_dict_from_config_file(confparser)

    preqs = generate_load.Prerequisites(config=config,
                                        configuration_ini=cloudsconf,
                                        cloud_prefix=args.env,
                                        results_path=args.generation_results)
    if args.clean:
        preqs.clean_tools.clean_objects()
    else:
        preqs.run_preparation_scenario()


def restore_vms():
    parser = argparse.ArgumentParser(
        description='Script to restore pre-generated VMs state.')
    parser.add_argument('cloudsconf', type=argparse.FileType('r'),
                        help='Please point configuration.ini file location')

    args = parser.parse_args()
    confparser = ConfigParser.ConfigParser()
    confparser.readfp(args.cloudsconf)
    cloudsconf = base.get_dict_from_config_file(confparser)

    preqs = generate_load.Prerequisites(config=config,
                                        configuration_ini=cloudsconf)
    preqs.run_restore_vms_state()


if __name__ == '__main__':
    main()
