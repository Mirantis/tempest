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
from tempest.api.mistral import base
from tempest.test import attr
from tempest import exceptions


class SanityTests(base.MistralTest):

    @attr(type='smoke')
    def test_check_base_url(self):
        resp, _ = self.check_base_url()
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_obj(self):
        resp, _ = self.check_base_url_with_version()
        assert resp['status'] == '200'

    @attr(type='smoke')
    def test_get_list_workbooks(self):
        resp, body = self.get_list_obj('workbooks')
        assert resp['status'] == '200'
        assert body['workbooks'] == []

    @attr(type='smoke')
    def test_get_workbook(self):
        self.create_obj('workbooks', 'test')
        self.obj.append(['workbooks', 'test'])
        resp, body = self.get_list_obj('workbooks/test')
        assert resp['status'] == '200'
        assert body['name'] == 'test'
        self.delete_obj('workbooks', 'test')
        self.obj.pop(self.obj.index(['workbooks', 'test']))

    @attr(type='smoke')
    def test_get_executions(self):
        self.create_obj('workbooks', 'test')
        self.obj.append(['workbooks', 'test'])
        resp, body = self.get_list_obj('workbooks/test/executions')
        assert resp['status'] == '200'
        assert body['executions'] == []
        self.delete_obj('workbooks', 'test')
        self.obj.pop(self.obj.index(['workbooks', 'test']))

    @attr(type='smoke')
    def test_create_and_delete_workbook(self):
        resp, body = self.create_obj('workbooks', 'test')
        self.obj.append(['workbooks', 'test'])
        assert resp['status'] == '201'
        assert body['name'] == 'test'
        resp, body = self.get_list_obj('workbooks')
        assert resp['status'] == '200'
        assert body['workbooks'][0]['name'] == 'test'
        self.delete_obj('workbooks', 'test')
        _, body = self.get_list_obj('workbooks')
        assert body['workbooks'] == []
        self.obj.pop(self.obj.index(['workbooks', 'test']))

    @attr(type='smoke')
    def test_update_workbook(self):
        self.create_obj('workbooks', 'test')
        self.obj.append(['workbooks', 'test'])
        resp, body = self.update_obj('workbooks', 'test')
        self.obj.pop(self.obj.index(['workbooks', 'test']))
        assert resp['status'] == '200'
        assert body['name'] == 'testupdated'
        self.obj.append(['workbooks', 'testupdated'])
        self.delete_obj('workbooks', 'testupdated')
        self.obj.pop(self.obj.index(['workbooks', 'testupdated']))

    @attr(type='smoke')
    def test_get_workbook_definition(self):
        self.create_obj('workbooks', 'test')
        self.obj.append(['workbooks', 'test'])
        resp, body = self.get_workbook_definition('test')
        assert resp['status'] == '200'
        assert body is not None
        self.delete_obj('workbooks', 'test')
        self.obj.pop(self.obj.index(['workbooks', 'test']))

    @testtools.skip('it is not realised')
    @attr(type='smoke')
    def test_upload_workbook_definition(self):
        self.create_obj('workbooks', 'test1')
        self.obj.append(['workbooks', 'test1'])
        resp, body = self.upload_workbook_definition('test1')
        assert resp['status'] == '200'
        self.delete_obj('workbooks', 'test1')
        self.obj.pop(self.obj.index(['workbooks', 'test1']))

    @attr(type='negative')
    def test_double_create_obj(self):
        self.create_obj('workbooks', 'test')
        self.obj.append(['workbooks', 'test'])
        self.assertRaises(exceptions.BadRequest, self.create_obj, 'workbooks',
                          'test')
        self.delete_obj('workbooks', 'test')
        _, body = self.get_list_obj('workbooks')
        assert body['workbooks'] == []
        self.obj.pop(self.obj.index(['workbooks', 'test']))

