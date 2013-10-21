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


from tempest.openstack.common import excutils
from tempest.savanna import base


class MapReduceTest(base.ITestCase):

    def __run_pi_job(self):

        self.execute_command('./script.sh run_pi_job')

    def __get_name_of_completed_pi_job(self):

        try:

            job_name = self.execute_command('./script.sh get_pi_job_name')

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(
                    'Failure while name obtaining completed \'PI\' job: ' +
                    str(e)
                )
                print(
                    self.read_file_from('/tmp/MapReduceTestOutput/log.txt')
                )

        return job_name[1][:-1]

    def __run_wordcount_job(self):

        try:

            self.execute_command('./script.sh run_wordcount_job')

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print('Failure while \'Wordcount\' job launch: ' + str(e))
                print(
                    self.read_file_from('/tmp/MapReduceTestOutput/log.txt')
                )

    @base.skip_test('SKIP_MAP_REDUCE_TEST',
                    message='Test for Map Reduce was skipped.')
    def _map_reduce_testing(self, cluster_info, hadoop_version=None):

        plugin = cluster_info['plugin']

        if not hadoop_version:

            hadoop_version = plugin.HADOOP_VERSION

        node_count = cluster_info['node_info']['node_count']

        extra_script_parameters = {
            'HADOOP_VERSION': hadoop_version,
            'HADOOP_DIRECTORY': plugin.HADOOP_DIRECTORY,
            'HADOOP_LOG_DIRECTORY': plugin.HADOOP_LOG_DIRECTORY,
            'HADOOP_USER': plugin.HADOOP_USER,
            'NODE_COUNT': node_count,
            'PLUGIN_NAME': plugin.PLUGIN_NAME
        }

        node_ip_and_process_list = cluster_info['node_ip_list']

        try:

            self.transfer_helper_script_to_nodes(
                node_ip_and_process_list, plugin.NODE_USERNAME,
                'map_reduce_test_script.sh',
                parameter_list=extra_script_parameters)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(str(e))

        namenode_ip = cluster_info['node_info']['namenode_ip']

        self.open_ssh_connection(namenode_ip, plugin.NODE_USERNAME)

        self.__run_pi_job()

        job_name = self.__get_name_of_completed_pi_job()

        self.close_ssh_connection()

        # Check that cluster used each "tasktracker" node while work of PI-job.
        # Count of map-tasks and reduce-tasks in helper script guarantees that
        # cluster will use each from such nodes while work of PI-job.
        try:

            for node_ip, process_list in node_ip_and_process_list.items():

                if plugin.PROCESS_NAMES['tt'] in process_list:

                    self.open_ssh_connection(node_ip, plugin.NODE_USERNAME)

                    self.execute_command(
                        './script.sh check_directory -job_name %s' % job_name
                    )

                    self.close_ssh_connection()

        except Exception as e:

            with excutils.save_and_reraise_exception():

                print(
                    'Log file of completed \'PI\' job on \'tasktracker\' '
                    'cluster node not found: ' + str(e)
                )
                self.close_ssh_connection()
                self.open_ssh_connection(namenode_ip, plugin.NODE_USERNAME)
                print(
                    self.read_file_from('/tmp/MapReduceTestOutput/log.txt')
                )

        self.open_ssh_connection(namenode_ip, plugin.NODE_USERNAME)

        self.__run_wordcount_job()

        self.close_ssh_connection()
