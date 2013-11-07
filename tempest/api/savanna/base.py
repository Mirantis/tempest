# Copyright (c) 2013 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import paramiko
import six
import socket
import telnetlib
import time
import uuid

import savannaclient.api.client as savanna_client

from tempest import clients
from tempest.openstack.common import excutils
import tempest.test


def skip_test(config_name, message=''):

    def handle(func):

        def call(self, *args, **kwargs):

            if getattr(self, config_name):

                print(
                    '\n======================================================='
                )
                print('INFO: ' + message)
                print(
                    '=======================================================\n'
                )

            else:

                return func(self, *args, **kwargs)

        return call

    return handle

_ssh = None


def _connect(host, username, private_key):
    global _ssh

    if type(private_key) in [str, unicode]:
        private_key = paramiko.RSAKey(file_obj=six.StringIO(private_key))
    _ssh = paramiko.SSHClient()
    _ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    _ssh.connect(host, username=username, pkey=private_key)


def _cleanup():
    global _ssh
    _ssh.close()


def _read_paramimko_stream(recv_func):
    result = ''
    buf = recv_func(1024)
    while buf != '':
        result += buf
        buf = recv_func(1024)

    return result


def _execute_command(cmd, get_stderr=False, raise_when_error=True):
    global _ssh

    chan = _ssh.get_transport().open_session()
    chan.exec_command(cmd)

    stdout = _read_paramimko_stream(chan.recv)
    stderr = _read_paramimko_stream(chan.recv_stderr)

    ret_code = chan.recv_exit_status()

    if ret_code and raise_when_error:
        raise RemoteCommandException(cmd=cmd, ret_code=ret_code,
                                     stdout=stdout, stderr=stderr)

    if get_stderr:
        return ret_code, stdout, stderr
    else:
        return ret_code, stdout


def _write_file(sftp, remote_file, data):
    fl = sftp.file(remote_file, 'w')
    fl.write(data)
    fl.close()


def _write_file_to(remote_file, data):
    global _ssh

    _write_file(_ssh.open_sftp(), remote_file, data)


def _read_file_from(remote_file):
    global _ssh

    fl = _ssh.open_sftp().file(remote_file, 'r')
    data = fl.read()
    fl.close()
    return data


class RemoteCommandException(Exception):
    message = "Error during command execution: \"%s\""

    def __init__(self, cmd, ret_code=None, stdout=None,
                 stderr=None):
        self.code = "REMOTE_COMMAND_FAILED"

        self.cmd = cmd
        self.ret_code = ret_code
        self.stdout = stdout
        self.stderr = stderr

        self.message = self.message % cmd

        if ret_code:
            self.message += '\nReturn code: ' + str(ret_code)

        if stderr:
            self.message += '\nSTDERR:\n' + stderr

        if stdout:
            self.message += '\nSTDOUT:\n' + stdout


