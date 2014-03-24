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

from tempest.api.murano import base
from tempest.test import attr
from tempest import exceptions


class SanityMuranoTest(base.MuranoTest):

    @attr(type='smoke')
    def test_create_and_delete_AD(self):
        """
        Create and delete AD
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to remove AD
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        _, info = self.get_list_services(env['id'], sess['id'])

        resp, serv = self.create_AD(env['id'], sess['id'])

        _, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(len(infa) - len(info), 1)

        resp, infa = self.get_service_info(env['id'], sess['id'], serv['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(infa['name'], 'ad.local')

        self.delete_service(env['id'], sess['id'], serv['id'])
        _, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), len(info))

    @attr(type='negative')
    def test_create_AD_without_env_id(self):
        """
        Try create AD without env_id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD using wrong env_id
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        self.assertRaises(exceptions.NotFound,
                          self.create_AD,
                          None,
                          sess['id'])

    @attr(type='negative')
    def test_create_AD_without_sess_id(self):
        """
        Try to create AD without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD using incorrect session id
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        self.create_session(env['id'])

        self.assertRaises(exceptions.Unauthorized,
                          self.create_AD,
                          env['id'],
                          "")

    @attr(type='negative')
    def test_delete_AD_without_env_id(self):
        """
        Try to delete AD without environment id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to remove AD using incorrect environment id
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        resp, serv = self.create_AD(env['id'], sess['id'])

        self.assertRaises(exceptions.NotFound,
                          self.delete_service,
                          None,
                          sess['id'],
                          serv['id'])

    @attr(type='negative')
    def test_delete_AD_without_session_id(self):
        """
        Try to delete AD without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to remove AD using wrong session id
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        resp, serv = self.create_AD(env['id'], sess['id'])

        self.assertRaises(exceptions.Unauthorized,
                          self.delete_service,
                          env['id'],
                          "",
                          serv['id'])

    @attr(type='smoke')
    def test_get_list_services(self):
        """
        Get a list of services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to get list of services
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(resp.status, 200)
        self.assertTrue(isinstance(infa, list))

    @attr(type='negative')
    def test_get_list_of_services_wo_env_id(self):
        """
        Try to get services list without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get services list using wrong environment id
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        self.create_AD(env['id'], sess['id'])

        self.assertRaises(exceptions.NotFound, self.get_list_services,
                          None, sess['id'])

    @attr(type='negative')
    def test_get_list_of_services_wo_sess_id(self):
        """
        Try to get services list without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get services list using wrong session id
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        self.create_AD(env['id'], sess['id'])

        resp, somelist = self.get_list_services(env['id'], "")

        self.assertEqual(resp.status, 200)
        self.assertTrue(isinstance(somelist, list))

    @attr(type='negative')
    def test_get_list_of_services_after_delete_env(self):
        """
        Try to get services list after deleting env
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to delete environment
            5. Send request to get services list
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        self.create_AD(env['id'], sess['id'])

        self.delete_environment(env['id'])

        self.assertRaises(exceptions.NotFound, self.get_list_services,
                          env['id'], sess['id'])

        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_after_delete_session(self):
        """
        Try to get services list after deleting session
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to delete session
            5. Send request to get services list
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        self.create_AD(env['id'], sess['id'])

        self.delete_session(env['id'], sess['id'])

        self.assertRaises(exceptions.NotFound, self.get_list_services,
                          env['id'], sess['id'])

    @testtools.skip("Service is not yet able to do it")
    @attr(type='smoke')
    def test_update_service(self):
        """
        Update service
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to update service
            5. Send request to remove AD
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        resp, serv = self.create_AD(env['id'], sess['id'])

        self.update_service(env['id'], sess['id'], serv['id'], serv)
        self.delete_service(env['id'], sess['id'], serv['id'])

    @attr(type='smoke')
    def test_get_service_info(self):
        """
        Get service detailed info
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to get detailed info about service
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        resp, serv = self.create_AD(env['id'], sess['id'])

        resp, infa = self.get_service_info(env['id'], sess['id'], serv['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(infa['name'], 'ad.local')

    @attr(type='positive')
    def test_alternate_service_create1(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create session
            4. Send request to create session
            5. Send request to create AD(session1)
            6. Send request to create IIS(session1)
            7. Send request to create SQL(session1)
            8. Send request to create IIS(session3)
            9. Send request to create aspnet farm(session3)
            10. Send request to create AD(session3)
            11. Send request to create IIS farm(session3)
            12. Send request to create SQL cluster(session3)
            13. Send request to delete IIS(session1)
            14. Send request to create IIS(session2)
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess1 = self.create_session(env['id'])
        resp, sess2 = self.create_session(env['id'])
        resp, sess3 = self.create_session(env['id'])

        resp, serv1 = self.create_AD(env['id'], sess1['id'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])

        self.assertEqual(len(infa), 1)

        resp, serv2 = self.create_IIS(env['id'], sess1['id'], serv1['domain'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])

        self.assertEqual(len(infa), 2)

        self.create_SQL(env['id'], sess1['id'], serv1['domain'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])

        self.assertEqual(len(infa), 3)

        self.create_IIS(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])

        self.assertEqual(len(infa), 1)

        self.create_aspnet_farm(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])

        self.assertEqual(len(infa), 2)

        resp, serv33 = self.create_AD(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])

        self.assertEqual(len(infa), 3)

        self.create_IIS_farm(env['id'], sess3['id'], serv33['domain'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])

        self.assertEqual(len(infa), 4)

        self.create_SQL_cluster(env['id'], sess3['id'], serv33['domain'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])

        self.assertEqual(len(infa), 5)

        self.delete_service(env['id'], sess1['id'], serv2['id'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])

        self.assertEqual(len(infa), 2)

        self.create_IIS(env['id'], sess2['id'])
        resp, infa = self.get_list_services(env['id'], sess2['id'])

        self.assertEqual(len(infa), 1)

    @attr(type='positive')
    def test_alternate_service_create2(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create aspnet farm
            5. Send request to create AD
            6. Send request to create IIS
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        self.create_IIS(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        self.create_aspnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        resp, serv3 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 3)

        self.create_IIS(env['id'], sess['id'], serv3['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 4)

    @attr(type='positive')
    def test_alternate_service_create3(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm
            4. Send request to create SQL cluster
            5. Send request to create SQL
            6. Send request to create AD
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        self.create_aspnet_farm(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        self.create_SQL_cluster(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 3)

        self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 4)

    @attr(type='positive')
    def test_alternate_service_create4(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create AD
            5. Send request to create SQL
            6. Send request to create SQL cluster
            7. Send request to create aspnet farm
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        self.create_IIS(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        resp, serv2 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.create_SQL(env['id'], sess['id'], serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 3)

        self.create_SQL_cluster(env['id'], sess['id'], serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 4)

        self.create_aspnet_farm(env['id'], sess['id'], serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 5)

    @attr(type='positive')
    def test_alternate_service_create5(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet
            4. Send request to create IIS
            5. Send request to delete aspnet
            6. Send request to create AD
            7. Send request to delete IIS
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_aspnet(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        resp, serv2 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.delete_service(env['id'], sess['id'], serv1['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.delete_service(env['id'], sess['id'], serv2['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

    @attr(type='positive')
    def test_alternate_service_create6(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create SQL cluster
            4. Send request to create SQL cluster
            5. Send request to create SQL cluster
            6. Send request to create SQL cluster
            7. Send request to create SQL cluster
            8. Send request to create IIS
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        for i in xrange(5):
            self.create_SQL_cluster(env['id'], sess['id'])
            resp, infa = self.get_list_services(env['id'], sess['id'])

            self.assertEqual(len(infa), i + 1)

        self.create_IIS(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 6)

    @attr(type='positive')
    def test_alternate_service_create7(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet
            4. Send request to create SQL
            5. Send request to create IIS
            6. Send request to create SQL
            7. Send request to create aspnet
            8. Send request to create IIS
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        self.create_aspnet(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 3)

        self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 4)

        self.create_aspnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 5)

        self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 6)

    @attr(type='positive')
    def test_alternate_service_create8(self):
        """
        Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create SQL
            5. Send request to create aspnet farm
            6. Send request to delete IIS
            7. Send request to create IIS
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 1)

        self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.create_aspnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 3)

        self.delete_service(env['id'], sess['id'], serv1['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 2)

        self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(len(infa), 3)

    @attr(type='negative')
    def test_double_delete_service(self):
        """
        Try to double delete service
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to delete IIS
            5. Send request to delete IIS
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])

        self.delete_service(env['id'], sess['id'], serv1['id'])

        self.assertRaises(Exception,
                          self.delete_service,
                          env['id'],
                          sess['id'],
                          serv1['id'])

    @attr(type='smoke')
    def test_get_list_services_of_empty_environment(self):
        """
        Gel list of services of empty environment
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to get list of services
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])

        resp, infa = self.get_list_services(env['id'], sess['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(len(infa), 0)
