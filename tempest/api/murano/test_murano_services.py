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

class SanityMuranoTest(base.MuranoTest):

    @attr(type='smoke')
    def test_create_and_delete_AD(self):
        """ Create and delete AD
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to remove AD
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_AD_wo_env_id(self):
        """ Try create AD without env_id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD using wrong env_id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_AD,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_AD_wo_sess_id(self):
        """ Try to create AD without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD using uncorrect session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_AD,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_AD_wo_env_id(self):
        """ Try to delete AD without environment id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to remove AD using uncorrect environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_AD_wo_session_id(self):
        """ Try to delete AD without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to remove AD using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_IIS(self):
        """ Create and delete IIS
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS
            4. Send request to remove IIS
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_IIS_wo_env_id(self):
        """ Try to create IIS without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_IIS,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_IIS_wo_sess_id(self):
        """ Try to create IIS without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_IIS,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_IIS_wo_env_id(self):
        """ Try to delete IIS without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS
            4. Send request to delete IIS using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_IIS_wo_session_id(self):
        """ Try to delete IIS without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS
            4. Send request to delete IIS using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_apsnet(self):
        """ Create and delete apsnet
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add apsnet
            4. Send request to remove apsnet
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_apsnet_wo_env_id(self):
        """ Try to create aspnet without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_apsnet,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_apsnet_wo_sess_id(self):
        """ Try to create aspnet without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_apsnet,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_apsnet_wo_env_id(self):
        """ Try to delete aspnet without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet
            4. Send request to delete aspnet using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_apsnet_wo_session_id(self):
        """ Try to delete aspnet without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet
            4. Send request to delete aspnet using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_IIS_farm(self):
        """ Create and delete IIS farm
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm
            4. Send request to remove IIS farm
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS_farm(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_IIS_farm_wo_env_id(self):
        """ Try to create IIS farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_IIS_farm,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_IIS_farm_wo_sess_id(self):
        """ Try to create IIS farm without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS farm using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_IIS_farm,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_IIS_farm_wo_env_id(self):
        """ Try to delete IIS farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm
            4. Send request to delete IIS farm using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_IIS_farm_wo_session_id(self):
        """ Try to delete IIS farm without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm
            4. Send request to delete IIS farm using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_IIS_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_apsnet_farm(self):
        """ Create and delete apsnet farm
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add apsnet farm
            4. Send request to remove apsnet farm
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet_farm(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_apsnet_farm_wo_env_id(self):
        """ Try to create aspnet farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_apsnet_farm,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_apsnet_farm_wo_sess_id(self):
        """ Try to create aspnet farm without sess id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_apsnet_farm,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_apsnet_farm_wo_env_id(self):
        """ Try to delete aspnet farm without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet farm
            4. Send request to delete aspnet farm using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_apsnet_farm_wo_session_id(self):
        """ Try to delete aspnet farm without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add aspnet farm
            4. Send request to delete aspnet farm using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_apsnet_farm(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_SQL(self):
        """ Create and delete SQL
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to remove SQL
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_SQL_wo_env_id(self):
        """ Try to create SQL without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create SQL using wrong environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_SQL,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_SQL_wo_sess_id(self):
        """ Try to create SQL without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create SQL using wrong session id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_SQL,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_SQL_wo_env_id(self):
        """ Try to delete SQL without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to delete SQL using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_SQL_wo_session_id(self):
        """ Try to delete SQL without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to delete SQL using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_SQL_cluster(self):
        """ Create and delete SQL
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to delete SQL
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_SQL_cluster(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_create_and_delete_linux_agent(self):
        """ Create and delete Linux Agent
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent
            4. Send request to delete linux agent
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_linux_agent(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip('Bug https://bugs.launchpad.net/murano/+bug/1227154')
    @attr(type='negative')
    def test_create_linux_agent_wo_env_id(self):
        """ Try create Linux Agent without env_id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent using wrong env_id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_linux_agent,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_create_linux_agent_wo_sess_id(self):
        """ Try to create Linux Agent without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent using uncorrect session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        self.assertRaises(Exception, self.create_linux_agent,
                          env['id'], "")
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Bug https://bugs.launchpad.net/murano/+bug/1227154")
    @attr(type='negative')
    def test_delete_linux_agent_wo_env_id(self):
        """ Try to delete Linux Agent without environment id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent
            4. Send request to remove linux agent using uncorrect
               environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_linux_agent(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          None, sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_delete_linux_agent_wo_session_id(self):
        """ Try to delete linux agent without session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add linux agent
            4. Send request to remove linux agent using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_linux_agent(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service,
                          env['id'], "", serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_get_list_services(self):
        """ Get a list of services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get list of services
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, somelist = self.get_list_services(env['id'], sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_wo_env_id(self):
        """ Try to get services list withoun env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get services list using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        self.assertRaises(Exception, self.get_list_services,
                          None, sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_wo_sess_id(self):
        """ Try to get services list withoun session id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to get services list using wrong session id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, somelist = self.get_list_services(env['id'], "")
        assert somelist == []
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_after_delete_env(self):
        """ Try to get services list after deleting env
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
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp = self.delete_environment(env['id'])
        self.assertRaises(Exception, self.get_list_services,
                          env['id'], sess['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_get_list_of_services_after_delete_session(self):
        """ Try to get services list after deleting session
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to delete session
            5. Send request to get services list
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp = self.delete_session(env['id'], sess['id'])
        self.assertRaises(Exception, self.get_list_services,
                          env['id'], sess['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @testtools.skip("Service is not yet able to do it")
    @attr(type='smoke')
    def test_update_service(self):
        """ Update service
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to update service
            5. Send request to remove AD
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, updt = self.update_service(env['id'], sess['id'], serv['id'],
                                         serv)
        resp = self.delete_service(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='smoke')
    def test_get_service_info(self):
        """ Get service detailed info
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to get detailed info about service
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        resp, serv = self.get_service_info(env['id'], sess['id'], serv['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create1(self):
        """ Check alternate creating and deleting services
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
            15. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess1 = self.create_session(env['id'])
        resp, sess2 = self.create_session(env['id'])
        resp, sess3 = self.create_session(env['id'])
        resp, serv1 = self.create_AD(env['id'], sess1['id'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_IIS(env['id'], sess1['id'], serv1['domain'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_SQL(env['id'], sess1['id'], serv1['domain'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 3
        resp, serv31 = self.create_IIS(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 1
        resp, serv32 = self.create_apsnet_farm(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 2
        resp, serv33 = self.create_AD(env['id'], sess3['id'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 3
        resp, serv34 = self.create_IIS_farm(env['id'], sess3['id'],
                                            serv33['domain'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 4
        resp, serv35 = self.create_SQL_cluster(env['id'], sess3['id'],
                                       serv33['domain'])
        resp, infa = self.get_list_services(env['id'], sess3['id'])
        assert len(infa) == 5
        resp = self.delete_service(env['id'], sess1['id'], serv2['id'])
        resp, infa = self.get_list_services(env['id'], sess1['id'])
        assert len(infa) == 2
        resp, serv21 = self.create_IIS(env['id'], sess2['id'])
        resp, infa = self.get_list_services(env['id'], sess2['id'])
        assert len(infa) == 1
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create2(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create aspnet farm
            5. Send request to create AD
            6. Send request to create IIS
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_apsnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_IIS(env['id'], sess['id'], serv3['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create3(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet farm
            4. Send request to create SQL cluster
            5. Send request to create SQL
            6. Send request to create AD
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_apsnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_SQL_cluster(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create4(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create AD
            5. Send request to create SQL
            6. Send request to create SQL cluster
            7. Send request to create aspnet farm
            8. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_SQL(env['id'], sess['id'], serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_SQL_cluster(env['id'], sess['id'],
                                      serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp, serv5 = self.create_apsnet_farm(env['id'], sess['id'],
                                              serv2['domain'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 5
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create5(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create aspnet
            4. Send request to create IIS
            5. Send request to delete aspnet
            6. Send request to create AD
            7. Send request to delete IIS
            8. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_apsnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp = self.delete_service(env['id'], sess['id'], serv1['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv1 = self.create_AD(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp = self.delete_service(env['id'], sess['id'], serv2['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create6(self):
        """ Check alternate creating and deleting services
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
            9. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        for i in xrange(5):
            resp, serv1 = self.create_SQL_cluster(env['id'], sess['id'])
            resp, infa = self.get_list_services(env['id'], sess['id'])
            assert len(infa) == i + 1
        resp, serv2 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 6
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create7(self):
        """ Check alternate creating and deleting services
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
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_apsnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp, serv4 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 4
        resp, serv5 = self.create_apsnet(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 5
        resp, serv6 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 6
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='positive')
    def test_alternate_service_create8(self):
        """ Check alternate creating and deleting services
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to create SQL
            5. Send request to create aspnet farm
            6. Send request to delete IIS
            7. Send request to create IIS
            8. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)                     
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 1
        resp, serv2 = self.create_SQL(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv3 = self.create_apsnet_farm(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp = self.delete_service(env['id'], sess['id'], serv1['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 2
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp, infa = self.get_list_services(env['id'], sess['id'])
        assert len(infa) == 3
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))

    @attr(type='negative')
    def test_double_delete_service(self):
        """ Try to double delete service
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create IIS
            4. Send request to delete IIS
            5. Send request to delete IIS
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.environments.append(env)
        resp, sess = self.create_session(env['id'])
        resp, serv1 = self.create_IIS(env['id'], sess['id'])
        resp = self.delete_service(env['id'], sess['id'], serv1['id'])
        self.assertRaises(Exception, self.delete_service, env['id'],
                          sess['id'], serv1['id'])
        resp = self.delete_environment(env['id'])
        self.environments.pop(self.environments.index(env))