class BaseSavannaTest(tempest.test.BaseTestCase):

    def setUp(self):

        super(BaseSavannaTest, self).setUp()

        if not self.config.service_available.savanna:

            skip_msg = ("%s skipped as nova is not available" % self.__name__)

            raise self.skipException(skip_msg)

        os = clients.AdminManager()

        self.flavors_client = os.flavors_client
        self.keypairs_client = os.keypairs_client
        self.container_client = os.container_client
        self.object_client = os.object_client
        self.images_client = os.images_client

        resp, images = self.images_client.list_images_with_detail()

        self.config.savanna_vanilla.image_id = None
        self.config.savanna_hdp.image_id = None
        vanilla_skip = self.config.savanna_vanilla.skip_all_tests_for_plugin
        hdp_skip = self.config.savanna_hdp.skip_all_tests_for_plugin

        for image in images:

            try:
                if image['metadata']['_savanna_username']:

                    if not vanilla_skip:

                        try:

                            if image['metadata']['_savanna_tag_vanilla']:

                                self.config.savanna_vanilla.image_id = \
                                    image['id']
                                self.config.savanna_vanilla.image_user = \
                                    image['metadata']['_savanna_username']
                        except KeyError:
                            pass

                    if not hdp_skip:

                        try:

                            if image['metadata']['_savanna_tag_hdp']:

                                self.config.savanna_hdp.image_id = image['id']
                                self.config.savanna_hdp.image_user = \
                                    image['metadata']['_savanna_username']

                        except KeyError:
                            pass

            except KeyError:
                pass

        if not hdp_skip and not self.config.savanna_hdp.image_id:
            self.fail("""
            ***********************************************
            Integration tests for HDP plugin is Enabled
            but Image for this plugin not found.
            Please check that the image is registered
            and all necessary tags are added.
            ***********************************************
            """)

        if not vanilla_skip and not self.config.savanna_vanilla.image_id:
            self.fail("""
            ***********************************************
            Integration tests for Vanilla plugin is Enabled
            but Image for this plugin not found.
            Please check that the image is registered
            and all necessary tags are added.
            ***********************************************
            """)

        savanna_host = self.config.savanna_common.savanna_host
        savanna_port = self.config.savanna_common.savanna_port

        telnetlib.Telnet(savanna_host, savanna_port)

        self.savanna = savanna_client.Client(
            username=os.username,
            api_key=os.password,
            project_name=os.tenant_name,
            auth_url=self.config.identity.uri,
            savanna_url='http://%s:%s/%s' % (
                savanna_host, savanna_port,
                self.config.savanna_common.savanna_api_version))

        resp, self.flavor = self.flavors_client.create_flavor(
            'tempest-savanna-flavor-%s' % str(uuid.uuid4())[:30], 1024, 1, 10,
            str(uuid.uuid4()), ephemeral=10)

        resp, self.ssh_key = self.keypairs_client.create_keypair(
            'tempest-savanna-ssh-' + str(uuid.uuid4())[:8])

        # This condition checks Swift's efficiency,
        # if at least one of the plugins included Swift test

        if not self.config.savanna_vanilla.skip_swift_test or not\
            self.config.savanna_hdp.skip_swift_test or not \
                self.config.savanna_vanilla.skip_edp_test:
            self.container_name = \
                'tempest-savanna-container-%s' % str(uuid.uuid4())[:8]

            resp, body = self.container_client.create_container(
                self.container_name)

            self.container_client.delete_container(self.container_name)

            if resp.status != 201:

                self.fail("""
                ***********************************************
                Swift is not work,
                please check swift's efficiency
                or off savanna swit test in all plugins
                ***********************************************
                """)

#-------------------------Methods for object creation--------------------------

    def create_node_group_template(self, name, plugin_config, description,
                                   volumes_per_node, volume_size,
                                   node_processes, node_configs,
                                   floating_ip_pool=None, hadoop_version=None):

        if not hadoop_version:

            hadoop_version = plugin_config.hadoop_version

        data = self.savanna.node_group_templates.create(
            name, plugin_config.plugin_name, hadoop_version, self.flavor['id'],
            description, volumes_per_node, volume_size, node_processes,
            node_configs, floating_ip_pool)

        node_group_template_id = data.id

        return node_group_template_id

    def create_cluster_template(self, name, plugin_config, description,
                                cluster_configs, node_groups,
                                anti_affinity=None, net_id=None):

        data = self.savanna.cluster_templates.create(
            name, plugin_config.plugin_name, plugin_config.hadoop_version,
            description, cluster_configs, node_groups, anti_affinity, net_id)

        cluster_template_id = data.id

        return cluster_template_id

    def create_cluster_and_get_info(self, plugin_config, cluster_template_id,
                                    description, cluster_configs,
                                    node_groups=None, anti_affinity=None,
                                    net_id=None, hadoop_version=None,
                                    image_id=None, is_transient=False):

        if not hadoop_version:

            hadoop_version = plugin_config.hadoop_version

        if not image_id:

            image_id = plugin_config.image_id

        self.cluster_id = None

        data = self.savanna.clusters.create(
            'savanna-cluster-' + str(uuid.uuid4())[:8],
            plugin_config.plugin_name, hadoop_version, cluster_template_id,
            image_id, is_transient, description, cluster_configs, node_groups,
            self.ssh_key['name'], anti_affinity, net_id)

        self.cluster_id = data.id

        self.poll_cluster_state(self.cluster_id)

        node_ip_list_with_node_processes = \
            self.get_cluster_node_ip_list_with_node_processes(self.cluster_id)

        try:

            node_info = self.get_node_info(node_ip_list_with_node_processes,
                                           plugin_config)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(
                    '\nFailure during check of node process deployment '
                    'on cluster node: ' + str(e)
                )

        try:

            self.await_active_workers_for_namenode(node_info, plugin_config)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(
                    '\nFailure while active worker waiting for namenode: '
                    + str(e)
                )

        # For example: method "create_cluster_and_get_info" return
        # {
        #       'node_info': {
        #               'tasktracker_count': 3,
        #               'node_count': 6,
        #               'namenode_ip': '172.18.168.242',
        #               'datanode_count': 3
        #               },
        #       'cluster_id': 'bee5c6a1-411a-4e88-95fc-d1fbdff2bb9d',
        #       'node_ip_list': {
        #               '172.18.168.153': ['tasktracker', 'datanode'],
        #               '172.18.168.208': ['secondarynamenode', 'oozie'],
        #               '172.18.168.93': ['tasktracker'],
        #               '172.18.168.101': ['tasktracker', 'datanode'],
        #               '172.18.168.242': ['namenode', 'jobtracker'],
        #               '172.18.168.167': ['datanode']
        #       },
        #       'plugin_config': <oslo.config.cfg.GroupAttr object at 0x215d9d>
        # }

        return {
            'cluster_id': self.cluster_id,
            'node_ip_list': node_ip_list_with_node_processes,
            'node_info': node_info,
            'plugin_config': plugin_config
        }

