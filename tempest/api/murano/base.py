# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Mirantis, Inc.
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

import json
import socket
import requests
import novaclient.v1_1.client as nvclient

from tempest.common import rest_client
from tempest import config
import tempest.test


class MuranoTest(tempest.test.BaseTestCase):

    def setUp(self):
        """
            This method allows to initialize authentication before
            each test case and define parameters of Murano API Service
            This method also create environment for all tests
        """

        super(MuranoTest, self).setUp()

        if not config.TempestConfig().service_available.murano:
            raise self.skipException("Murano tests is disabled")
        _config = config.TempestConfig()
        user = self.config.identity.admin_username
        password = self.config.identity.admin_password
        tenant = self.config.identity.admin_tenant_name
        auth_url = self.config.identity.uri
        client_args = (_config, user, password, auth_url, tenant)

        self.client = rest_client.RestClient(*client_args)
        self.client.service = 'identity'
        self.token = self.client.get_auth()
        self.client.base_url = self.config.murano.murano_url

        response, environment = self.create_environment('test455444')
        self.environments = [environment, ]
        self.inst_wth_fl_ip = []

    def tearDown(self):
        """
            This method allows to clean up after each test.
            The main task for this method - delete environment after
            PASSED and FAILED tests.
        """

        super(MuranoTest, self).tearDown()

        for environment in self.environments:
            try:
                self.delete_environment(environment['id'])
            except Exception:
                pass
        for inst in self.inst_wth_fl_ip:
            try:
                self.remove_floating_ip(inst)
            except Exception:
                pass

    def create_environment(self, name):
        """
            This method allows to create environment.

            Input parameters:
              name - Name of new environment

            Returns response and new environment.
        """

        post_body = '{"name": "%s"}' % name
        resp, body = self.client.post('environments', post_body,
                                      self.client.headers)

        return resp, json.loads(body)

    def delete_environment(self, environment_id):
        """
            This method allows to delete environment

            Input parameters:
              environment_id - ID of deleting environment
        """
        self.client.delete('environments/' + str(environment_id),
                           self.client.headers)

    def update_environment(self, environment_id, environment_name):
        """
            This method allows to update environment instance

            Input parameters:
              environment_id - ID of updating environment
              environment_name - name of updating environment
        """
        post_body = '{"name": "%s"}' % (environment_name + "-changed")
        resp, body = self.client.put('environments/' + str(environment_id),
                                     post_body, self.client.headers)
        return resp, json.loads(body)

    def get_list_environments(self):
        """
            This method allows to get a list of existing environments

            Returns response and list of environments
        """
        resp, body = self.client.get('environments',
                                     self.client.headers)
        return resp, json.loads(body)

    def get_environment_by_id(self, environment_id):
        """
            This method allows to get environment's info by id

            Input parameters:
              environment_id - ID of needed environment
            Returns response and environment's info
        """
        resp, body = self.client.get('environments/' + str(environment_id),
                                     self.client.headers)
        return resp, json.loads(body)

    def nova_auth(self):
        user = self.config.identity.admin_username
        password = self.config.identity.admin_password
        tenant = self.config.identity.admin_tenant_name
        auth_url = self.config.identity.uri
        nova = nvclient.Client(user, password, tenant, auth_url,
                               service_type="compute")
        return nova

    def search_instances(self, environment_id, hostname):
        nova = self.nova_auth()
        somelist = []
        for i in nova.servers.list():
            if ((str(environment_id) in str(
                    i.name)) and (str(hostname) in str(i.name))):
                somelist.append(i.id)
        return somelist

    def add_floating_ip(self, instance_id):
        nova = self.nova_auth()
        pool = nova.floating_ip_pools.list()[0].name
        ip = nova.floating_ips.create(pool)
        nova.servers.get(instance_id).add_floating_ip(ip)
        return ip.ip

    def remove_floating_ip(self, instance_id):
        nova = self.nova_auth()
        fl_ips = nova.floating_ips.findall(instance_id=instance_id)
        for fl_ip in fl_ips:
            nova.floating_ips.delete(fl_ip.id)
        return None

    def socket_check(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result

    def create_session(self, environment_id):
        """
            This method allow to create session

            Input parameters:
              environment_id - ID of environment
                   where session should be created
        """
        post_body = None
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/configure',
                                      post_body, self.client.headers)
        return resp, json.loads(body)

    def get_session_info(self, environment_id, session_id):
        """
            This method allow to get session's info

            Input parameters:
              environment_id - ID of environment
                             where needed session was created
              session_id - ID of needed session
            Return response and session's info
        """
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/sessions/' + str(session_id),
                                     self.client.headers)
        return resp, json.loads(body)

    def delete_session(self, environment_id, session_id):
        """
            This method allow to delete session

            Input parameters:
              environment_id - ID of environment
                             where needed session was created
              session_id - ID of needed session
        """
        self.client.delete('environments/' + str(environment_id) +
                           '/sessions/' + str(session_id), self.client.headers)

    def create_AD(self, environment_id, session_id):
        """
            This method allow to add AD

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        post_body = {"type": "activeDirectory", "name": "ad.local",
                     "adminPassword": "P@ssw0rd", "domain": "ad.local",
                     "availabilityZone": "nova",
                     "unitNamingPattern": "adinstance",
                     "flavor": "m1.medium", "osImage":
                     {"type": "ws-2012-std", "name": "ws-2012-std", "title":
                     "Windows Server 2012 Standard"}, "configuration":
                     "standalone", "units": [{"isMaster": True,
                     "recoveryPassword": "P@ssw0rd",
                     "location": "west-dc"}]}

        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_IIS(self, environment_id, session_id, domain_name=""):
        """
            This method allow to add IIS

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        iis_name = "someservice"
        creds = {'username': 'Administrator',
                 'password': 'P@ssw0rd'}
        post_body = {"type": "webServer", "domain": domain_name,
                     "availabilityZone": "nova", "name": iis_name,
                     "adminPassword": "P@ssw0rd",
                     "unitNamingPattern": "iisinstance",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "units": [{}], "credentials": creds,
                     "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_apsnet(self, environment_id, session_id, domain_name=""):
        """
            This method allow to add apsnet

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        creds = {'username': 'Administrator',
                 'password': 'P@ssw0rd'}
        post_body = {"type": "aspNetApp", "domain": domain_name,
                     "availabilityZone": "nova",
                     "name": "someasp", "repository":
                     "git://github.com/Mirantis/murano-mvc-demo.git",
                     "adminPassword": "P@ssw0rd",
                     "unitNamingPattern": "aspnetinstance",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "units": [{}], "credentials": creds,
                     "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_IIS_farm(self, environment_id, session_id, domain_name=""):
        """
            This method allow to add IIS farm

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        creds = {'username': 'Administrator', 'password': 'P@ssw0rd'}
        post_body = {"type": "webServerFarm", "domain": domain_name,
                     "availabilityZone": "nova", "name": "someIISFARM",
                     "adminPassword": "P@ssw0rd", "loadBalancerPort": 80,
                     "unitNamingPattern": "",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "units": [{}, {}],
                     "credentials": creds, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_apsnet_farm(self, environment_id, session_id, domain_name=""):
        """
            This method allow to add apsnet farm

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        creds = {'username': 'Administrator', 'password': 'P@ssw0rd'}
        post_body = {"type": "aspNetAppFarm", "domain": domain_name,
                     "availabilityZone": "nova", "name": "SomeApsFarm",
                     "repository":
                             "git://github.com/Mirantis/murano-mvc-demo.git",
                     "adminPassword": "P@ssw0rd", "loadBalancerPort": 80,
                     "unitNamingPattern": "",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "units": [{}, {}],
                     "credentials": creds, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_SQL(self, environment_id, session_id, domain_name=""):
        """
            This method allow to add SQL

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        post_body = {"type": "msSqlServer", "domain": domain_name,
                     "availabilityZone": "nova", "name": "SQLSERVER",
                     "adminPassword": "P@ssw0rd",
                     "unitNamingPattern": "sqlinstance",
                     "saPassword": "P@ssw0rd", "mixedModeAuth": True,
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"}, "units": [{}],
                     "credentials": {"username": "Administrator",
                     "password": "P@ssw0rd"}, "flavor": "m1.medium"}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_SQL_cluster(self, environment_id, session_id, domain_name=""):
        """
            This method allow to add SQL cluster

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        AG = self.config.murano.agListnerIP
        clIP = self.config.murano.clusterIP
        post_body = {"domain": domain_name, "domainAdminPassword": "P@ssw0rd",
                     "externalAD": False,
                     "sqlServiceUserName": "Administrator",
                     "sqlServicePassword": "P@ssw0rd",
                     "osImage": {"type": "ws-2012-std", "name": "ws-2012-std",
                     "title": "Windows Server 2012 Standard"},
                     "agListenerName": "SomeSQL_AGListner",
                     "flavor": "m1.medium",
                     "agGroupName": "SomeSQL_AG",
                     "domainAdminUserName": "Administrator",
                     "agListenerIP": AG,
                     "clusterIP": clIP,
                     "type": "msSqlClusterServer", "availabilityZone": "nova",
                     "adminPassword": "P@ssw0rd",
                     "clusterName": "SomeSQL", "mixedModeAuth": True,
                     "unitNamingPattern": "", "units": [{"isMaster": True,
                     "name": "node1", "isSync": True}, {"isMaster": False,
                     "name": "node2", "isSync": True}],
                     "name": "Sqlname", "saPassword": "P@ssw0rd",
                     "databases": ['NewDB']}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def create_linux_agent(self, environment_id, session_id, domain_name=""):
        post_body = {'availabilityZone': 'nova', 'name': 'Linux_agent',
                     'deployTelnet': True, 'unitNamingPattern': '',
                     'osImage': {'type': 'linux',
                     'name': 'F18-x86_64-cfntools-MURANO',
                     'title': 'Linux with vNext agent'}, 'units': [{}],
                     'flavor': 'm1.medium', 'type': 'linuxTelnetService'}
        post_body = json.dumps(post_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.post('environments/' + str(environment_id) +
                                      '/services', post_body,
                                      self.client.headers)
        return resp, json.loads(body)

    def delete_service(self, environment_id, session_id, service_id):
        """
            This method allow to delete service

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
              service_id - ID of needed service
        """
        self.client.headers.update({'X-Configuration-Session': session_id})
        self.client.delete('environments/' + str(environment_id)
                           + '/services/' + str(service_id),
                           self.client.headers)

    def get_list_services(self, environment_id, session_id):
        """
            This method allow to get list of services

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/services',
                                     self.client.headers)
        return resp, json.loads(body)

    def get_service_info(self, environment_id, session_id, service_id):
        """
            This method allow to get detailed service info

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
              service_id - ID of needed service
        """
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/services/' + str(service_id),
                                     self.client.headers)
        return resp, json.loads(body)

    def update_service(self, environment_id, session_id, service_id, s_body):
        """
            This method allows to update service

            Input parameters:
              environment_id - env's id
              session_id - session_id where service is attach
              service_id - service id of updating service
              s_body - json obj
        """
        s_body['flavor'] = "m1.small"
        post_body = json.dumps(s_body)
        self.client.headers.update({'X-Configuration-Session': session_id})
        resp, body = self.client.put('environments/' + str(environment_id) +
                                     '/services/' + str(service_id),
                                     post_body, self.client.headers)
        return resp, json.loads(body)

    def deploy_session(self, environment_id, session_id):
        """
            This method allow to send environment on deploy

            Input parameters:
              environment_id - ID of current environment
              session_id - ID of current session
        """
        post_body = None
        resp = self.client.post('environments/' + str(environment_id) +
                                '/sessions/' + str(session_id) +
                                '/deploy', post_body, self.client.headers)
        return resp

    def get_deployments_list(self, environment_id):
        """
            This method allow to get list of deployments

            Input parameters:
              environment_id - ID of current environment
        """
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/deployments', self.client.headers)
        return resp, json.loads(body)

    def get_deployment_info(self, environment_id, deployment_id):
        """
            This method allow to get detailed info about deployment

            Input parameters:
              environment_id - ID of current environment
              deployment_id - ID of needed deployment
        """
        resp, body = self.client.get('environments/' + str(environment_id) +
                                     '/deployments/' + str(deployment_id),
                                     self.client.headers)
        return resp, json.loads(body)

