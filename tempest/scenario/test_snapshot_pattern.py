# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 NEC Corporation
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

import logging

from tempest.common.utils.data_utils import rand_name
from tempest.common.utils.linux.remote_client import RemoteClient
from tempest.scenario import manager


LOG = logging.getLogger(__name__)


class TestSnapshotPattern(manager.OfficialClientTest):
    """
    This test is for snapshotting an instance and booting with it.
    The following is the scenario outline:
     * boot a instance and create a timestamp file in it
     * snapshot the instance
     * boot a second instance from the snapshot
     * check the existence of the timestamp file in the second instance

    """

    def _wait_for_server_status(self, server, status):
        self.status_timeout(self.compute_client.servers,
                            server.id,
                            status)

    def _wait_for_image_status(self, image_id, status):
        self.status_timeout(self.image_client.images, image_id, status)

    def _boot_image(self, image_id):
        name = rand_name('scenario-server-')
        client = self.compute_client
        flavor_id = self.config.compute.flavor_ref
        LOG.debug("name:%s, image:%s" % (name, image_id))
        server = client.servers.create(name=name,
                                       image=image_id,
                                       flavor=flavor_id,
                                       key_name=self.keypair.name)
        self.addCleanup(self.compute_client.servers.delete, server)
        self.assertEqual(name, server.name)
        self._wait_for_server_status(server, 'ACTIVE')
        server = client.servers.get(server)  # getting network information
        LOG.debug("server:%s" % server)
        return server

    def _add_keypair(self):
        name = rand_name('scenario-keypair-')
        self.keypair = self.compute_client.keypairs.create(name=name)
        self.addCleanup(self.compute_client.keypairs.delete, self.keypair)
        self.assertEqual(name, self.keypair.name)

    def _create_security_group_rule(self):
        sgs = self.compute_client.security_groups.list()
        for sg in sgs:
            if sg.name == 'default':
                secgroup = sg

        ruleset = {
            # ssh
            'ip_protocol': 'tcp',
            'from_port': 22,
            'to_port': 22,
            'cidr': '0.0.0.0/0',
            'group_id': None
        }
        sg_rule = self.compute_client.security_group_rules.create(secgroup.id,
                                                                  **ruleset)
        self.addCleanup(self.compute_client.security_group_rules.delete,
                        sg_rule.id)

    def _ssh_to_server(self, server):
        username = self.config.scenario.ssh_user
        ip = server.networks[self.config.compute.network_for_ssh][0]
        linux_client = RemoteClient(ip,
                                    username,
                                    pkey=self.keypair.private_key)

        return linux_client.ssh_client

    def _write_timestamp(self, server):
        ssh_client = self._ssh_to_server(server)
        ssh_client.exec_command('date > /tmp/timestamp; sync')
        self.timestamp = ssh_client.exec_command('cat /tmp/timestamp')

    def _create_image(self, server):
        snapshot_name = rand_name('scenario-snapshot-')
        create_image_client = self.compute_client.servers.create_image
        image_id = create_image_client(server, snapshot_name)
        self.addCleanup(self.image_client.images.delete, image_id)
        self._wait_for_server_status(server, 'ACTIVE')
        self._wait_for_image_status(image_id, 'active')
        snapshot_image = self.image_client.images.get(image_id)
        self.assertEquals(snapshot_name, snapshot_image.name)
        return image_id

    def _check_timestamp(self, server):
        ssh_client = self._ssh_to_server(server)
        got_timestamp = ssh_client.exec_command('cat /tmp/timestamp')
        self.assertEqual(self.timestamp, got_timestamp)

    def test_snapshot_pattern(self):
        # prepare for booting a instance
        self._add_keypair()
        self._create_security_group_rule()

        # boot a instance and create a timestamp file in it
        server = self._boot_image(self.config.compute.image_ref)
        self._write_timestamp(server)

        # snapshot the instance
        snapshot_image_id = self._create_image(server)

        # boot a second instance from the snapshot
        server_from_snapshot = self._boot_image(snapshot_image_id)

        # check the existence of the timestamp file in the second instance
        self._check_timestamp(server_from_snapshot)
