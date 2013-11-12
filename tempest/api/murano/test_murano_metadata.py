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
from tempest.test import attr
from tempest.api.murano import base

class SanityMuranoTest(base.MuranoMeta):

    @attr(type='smoke')
    def test_get_list_metadata_objects_ui(self):
        resp, body = self.get_list_metadata_objects("ui")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_workflows(self):
        resp, body = self.get_list_metadata_objects("workflows")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_heat(self):
        resp, body = self.get_list_metadata_objects("heat")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_agent(self):
        resp, body = self.get_list_metadata_objects("agent")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_scripts(self):
        resp, body = self.get_list_metadata_objects("scripts")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_metadata_objects_manifests(self):
        resp, body = self.get_list_metadata_objects("manifests")
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='negative')
    def test_get_list_metadata_objects_uncorrect_type(self):
        self.assertRaises(Exception, self.get_list_metadata_objects,
                          "someth")

    @attr(type='smoke')
    def test_get_ui_definitions(self):
        resp, body = self.get_ui_definitions()
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_conductor_metadata(self):
        resp, body = self.get_conductor_metadata()
        assert body is not None
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_create_directory_and_delete_workflows(self):
        resp, body = self.create_directory("workflows/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("workflows/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    @attr(type='smoke')
    def test_create_directory_and_delete_ui(self):
        resp, body = self.create_directory("ui/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("ui/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    @attr(type='smoke')
    def test_create_directory_and_delete_heat(self):
        resp, body = self.create_directory("heat/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("heat/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    @attr(type='smoke')
    def test_create_directory_and_delete_agent(self):
        resp, body = self.create_directory("agent/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("agent/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    @attr(type='smoke')
    def test_create_directory_and_delete_scripts(self):
        resp, body = self.create_directory("scripts/", "testdir")
        resp1, body1 = self.delete_metadata_obj_or_folder("scripts/testdir")
        assert resp['status'] == '200'
        assert resp1['status'] == '200'

    @attr(type='negative')
    def test_create_directory_uncorrect_type(self):
        self.assertRaises(Exception, self.create_directory,
                          "someth/", "testdir")

    @testtools.skip('It is look as a bug')
    @attr(type='negative')
    def test_double_create_directory(self):
        self.create_directory("workflows/", "testdir")
        self.assertRaises(Exception, self.create_directory,
                          "workflows/", "testdir")
        self.delete_metadata_obj_or_folder("workflows/testdir")

    @attr(type='negative')
    def test_delete_nonexistent_object(self):
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "somth/blabla")

    @attr(type='negative')
    def test_delete_basic_folder(self):
        self.assertRaises(Exception, self.delete_metadata_obj_or_folder,
                          "workflows")

    @attr(type='negative')
    def test_create_basic_folder(self):
        self.assertRaises(Exception, self.create_directory,
                          "", "somth")

    @attr(type='negative')
    def test_double_upload_file(self):
        self.upload_metadata_object(path="workflows")
        resp = self.upload_metadata_object(path="workflows")
        assert resp.status_code == 403
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")

    @attr(type='negative')
    def test_upload_file_uncorrect(self):
        resp = self.upload_metadata_object(path="workflows/testfil")
        assert resp.status_code == 404

    @attr(type='smoke')
    def test_upload_file_and_delete_workflows(self):
        resp = self.upload_metadata_object(path="workflows")
        resp1, body1 = self.get_list_metadata_objects("workflows")
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_ui(self):
        resp = self.upload_metadata_object(path="ui")
        resp1, body1 = self.get_list_metadata_objects("ui")
        self.delete_metadata_obj_or_folder("ui/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_heat(self):
        resp = self.upload_metadata_object(path="heat")
        resp1, body1 = self.get_list_metadata_objects("heat")
        self.delete_metadata_obj_or_folder("heat/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_agent(self):
        resp = self.upload_metadata_object(path="agent")
        resp1, body1 = self.get_list_metadata_objects("agent")
        self.delete_metadata_obj_or_folder("agent/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_upload_file_and_delete_scripts(self):
        resp = self.upload_metadata_object(path="scripts")
        resp1, body1 = self.get_list_metadata_objects("scripts")
        self.delete_metadata_obj_or_folder("scripts/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    @testtools.skip('It is look as a bug')
    def test_upload_file_and_delete_manifests(self):
        resp = self.upload_metadata_object(path="manifests")
        resp1, body1 = self.get_list_metadata_objects("manifests")
        self.delete_metadata_obj_or_folder("manifests/testfile.txt")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)

    @attr(type='smoke')
    def test_get_metadata_object(self):
        self.upload_metadata_object(path="workflows")
        resp1, body1 = self.get_metadata_object("workflows/testfile.txt")
        self.delete_metadata_obj_or_folder("workflows/testfile.txt")
        assert resp1['status'] == '200'
        assert body1 is not None

    @attr(type='negative')
    def test_get_nonexistent_metadata_object(self):
        self.assertRaises(Exception, self.get_metadata_object,
                          "somth/blabla")

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='smoke')
    def test_create_directory_and_upload_file_workflows(self):
        self.create_directory("workflows/", "testdir")
        resp = self.upload_metadata_object(path="workflows/testdir")
        resp1, body1 = self.get_list_metadata_objects("workflows/testdir")
        resp2, body2 = self.delete_metadata_obj_or_folder("workflows/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        assert resp2['status'] == '200'
        resp1, body1 = self.get_list_metadata_objects("workflows")
        assert resp1['status'] == '200'
        assert ('testfile.txt' not in body1)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='smoke')
    def test_create_directory_and_upload_file_ui(self):
        self.create_directory("ui/", "testdir")
        resp = self.upload_metadata_object(path="ui/testdir")
        resp1, body1 = self.get_list_metadata_objects("ui/testdir")
        resp2, body2 = self.delete_metadata_obj_or_folder("ui/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        assert resp2['status'] == '200'
        resp1, body1 = self.get_list_metadata_objects("ui")
        assert resp1['status'] == '200'
        assert ('testfile.txt' not in body1)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='smoke')
    def test_create_directory_and_upload_file_heat(self):
        self.create_directory("heat/", "testdir")
        resp = self.upload_metadata_object(path="heat/testdir")
        resp1, body1 = self.get_list_metadata_objects("heat/testdir")
        resp2, body2 = self.delete_metadata_obj_or_folder("heat/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        assert resp2['status'] == '200'
        resp1, body1 = self.get_list_metadata_objects("heat")
        assert resp1['status'] == '200'
        assert ('testfile.txt' not in body1)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='smoke')
    def test_create_directory_and_upload_file_agent(self):
        self.create_directory("agent/", "testdir")
        resp = self.upload_metadata_object(path="agent/testdir")
        resp1, body1 = self.get_list_metadata_objects("agent/testdir")
        resp2, body2 = self.delete_metadata_obj_or_folder("agent/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        assert resp2['status'] == '200'
        resp1, body1 = self.get_list_metadata_objects("agent")
        assert resp1['status'] == '200'
        assert ('testfile.txt' not in body1)

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1249303')
    @attr(type='smoke')
    def test_create_directory_and_upload_file_scripts(self):
        self.create_directory("scripts/", "testdir")
        resp = self.upload_metadata_object(path="scripts/testdir")
        resp1, body1 = self.get_list_metadata_objects("scripts/testdir")
        resp2, body2 = self.delete_metadata_obj_or_folder("scripts/testdir")
        assert resp.status_code == 200
        assert resp1['status'] == '200'
        assert ('testfile.txt' in body1)
        assert resp2['status'] == '200'
        resp1, body1 = self.get_list_metadata_objects("scripts")
        assert resp1['status'] == '200'
        assert ('testfile.txt' not in body1)