class MuranoMeta(tempest.test.BaseTestCase):

    def setUp(self):

        super(MuranoMeta, self).setUp()
        if not config.TempestConfig().service_available.murano:
            raise self.skipException("Murano tests is disabled")
        _config = config.TempestConfig()
        user = self.config.identity.admin_username
        password = self.config.identity.admin_password
        tenant = self.config.identity.admin_tenant_name
        auth_url = self.config.identity.uri
        client_args = (_config, user, password, auth_url, tenant)
        self.client = rest_client.RestClient(*client_args)
        self.client.service = 'identity'
        self.token = self.client.get_auth()
        self.client.base_url = self.config.murano.murano_metadata

    def get_ui_definitions(self):
        resp, body = self.client.get('v1/client/ui', self.client.headers)
        return resp, body

    def get_conductor_metadata(self):
        resp, body = self.client.get('v1/client/conductor', self.client.headers)
        return resp, body

    def get_list_metadata_objects(self, path):
        resp, body = self.client.get('v1/admin/' + path, self.client.headers)
        return resp, body

    def get_metadata_object(self, object):
        resp, body = self.client.get('v1/admin/' + object, self.client.headers)
        return resp, body

    def upload_metadata_object(self, object, path):
        files = {'file': open(object, 'rb')}
        headers = {'X-Auth-Token': self.token}
        resp = requests.post('http://172.18.78.92:8084/v1/admin/%s' %path,
                             files=files,
                             headers=headers)
        return resp

    def create_directory(self, path, name):
        post_body = '{}'
        resp, body = self.client.put('v1/admin/' + path + name, post_body,
                                      self.client.headers)
        return resp, body

    def delete_metadata_obj_or_folder(self, object):
        resp, body = self.client.delete('v1/admin/' + object,
                                        self.client.headers)
        return resp, body
