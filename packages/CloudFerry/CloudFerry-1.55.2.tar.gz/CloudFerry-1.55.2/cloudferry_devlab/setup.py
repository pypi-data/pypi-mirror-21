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

from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup

all_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(r.req) for r in all_reqs]


setup(name='cloudferry_devlab',
      description='Devlab scripts and functional tests for CloudFerry tool.',
      url='https://github.com/MirantisWorkloadMobility/CloudFerry/tree/master/'
          'cloudferry_devlab',
      author='Mirantis Workload Mobility',
      author_email='workloadmobility@mirantis.com',
      license='Apache',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'generate_load = cloudferry_devlab.bin.main:main',
              'restore_vms_state = cloudferry_devlab.bin.main:restore_vms'
          ],
      },
      package_data={'cloudferry_devlab.tests.testcases':
                    ['groups_example.yaml']},
      install_requires=reqs)
