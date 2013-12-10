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

import time

from tempest.api.murano import base
from tempest.test import attr


class SanityMuranoTest(base.MuranoTest):

    @attr(type='positive')
    def test_create_and_deploying_linux_telnet(self):
        """
        Create and deploy Linux telnet
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to create session
        3. Send request to add linux telnet
        4. Send request to deploy linux telnet
        5. Send request to get info for check deployment status
        6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_linux_telnet(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    def test_create_and_deploying_linux_apache(self):
        """
        Create and deploy Linux apache
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to create session
        3. Send request to add linux apache
        4. Send request to deploy linux apache
        5. Send request to get info for check deployment status
        6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_linux_apache(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    def test_create_and_deploying_demo_service(self):
        """
        Create and deploy demo service
        Target component: Murano

        Scenario:
        1. Send request to create environment
        2. Send request to create session
        3. Send request to add demo service
        4. Send request to deploy demo service
        5. Send request to get info for check deployment status
        6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_demo_service(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_ad(self):
        """
        Create and deploy AD
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to deploy AD
            5. Send request to get info for check deloyment status
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert (k > 7 and k <= 120)
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        inst_id_list = self.search_instances(env['id'], 'ad')
        for i in inst_id_list:
            self.inst_wth_fl_ip.append(i)
            ip = self.add_floating_ip(i)
            time.sleep(5)
            assert self.socket_check(ip, 3389) == 0
            self.remove_floating_ip(i)
            self.inst_wth_fl_ip.pop(self.inst_wth_fl_ip.index(i))
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_iis(self):
        """
        Create and deploy IIS
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS
            4. Send request to deploy IIS
            5. Send request to get info for check deloyment status
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_IIS(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert (k > 7 and k <= 120)
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        inst_id_list = self.search_instances(env['id'], 'iis')
        for i in inst_id_list:
            self.inst_wth_fl_ip.append(i)
            ip = self.add_floating_ip(i)
            time.sleep(5)
            assert self.socket_check(ip, 80) == 0
            assert self.socket_check(ip, 3389) == 0
            self.remove_floating_ip(i)
            self.inst_wth_fl_ip.pop(self.inst_wth_fl_ip.index(i))
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_apsnet(self):
        """
        Create and deploy apsnet
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add apsnet
            4. Send request to deploy apsnet
            5. Send request to get info for check deloyment status
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_apsnet(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert (k > 7 and k <= 120)
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        inst_id_list = self.search_instances(env['id'], 'asp')
        for i in inst_id_list:
            self.inst_wth_fl_ip.append(i)
            ip = self.add_floating_ip(i)
            time.sleep(5)
            assert self.socket_check(ip, 80) == 0
            assert self.socket_check(ip, 3389) == 0
            self.remove_floating_ip(i)
            self.inst_wth_fl_ip.pop(self.inst_wth_fl_ip.index(i))
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_iis_farm(self):
        """
        Create and deploy IIS farm
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add IIS farm
            4. Send request to deploy IIS farm
            5. Send request to get info for check deloyment status
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_IIS_farm(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert (k > 7 and k <= 120)
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_apsnet_farm(self):
        """
        Create and deploy apsnet farm
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add apsnet farm
            4. Send request to deploy apsnet farm
            5. Send request to get info for check deloyment status
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_apsnet_farm(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert (k > 7 and k <= 120)
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_sql(self):
        """
        Create and deploy SQL
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add SQL
            4. Send request to deploy SQL
            5. Send request to get info for check deloyment status
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_SQL(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert (k > 7 and k <= 120)
        resp, envo = self.get_deployments_list(env['id'])
        assert envo['deployments'][0]['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        inst_id_list = self.search_instances(env['id'], 'sql')
        for i in inst_id_list:
            self.inst_wth_fl_ip.append(i)
            ip = self.add_floating_ip(i)
            time.sleep(5)
            assert self.socket_check(ip, 1433) == 0
            assert self.socket_check(ip, 3389) == 0
            self.remove_floating_ip(i)
            self.inst_wth_fl_ip.pop(self.inst_wth_fl_ip.index(i))
        self.delete_environment(env['id'])

    @attr(type='positive')
    def test_create_and_deploying_sql_cluster(self):
        """
        Create and deploy SQL cluster
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to add AD
            4. Send request to add SQL cluster
            5. Send request to deploy session
            6. Send request to get info for check deloyment status
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        self.create_SQL_cluster(env['id'], sess['id'], serv['domain'])
        self.deploy_session(env['id'], sess['id'])
        self.get_session_info(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 180:
                break
        assert (k > 7 and k <= 180)
        resp, envo = self.get_deployments_list(env['id'])
        for i in envo['deployments']:
            assert i['state'] == 'success'
        self.get_deployment_info(env['id'], envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_get_deployments_list_wo_env_id(self):
        """
        Try to get deployments list without env id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to get deployments list using uncorrect
               environment id
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        self.create_session(env['id'])
        self.assertRaises(Exception, self.get_deployments_list, None)
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_create_service_after_begin_of_deploy(self):
        """
        Try to create service after begin of deploy
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to deploy session
            5. Send request to create IIS
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.assertRaises(Exception, self.create_IIS, env['id'], sess['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_delete_service_after_begin_of_deploy(self):
        """
        Try to delete service after begin of deploy
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to deploy session
            5. Send request to delete AD
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        resp, serv = self.create_AD(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        self.assertRaises(Exception, self.delete_service, env['id'],
                          sess['id'], serv['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_deploy_after_delete_environment(self):
        """
        Try to deploy session after deleting environment
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to delete environment
            5. Send request to deploy session
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.delete_environment(env['id'])
        self.assertRaises(Exception, self.deploy_session, env['id'],
                          sess['id'])

    @attr(type='negative')
    def test_deploy_after_delete_session(self):
        """
        Try to deploy session after deleting this session
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to delete session
            5. Send request to deploy session
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.delete_session(env['id'], sess['id'])
        self.assertRaises(Exception, self.deploy_session, env['id'], "")
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_deploy_empty_environment(self):
        """
        Deploy empty environment
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to deploy session
            4. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.deploy_session(env['id'], sess['id'])
        env.update({'status': None})
        k = 0
        while env['status'] != "ready":
            time.sleep(15)
            k += 1
            resp, env = self.get_environment_by_id(env['id'])
            if 'status' not in env:
                env.update({'status': None})
            if k > 120:
                break
        assert k < 8
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_deploy_second_session_after_first(self):
        """
        Try to deploy second session after begin of deploy first session
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session1
            3. Send request to create session2
            4. Send request to deploy session1
            5. Send request to deploy session2
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess1 = self.create_session(env['id'])
        resp, sess2 = self.create_session(env['id'])
        self.deploy_session(env['id'], sess1['id'])
        self.assertRaises(Exception, self.deploy_session, env['id'],
                          sess2['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_deploy_second_session_after_first_with_add_service(self):
        """
        Try to deploy session after deleting this session
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session1
            3. Send request to create session2
            4. Send request to deploy session1
            5. Send request to create AD
            6. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess1 = self.create_session(env['id'])
        resp, sess2 = self.create_session(env['id'])
        self.deploy_session(env['id'], sess1['id'])
        self.assertRaises(Exception, self.create_AD, env['id'], sess2['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_deploy_session_wo_env_id(self):
        """
        Try to deploy session without environment id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to deploy session using wrong environment id
            5. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.assertRaises(Exception, self.deploy_session, None,
                          sess['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_get_deployment_info_wo_env_id(self):
        """
        Try to get deployment info without environment id
        Target component: Murano

        Scenario:
            1. Send request to create environment
            2. Send request to create session
            3. Send request to create AD
            4. Send request to deploy session
            5. Send request to get deployments list
            6. Send request to get deployment info using wrong environment id
            7. Send request to delete environment
        """
        resp, env = self.create_environment('test')
        resp, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.deploy_session(env['id'], sess['id'])
        time.sleep(5)
        resp, envo = self.get_deployments_list(env['id'])
        self.assertRaises(Exception, self.get_deployment_info,
                          None, envo['deployments'][0]['id'])
        self.delete_environment(env['id'])

    @attr(type='negative')
    def test_deploy_service_wo_session_id(self):
        _, env = self.create_environment('test')
        _, sess = self.create_session(env['id'])
        self.create_AD(env['id'], sess['id'])
        self.assertRaises(Exception, self.deploy_session, env['id'], None)
        self.delete_environment(env['id'])