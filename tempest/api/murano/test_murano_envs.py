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

from tempest.api.murano import base
from tempest.test import attr
from tempest import exceptions


class SanityMuranoTest(base.MuranoTest):

    @attr(type='smoke')
    def test_create_and_delete_environment(self):
        """
        Create and delete environment
        Test create environment, after that test try to get
        environment's info, using environment's id,
        and finally delete this environment
        Target component: Murano

        Scenario:
            1. Send request to create environment.
            2. Send request to get environment
            3. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        self.assertEqual(resp.status, 200)

        resp, infa = self.get_environment_by_id(env['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(infa['name'], 'test')

        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_get_environment(self):
        """
        Get environment by id
        Test create environment, after that test try to get
        environment's info, using environment's id,
        and finally delete this environment
        Target component: Murano

        Scenario:
            1. Send request to create environment.
            2. Send request to get environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, infa = self.get_environment_by_id(env['id'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(infa['name'], 'test')

    @attr(type='smoke')
    def test_get_list_environments(self):
        """
        Get list of existing environments
        Test create environment and try to get list of existing environments
        Target component: Murano

        Scenario:
        1. Create environment
        2. Send request to get list of environments
        """
        _, env1 = self.create_environment('test1')
        self.environments.append(env1)

        resp, infa = self.get_list_environments()

        self.assertEqual(resp.status, 200)
        self.assertEqual(len(infa['environments']), 1)

    @attr(type='smoke')
    def test_update_environment(self):
        """
        Update environment instance
        Test try to update environment instance
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to update environment instance
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, infa = self.update_environment(env['id'], env['name'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(infa['name'], 'test-changed')

    @attr(type='negative')
    def test_update_env_with_wrong_env_id(self):
        """
        Try to update environment using incorrect env_id
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to update environment instance(with incorrect env_id)
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        self.assertRaises(exceptions.NotFound,
                          self.update_environment,
                          None,
                          env['name'])

    @attr(type='smoke')
    def test_update_env_after_begin_of_deploy(self):
        """
        Try to update environment after begin of deploy
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to create session
        3. Send request to deploy session
        4. Send request to update environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        resp, sess = self.create_session(env['id'])
        self.deploy_session(env['id'], sess['id'])

        resp, infa = self.update_environment(env['id'], env['name'])

        self.assertEqual(resp.status, 200)
        self.assertEqual(infa['name'], 'test-changed')

    @attr(type='negative')
    def test_delete_env_by_incorrect_env_id(self):
        """
        Try to delete environment using incorrect env_id
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to delete environment(with incorrect env_id)
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        self.assertRaises(exceptions.NotFound,
                          self.delete_environment,
                          None)

    @attr(type='negative')
    def test_double_delete_environment(self):
        """
        Try to delete environment twice
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to delete environment
        3. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)

        self.delete_environment(env['id'])

        self.environments.pop(self.environments.index(env))
        self.assertRaises(exceptions.NotFound,
                          self.delete_environment,
                          env['id'])

    @attr(type='negative')
    def test_delete_env_and_get_env(self):
        """
        Try to get deleted environment
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to delete environment
        3. Send request to get deleted environment
        """
        _, env = self.create_environment('test')
        self.environments.append(env)
        self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

        self.assertRaises(exceptions.NotFound,
                          self.get_environment_by_id,
                          env['id'])

    @attr(type='negative')
    def test_get_environment_wo_env_id(self):
        """
        Try to get environment by incorrect env_id
        Target component: Murano

        Scenario:
        1. Send request to get environment using incorrect environment id
        """
        self.assertRaises(exceptions.NotFound,
                          self.get_environment_by_id,
                          None)