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
import StringIO

from cloudferry.lib.utils import override
from tests import test


class AttributeOverrideTestCase(test.TestCase):
    def test_empty_overrides_dont_change_attribute(self):
        obj = {'foo': 'bar'}
        overrides = override.AttributeOverrides.zero()
        self.assertEqual('bar', overrides.get_attr(obj, 'foo'))

    def test_simple_mapping(self):
        obj = {
            'foo': 'bar'
        }
        overrides = override.AttributeOverrides({
            'foo': [
                {'when': 'bar', 'replace': 'baz'},
            ]
        })
        self.assertEqual('baz', overrides.get_attr(obj, 'foo'))

    def test_full_mapping1(self):
        obj1 = {
            'foo': 'bar'
        }
        obj2 = {
            'foo': 'baz'
        }
        overrides = override.AttributeOverrides({
            'foo': [
                {'when': {'foo': ['bar', 'baz']}, 'replace': 'qux'},
            ]
        })
        self.assertEqual('qux', overrides.get_attr(obj1, 'foo'))
        self.assertEqual('qux', overrides.get_attr(obj2, 'foo'))

    def test_full_mapping2(self):
        obj1 = {
            'foo': 'bar',
            'additional': 1337,
        }
        obj2 = {
            'foo': 'baz',
            'additional': 1338,
        }
        overrides = override.AttributeOverrides({
            'foo': [
                {
                    'when': {
                        'foo': ['bar', 'baz'],
                        'additional': [1337],
                    },
                    'replace': 'qux'
                },
                {
                    'when': {
                        'foo': ['bar'],
                        'additional': [1338],
                    },
                    'replace': 'quux'
                },
                {
                    'when': {
                        'foo': ['baz'],
                        'additional': [1338],
                    },
                    'replace': 'quuux'
                },
            ]
        })
        self.assertEqual('qux', overrides.get_attr(obj1, 'foo'))
        self.assertEqual('quuux', overrides.get_attr(obj2, 'foo'))

    def test_default(self):
        obj = {
            'foo': 'bar'
        }
        overrides = override.AttributeOverrides({
            'foo': [
                {'when': {'foo': ['foo']}, 'replace': 'qux'},
                {'default': 'quux'}
            ]
        })
        self.assertEqual('quux', overrides.get_attr(obj, 'foo'))

    def test_raises_error_if_volumes_or_servers_are_not_present(self):
        invalid_yaml = """
        wrong_option:
            availability_zone:
                - when: x
                  replace: y
        servers:
            availability_zone:
                - when: p
                  replace: n
        """

        stream = StringIO.StringIO(invalid_yaml)

        self.assertRaises(override.InvalidOverrideConfigError,
                          override.AttributeOverrides.from_stream,
                          stream, 'servers')

    def test_not_raises_error_if_one_of_allowed_types_is_present(self):
        correct_yaml1 = """
        servers:
            availability_zone:
                - when: x
                  replace: y
        """

        correct_yaml2 = """
        volumes:
            availability_zone:
                - when: x
                  replace: y
        """

        yamls = [correct_yaml1, correct_yaml2]

        for yaml in yamls:
            stream = StringIO.StringIO(yaml)

            try:
                override.AttributeOverrides.from_stream(stream, 'servers')
            except (TypeError, override.InvalidOverrideConfigError) as e:
                self.fail("AttributeOverrides should not raise error for "
                          "yamls having 'volumes' and 'servers' object "
                          "types, instead got error: '%s'" % e)
