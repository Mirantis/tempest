# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack, LLC
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.api.object_storage import base
from tempest.common.utils.data_utils import rand_name
from tempest import exceptions
from tempest.test import attr
from tempest.test import HTTP_SUCCESS


class AccountTest(base.BaseObjectTest):
    @classmethod
    def setUpClass(cls):
        super(AccountTest, cls).setUpClass()
        cls.container_name = rand_name(name='TestContainer')
        cls.container_client.create_container(cls.container_name)

    @classmethod
    def tearDownClass(cls):
        cls.container_client.delete_container(cls.container_name)

    @attr(type='smoke')
    def test_list_containers(self):
        # list of all containers should not be empty
        params = {'format': 'json'}
        resp, container_list = \
            self.account_client.list_account_containers(params=params)

        self.assertIsNotNone(container_list)
        container_names = [c['name'] for c in container_list]
        self.assertTrue(self.container_name in container_names)

    @attr(type='smoke')
    def test_list_account_metadata(self):
        # list all account metadata
        resp, metadata = self.account_client.list_account_metadata()
        self.assertIn(int(resp['status']), HTTP_SUCCESS)
        self.assertIn('x-account-object-count', resp)
        self.assertIn('x-account-container-count', resp)
        self.assertIn('x-account-bytes-used', resp)

    @attr(type='smoke')
    def test_create_and_delete_account_metadata(self):
        header = 'test-account-meta'
        data = 'Meta!'
        # add metadata to account
        resp, _ = self.account_client.create_account_metadata(
            metadata={header: data})
        self.assertIn(int(resp['status']), HTTP_SUCCESS)

        resp, _ = self.account_client.list_account_metadata()
        self.assertIn('x-account-meta-' + header, resp)
        self.assertEqual(resp['x-account-meta-' + header], data)

        # delete metadata from account
        resp, _ = \
            self.account_client.delete_account_metadata(metadata=[header])
        self.assertIn(int(resp['status']), HTTP_SUCCESS)

        resp, _ = self.account_client.list_account_metadata()
        self.assertNotIn('x-account-meta-' + header, resp)

    @attr(type=['negative', 'gate'])
    def test_list_containers_with_non_authorized_user(self):
        # list containers using non-authorized user

        # create user
        self.data.setup_test_user()
        resp, body = \
            self.token_client.auth(self.data.test_user,
                                   self.data.test_password,
                                   self.data.test_tenant)
        new_token = \
            self.token_client.get_token(self.data.test_user,
                                        self.data.test_password,
                                        self.data.test_tenant)
        custom_headers = {'X-Auth-Token': new_token}
        params = {'format': 'json'}
        # list containers with non-authorized user token
        self.assertRaises(exceptions.Unauthorized,
                          self.custom_account_client.list_account_containers,
                          params=params, metadata=custom_headers)
        # delete the user which was created
        self.data.teardown_all()