#---------Helper methods for cluster info obtaining and its processing---------

    def poll_cluster_state(self, cluster_id):

        data = self.savanna.clusters.get(cluster_id)

        timeout = self.config.savanna_common.cluster_creation_timeout * 60
        while str(data.status) != 'Active':

            print('CLUSTER STATUS: ' + str(data.status))

            if str(data.status) == 'Error':

                print('\n' + str(data) + '\n')

                self.fail('Cluster state == \'Error\'.')

            if timeout <= 0:

                print('\n' + str(data) + '\n')

                self.fail(
                    'Cluster did not return to \'Active\' state '
                    'within %d minutes.'
                    % self.config.savanna_common.cluster_creation_timeout
                )

            data = self.savanna.clusters.get(cluster_id)
            time.sleep(10)
            timeout -= 10

        return str(data.status)

    def get_cluster_node_ip_list_with_node_processes(self, cluster_id):

        data = self.savanna.clusters.get(cluster_id)
        node_groups = data.node_groups

        node_ip_list_with_node_processes = {}
        for node_group in node_groups:

            instances = node_group['instances']
            for instance in instances:

                node_ip = instance['management_ip']
                node_ip_list_with_node_processes[node_ip] = node_group[
                    'node_processes']

        # For example:
        # node_ip_list_with_node_processes = {
        #       '172.18.168.181': ['tasktracker'],
        #       '172.18.168.94': ['secondarynamenode'],
        #       '172.18.168.208': ['namenode', 'jobtracker'],
        #       '172.18.168.93': ['tasktracker', 'datanode'],
        #       '172.18.168.44': ['tasktracker', 'datanode'],
        #       '172.18.168.233': ['datanode']
        # }

        return node_ip_list_with_node_processes

    def try_telnet(self, host, port):

        try:

            telnetlib.Telnet(host, port)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(
                    '\nTelnet has failed: ' + str(e) +
                    '  NODE IP: %s, PORT: %s. Passed %s minute(s).'
                    % (host, port, self.config.savanna_common.telnet_timeout)
                )

    def get_node_info(self, node_ip_list_with_node_processes, plugin_config):

        tasktracker_count = 0
        datanode_count = 0
        node_count = 0

        for node_ip, processes in node_ip_list_with_node_processes.items():

            self.try_telnet(node_ip, '22')
            node_count += 1

            for process in processes:

                if process in plugin_config.hadoop_processes_with_ports:

                    timeout = self.config.savanna_common.telnet_timeout
                    for i in range(timeout * 60):

                        try:

                            time.sleep(1)
                            telnetlib.Telnet(
                                node_ip,
                                plugin_config.hadoop_processes_with_ports[
                                    process]
                            )

                            break

                        except socket.error:

                            print(
                                'Connection attempt. NODE PROCESS: %s, '
                                'PORT: %s.'
                                % (process,
                                   plugin_config.hadoop_processes_with_ports[
                                       process])
                            )

                    else:

                        self.try_telnet(
                            node_ip,
                            plugin_config.hadoop_processes_with_ports[process]
                        )

            if plugin_config.process_names['tt'] in processes:

                tasktracker_count += 1

            if plugin_config.process_names['dn'] in processes:

                datanode_count += 1

            if plugin_config.process_names['nn'] in processes:

                namenode_ip = node_ip

        return {
            'namenode_ip': namenode_ip,
            'tasktracker_count': tasktracker_count,
            'datanode_count': datanode_count,
            'node_count': node_count
        }

    def await_active_workers_for_namenode(self, node_info, plugin_config):

        self.open_ssh_connection(
            node_info['namenode_ip'], plugin_config.image_user
        )

        timeout = self.config.savanna_common.HDFS_initialization_timeout

        for i in range(timeout * 6):

            time.sleep(10)

            active_tasktracker_count = self.execute_command(
                'sudo su -c "hadoop job -list-active-trackers" %s'
                % plugin_config.hadoop_user)[1]

            active_datanode_count = int(
                self.execute_command(
                    'sudo su -c "hadoop dfsadmin -report" %s \
                    | grep "Datanodes available:.*" | awk \'{print $3}\''
                    % plugin_config.hadoop_user)[1]
            )

            if not active_tasktracker_count:

                active_tasktracker_count = 0

            else:

                active_tasktracker_count = len(
                    active_tasktracker_count[:-1].split('\n'))

            if (
                    active_tasktracker_count == node_info['tasktracker_count']
            ) and (
                    active_datanode_count == node_info['datanode_count']
            ):

                break

        else:

            self.fail(
                'Tasktracker or datanode cannot be started within '
                '%s minute(s) for namenode.'
                % self.config.savanna_common.HDFS_initialization_timeout
            )

        self.close_ssh_connection()

