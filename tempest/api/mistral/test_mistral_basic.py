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

from tempest.api.mistral import base
from tempest.test import attr


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

