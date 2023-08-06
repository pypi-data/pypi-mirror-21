# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock

from oslo_config import cfg
from oslo_db import options
from oslotest import base

from neutron_lib.callbacks import registry
from neutron_lib.db import model_base
from neutron_lib import fixture
from neutron_lib.plugins import directory


class PluginDirectoryFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(PluginDirectoryFixtureTestCase, self).setUp()
        self.directory = mock.Mock()
        self.useFixture(fixture.PluginDirectoryFixture(
            plugin_directory=self.directory))

    def test_fixture(self):
        directory.add_plugin('foo', 'foo')
        self.assertTrue(self.directory.add_plugin.called)


class CallbackRegistryFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(CallbackRegistryFixtureTestCase, self).setUp()
        self.manager = mock.Mock()
        self.useFixture(fixture.CallbackRegistryFixture(
            callback_manager=self.manager))

    def test_fixture(self):
        registry.notify('a', 'b', self)
        self.assertTrue(self.manager.notify.called)


class SqlFixtureTestCase(base.BaseTestCase):

    def setUp(self):
        super(SqlFixtureTestCase, self).setUp()
        options.set_defaults(
            cfg.CONF,
            connection='sqlite://')
        self.useFixture(fixture.SqlFixture())

    def test_fixture(self):
        self.assertIsNotNone(model_base.BASEV2.metadata.sorted_tables)


class APIDefinitionFixtureTestCase(base.BaseTestCase):

    _ATTR_MAP_1 = {'routers': {'name': 'a'}}
    _ATTR_MAP_2 = {'ports': {'description': 'a'}}

    def setUp(self):
        super(APIDefinitionFixtureTestCase, self).setUp()
        self.routers_def = mock.Mock()
        self.routers_def.RESOURCE_ATTRIBUTE_MAP = (
            APIDefinitionFixtureTestCase._ATTR_MAP_1)
        self.ports_def = mock.Mock()
        self.ports_def.RESOURCE_ATTRIBUTE_MAP = (
            APIDefinitionFixtureTestCase._ATTR_MAP_2)
        self.useFixture(fixture.APIDefinitionFixture(
            self.routers_def, self.ports_def))

    def test_fixture(self):
        # assert same contents, but different instances
        self.assertEqual(APIDefinitionFixtureTestCase._ATTR_MAP_1,
                         self.routers_def.RESOURCE_ATTRIBUTE_MAP)
        self.assertEqual(APIDefinitionFixtureTestCase._ATTR_MAP_2,
                         self.ports_def.RESOURCE_ATTRIBUTE_MAP)
        self.assertIsNot(APIDefinitionFixtureTestCase._ATTR_MAP_1,
                         self.routers_def.RESOURCE_ATTRIBUTE_MAP)
        self.assertIsNot(APIDefinitionFixtureTestCase._ATTR_MAP_2,
                         self.ports_def.RESOURCE_ATTRIBUTE_MAP)
