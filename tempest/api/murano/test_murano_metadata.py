# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import testtools
from tempest import exceptions
from tempest.test import attr
from tempest.api.murano import base
import tempest.config as config

class SanityMuranoTest(base.MuranoMeta):

    def test_get_list_metadata_objects_ui(self):
        resp, body = self.get_list_metadata_objects("ui")
        assert body is not None
        assert resp['status'] == '200'

    def test_get_list_metadata_objects_workflows(self):
        resp, body = self.get_list_metadata_objects("workflows")
        assert body is not None
        assert resp['status'] == '200'

    def test_get_list_metadata_objects_heat(self):
        resp, body = self.get_list_metadata_objects("heat")
        assert body is not None
        assert resp['status'] == '200'

    def test_get_list_metadata_objects_agent(self):
        resp, body = self.get_list_metadata_objects("agent")
        assert body is not None
        assert resp['status'] == '200'

    def test_get_list_metadata_objects_scripts(self):
        resp, body = self.get_list_metadata_objects("scripts")
        assert body is not None
        assert resp['status'] == '200'

    def test_get_list_metadata_objects_manifests(self):
        resp, body = self.get_list_metadata_objects("manifests")
        assert body is not None
        assert resp['status'] == '200'

    def test_get_ui_definitions(self):
        resp, body = self.get_ui_definitions()
        assert body is not None
        assert resp['status'] == '200'

    def test_get_conductor_metadata(self):
        resp, body = self.get_conductor_metadata()
        assert body is not None
        assert resp['status'] == '200'

    def test_create_directory_and_delete_workflows(self):
        resp, body = self.create_directory("workflows/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("workflows/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    def test_create_directory_and_delete_ui(self):
        resp, body = self.create_directory("ui/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("ui/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    def test_create_directory_and_delete_heat(self):
        resp, body = self.create_directory("heat/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("heat/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    def test_create_directory_and_delete_agent(self):
        resp, body = self.create_directory("agent/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("agent/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    def test_upload_file_and_delete(self):
        resp = self.upload_metadata_object("testfile.txt", "workflows")
        resp1, body1 = self.get_list_metadata_objects("workflows")
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    def test_get_metadata_object(self):
        self.upload_metadata_object("testfile.txt", "workflows")
        resp1, body1 = self.get_metadata_object("workflows/testfile.txt")
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")
        assert resp1['status'] == '200'
        assert body1 is not None