#---------------------------------Remote---------------------------------------

    def open_ssh_connection(self, host, node_username):

        _connect(host, node_username, self.ssh_key['private_key'])

    @staticmethod
    def execute_command(cmd):

        return _execute_command(cmd, get_stderr=True)

    @staticmethod
    def write_file_to(remote_file, data):

        _write_file_to(remote_file, data)

    @staticmethod
    def read_file_from(remote_file):

        return _read_file_from(remote_file)

    @staticmethod
    def close_ssh_connection():

        _cleanup()

    def transfer_helper_script_to_node(self, script_name, parameter_list=None):

        script = open('tempest/api/savanna/resources/%s' % script_name).read()

        if parameter_list:

            for parameter, value in parameter_list.iteritems():

                script = script.replace(
                    '%s=""' % parameter, '%s=%s' % (parameter, value))

        try:

            self.write_file_to('script.sh', script)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(
                    '\nFailure while helper script transferring '
                    'to cluster node: ' + str(e)
                )

        self.execute_command('chmod 777 script.sh')

    def transfer_helper_script_to_nodes(self, node_ip_list, node_username,
                                        script_name, parameter_list=None):

        for node_ip in node_ip_list:

            self.open_ssh_connection(node_ip, node_username)

            self.transfer_helper_script_to_node(script_name, parameter_list)

            self.close_ssh_connection()

#--------------------------------Helper methods--------------------------------

    def delete_objects(self, cluster_id=None,
                       cluster_template_id=None,
                       node_group_template_id_list=None):

        if cluster_id:

            self.savanna.clusters.delete(cluster_id)

        if cluster_template_id:

            self.savanna.cluster_templates.delete(cluster_template_id)

        if node_group_template_id_list:

            for node_group_template_id in node_group_template_id_list:

                self.savanna.node_group_templates.delete(
                    node_group_template_id
                )

    def delete_swift_container(self, container):

        objects = [obj['name'] for obj in
                   self.container_client.list_all_container_objects(container)]
        for obj in objects:
            self.object_client.delete_object(container, obj)

        self.container_client.delete_container(container)

    @staticmethod
    def print_error_log(message, exception=None):

        print(
            '\n\n!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!* '
            'ERROR LOG *!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*'
            '!*!\n'
        )
        print(message + str(exception))
        print(
            '\n!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!* END OF '
            'ERROR LOG *!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*'
            '!*!\n\n'
        )

    def capture_error_log_from_cluster_node(self, log_file):

        print(
            '\n\n!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!* CAPTURED ERROR '
            'LOG FROM CLUSTER NODE *!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*'
            '!*!\n'
        )
        print(self.read_file_from(log_file))
        print(
            '\n!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!* END OF CAPTURED ERROR '
            'LOG FROM CLUSTER NODE *!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*!*'
            '!*!\n\n'
        )

    def tearDown(self):

        super(BaseSavannaTest, self).tearDown()

        self.keypairs_client.delete_keypair(self.ssh_key['name'])

        self.flavors_client.delete_flavor(self.flavor['id'])
