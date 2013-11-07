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

import nose.plugins.attrib as attrib

from tempest.api.savanna import cluster_configs
from tempest.api.savanna import edp
from tempest.api.savanna import map_reduce
from tempest.api.savanna import scaling
from tempest.api.savanna import swift
from tempest import config as cfg
from tempest.openstack.common import excutils


class VanillaGatingTest(cluster_configs.ClusterConfigTest,
                        map_reduce.MapReduceTest, swift.SwiftTest,
                        scaling.ScalingTest, edp.EDPTest):

    SKIP_CLUSTER_CONFIG_TEST = \
        cfg.TempestConfig().savanna_vanilla.skip_cluster_config_test
    SKIP_MAP_REDUCE_TEST = \
        cfg.TempestConfig().savanna_vanilla.skip_map_reduce_test
    SKIP_SWIFT_TEST = cfg.TempestConfig().savanna_vanilla.skip_swift_test
    SKIP_SCALING_TEST = cfg.TempestConfig().savanna_vanilla.skip_scaling_test
    SKIP_EDP_TEST = cfg.TempestConfig().savanna_vanilla.skip_edp_test

    @classmethod
    def setUpClass(cls):
        super(VanillaGatingTest, cls).setUpClass()

        if cls.config.savanna_vanilla.skip_all_tests_for_plugin:

            raise cls.skipException(
                'All tempest tests for Vanilla plugin were skipped')

    @attrib.attr(tags='slow')
    def test_vanilla_plugin_slow(self):

        node_group_template_id_list = []

        #---------------------"tt-dn" node group template creation-------------

        try:

            node_group_template_tt_dn_id = self.create_node_group_template(
                name='vanilla-tt-dn',
                plugin_config=self.config.savanna_vanilla,
                description='test node group template',
                volumes_per_node=0,
                volume_size=0,
                node_processes=['tasktracker', 'datanode'],
                node_configs={
                    'HDFS': cluster_configs.DN_CONFIG,
                    'MapReduce': cluster_configs.TT_CONFIG
                }
            )
            node_group_template_id_list.append(node_group_template_tt_dn_id)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                message = 'Failure while \'tt-dn\' node group ' \
                          'template creation: '
                self.print_error_log(message, e)

        #-----------------------"tt" node group template creation--------------

        try:

            node_group_template_tt_id = self.create_node_group_template(
                name='vanilla-tt',
                plugin_config=self.config.savanna_vanilla,
                description='test node group template',
                volumes_per_node=0,
                volume_size=0,
                node_processes=['tasktracker'],
                node_configs={
                    'MapReduce': cluster_configs.TT_CONFIG
                }
            )
            node_group_template_id_list.append(node_group_template_tt_id)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    node_group_template_id_list=node_group_template_id_list
                )

                message = 'Failure while \'tt\' node group template creation: '
                self.print_error_log(message, e)

        #----------------------"dn" node group template creation---------------

        try:

            node_group_template_dn_id = self.create_node_group_template(
                name='vanilla-dn',
                plugin_config=self.config.savanna_vanilla,
                description='test node group template',
                volumes_per_node=0,
                volume_size=0,
                node_processes=['datanode'],
                node_configs={
                    'HDFS': cluster_configs.DN_CONFIG
                }
            )
            node_group_template_id_list.append(node_group_template_dn_id)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    node_group_template_id_list=node_group_template_id_list
                )

                message = 'Failure while \'dn\' node group template creation: '
                self.print_error_log(message, e)

        #---------------------------Cluster template creation------------------

        try:

            cluster_template_id = self.create_cluster_template(
                name='vanilla-test-cluster-template',
                plugin_config=self.config.savanna_vanilla,
                description='test cluster template',
                cluster_configs={
                    'HDFS': cluster_configs.CLUSTER_HDFS_CONFIG,
                    'MapReduce': cluster_configs.CLUSTER_MR_CONFIG,
                    'general': cluster_configs.CLUSTER_GENERAL_CONFIG
                },
                node_groups=[
                    dict(
                        name='master-node-jt-nn',
                        flavor_id=self.flavor['id'],
                        node_processes=['namenode', 'jobtracker'],
                        node_configs={
                            'HDFS': cluster_configs.NN_CONFIG,
                            'MapReduce': cluster_configs.JT_CONFIG
                        },
                        count=1),
                    dict(
                        name='master-node-sec-nn-oz',
                        flavor_id=self.flavor['id'],
                        node_processes=['secondarynamenode', 'oozie'],
                        node_configs={},
                        count=1),
                    dict(
                        name='worker-node-tt-dn',
                        node_group_template_id=node_group_template_tt_dn_id,
                        count=3),
                    dict(
                        name='worker-node-dn',
                        node_group_template_id=node_group_template_dn_id,
                        count=1),
                    dict(
                        name='worker-node-tt',
                        node_group_template_id=node_group_template_tt_id,
                        count=1)
                ]
            )

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    node_group_template_id_list=node_group_template_id_list
                )

                message = 'Failure while cluster template creation: '
                self.print_error_log(message, e)

        #-------------------------------Cluster creation-----------------------

        try:

            cluster_info = self.create_cluster_and_get_info(
                plugin_config=self.config.savanna_vanilla,
                cluster_template_id=cluster_template_id,
                description='test cluster',
                cluster_configs={}
            )

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    self.cluster_id, cluster_template_id,
                    node_group_template_id_list
                )

                message = 'Failure while cluster creation: '
                self.print_error_log(message, e)

        #----------------------------CLUSTER CONFIG TESTING--------------------

        try:
            self._cluster_config_testing(cluster_info)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    cluster_info['cluster_id'], cluster_template_id,
                    node_group_template_id_list
                )

                message = 'Failure while cluster config testing: '
                self.print_error_log(message, e)

        #------------------------------MAP REDUCE TESTING----------------------

        try:

            self._map_reduce_testing(cluster_info)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    cluster_info['cluster_id'], cluster_template_id,
                    node_group_template_id_list
                )

                message = 'Failure while Map Reduce testing: '
                self.print_error_log(message, e)

        #---------------------------CHECK SWIFT AVAILABILITY-------------------

        try:

            self._check_swift_availability(cluster_info)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    cluster_info['cluster_id'], cluster_template_id,
                    node_group_template_id_list
                )

                message = 'Failure during check of Swift availability: '
                self.print_error_log(message, e)

        #----------------------------------EDP TESTING-------------------------

        job_data = open('tempest/api/savanna/resources/edp-job.pig').read()

        lib_data = open('tempest/api/savanna/resources/edp-lib.jar').read()

        job_jar_data = open('tempest/api/savanna/resources/edp-job.jar').read()

        configs = {
            "configs": {
            "mapred.mapper.class": "org.apache.oozie.example.SampleMapper",
            "mapred.reducer.class": "org.apache.oozie.example.SampleReducer"
            }
        }

        try:

            self._edp_testing('Pig', [{'pig': job_data}], [{'jar': lib_data}])

            self._edp_testing('Jar', [], [{'jar': job_jar_data}], configs)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    cluster_info['cluster_id'], cluster_template_id,
                    node_group_template_id_list
                )

                message = 'Failure while EDP testing: '
                self.print_error_log(message, e)

        #--------------------------------CLUSTER SCALING-----------------------

        change_list = [
            {
                'operation': 'resize',
                'info': ['worker-node-tt-dn', 4]
            },
            {
                'operation': 'resize',
                'info': ['worker-node-dn', 0]
            },
            {
                'operation': 'resize',
                'info': ['worker-node-tt', 0]
            },
            {
                'operation': 'add',
                'info': [
                    'new-worker-node-tt', 1, '%s' % node_group_template_tt_id
                ]
            },
            {
                'operation': 'add',
                'info': [
                    'new-worker-node-dn', 1, '%s' % node_group_template_dn_id
                ]
            }
        ]

        try:

            new_cluster_info = self._cluster_scaling(cluster_info, change_list)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    cluster_info['cluster_id'], cluster_template_id,
                    node_group_template_id_list
                )

                message = 'Failure while cluster scaling: '
                self.print_error_log(message, e)

        if not self.config.savanna_vanilla.skip_scaling_test:

        #---------------------CLUSTER CONFIG TESTING AFTER SCALING-------------

            try:

                self._cluster_config_testing(new_cluster_info)

            except Exception as e:

                with excutils.save_and_reraise_exception():

                    self.delete_objects(
                        new_cluster_info['cluster_id'], cluster_template_id,
                        node_group_template_id_list
                    )

                    message = 'Failure while cluster config testing after ' \
                              'cluster scaling: '
                    self.print_error_log(message, e)

        #-----------------------MAP REDUCE TESTING AFTER SCALING---------------

            try:

                self._map_reduce_testing(new_cluster_info)

            except Exception as e:

                with excutils.save_and_reraise_exception():

                    self.delete_objects(
                        new_cluster_info['cluster_id'], cluster_template_id,
                        node_group_template_id_list
                    )

                    message = 'Failure while Map Reduce testing after ' \
                              'cluster scaling: '
                    self.print_error_log(message, e)

        #--------------------CHECK SWIFT AVAILABILITY AFTER SCALING------------

            try:

                self._check_swift_availability(new_cluster_info)

            except Exception as e:

                with excutils.save_and_reraise_exception():

                    self.delete_objects(
                        new_cluster_info['cluster_id'], cluster_template_id,
                        node_group_template_id_list
                    )

                    message = 'Failure during check of Swift availability ' \
                              'after cluster scaling: '
                    self.print_error_log(message, e)

        #----------------------------DELETE CREATED OBJECTS--------------------

        self.delete_objects(
            cluster_info['cluster_id'], cluster_template_id,
            node_group_template_id_list
        )

    @attrib.attr(tags='smoke')
    def test_vanilla_plugin_smoke(self):

        node_group_template_id_list = []

        #-------------------master node group template creation----------------

        try:

            node_group_template_master_id = self.create_node_group_template(
                name='smoke-vanilla-jt-nn',
                plugin_config=self.config.savanna_vanilla,
                description='test node group template',
                volumes_per_node=0,
                volume_size=0,
                node_processes=['jobtracker', 'namenode'],
                node_configs={
                    'HDFS': cluster_configs.DN_CONFIG,
                    'MapReduce': cluster_configs.TT_CONFIG
                }
            )
            node_group_template_id_list.append(node_group_template_master_id)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                message = """
                Failure while node group template (with topology:
                jobtracker+namenode) creation:
                """
                self.print_error_log(message, e)

        #---------------------worker node group template creation--------------

        try:

            node_group_template_worker_id = self.create_node_group_template(
                name='smoke-vanilla-tt-dn',
                plugin_config=self.config.savanna_vanilla,
                description='test node group template',
                volumes_per_node=0,
                volume_size=0,
                node_processes=['tasktracker', 'datanode'],
                node_configs={
                    'MapReduce': cluster_configs.TT_CONFIG
                }
            )
            node_group_template_id_list.append(node_group_template_worker_id)

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    node_group_template_id_list=node_group_template_id_list
                )

                message = """
                Failure while node group template (with topology:
                tasktracker+datanode) creation:
                """
                self.print_error_log(message, e)

        #---------------------------Cluster template creation------------------

        try:

            cluster_template_with_ngt_id = self.create_cluster_template(
                name='vanilla-test-cluster-template-1',
                plugin_config=self.config.savanna_vanilla,
                description='test cluster template',
                cluster_configs={
                    'HDFS': cluster_configs.CLUSTER_HDFS_CONFIG,
                    'MapReduce': cluster_configs.CLUSTER_MR_CONFIG,
                    'general': cluster_configs.CLUSTER_GENERAL_CONFIG
                },
                node_groups=[
                    dict(
                        name='master-node',
                        node_group_template_id=node_group_template_master_id,
                        count=1),
                    dict(
                        name='worker-node',
                        node_group_template_id=node_group_template_worker_id,
                        count=3)
                ]
            )

        except Exception as e:

            with excutils.save_and_reraise_exception():

                self.delete_objects(
                    node_group_template_id_list=node_group_template_id_list
                )

        try:

            cluster_template_without_ngt_id = self.create_cluster_template(
                name='vanilla-test-cluster-template-2',
                plugin_config=self.config.savanna_vanilla,
                description='test cluster template',
                cluster_configs={
                    'HDFS': cluster_configs.CLUSTER_HDFS_CONFIG,
                    'MapReduce': cluster_configs.CLUSTER_MR_CONFIG,
                    'general': cluster_configs.CLUSTER_GENERAL_CONFIG
                },
                node_groups=[
                    dict(
                        name='master-node',
                        flavor_id=self.flavor['id'],
                        node_processes=['namenode', 'jobtracker'],
                        node_configs={
                            'HDFS': cluster_configs.NN_CONFIG,
                            'MapReduce': cluster_configs.JT_CONFIG
                        },
                        count=1),
                    dict(
                        name='worker-node',
                        flavor_id=self.flavor['id'],
                        node_processes=['datanode', 'tasktracker'],
                        node_configs={},
                        count=1),
                ]
            )

        except Exception as e:

            with excutils.save_and_reraise_exception():

                message = """
                Failure while cluster template without
                nodegroup templates creation:
                """
                self.print_error_log(message, e)

        self.delete_objects(
            cluster_template_id=cluster_template_with_ngt_id,
            node_group_template_id_list=node_group_template_id_list)

        self.delete_objects(
            cluster_template_id=cluster_template_without_ngt_id)
