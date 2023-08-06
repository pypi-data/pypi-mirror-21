# Copyright 2013 OpenStack Foundation
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

from testtools import matchers

from tempest.api.volume import base
from tempest.common import waiters
from tempest.lib import decorators


class VolumesTransfersTest(base.BaseVolumeTest):

    credentials = ['primary', 'alt', 'admin']

    @classmethod
    def setup_clients(cls):
        super(VolumesTransfersTest, cls).setup_clients()

        cls.client = cls.os.volume_transfers_v2_client
        cls.alt_client = cls.os_alt.volume_transfers_v2_client
        cls.alt_volumes_client = cls.os_alt.volumes_v2_client
        cls.adm_volumes_client = cls.os_adm.volumes_v2_client

    @decorators.idempotent_id('4d75b645-a478-48b1-97c8-503f64242f1a')
    def test_create_get_list_accept_volume_transfer(self):
        # Create a volume first
        volume = self.create_volume()
        self.addCleanup(self.delete_volume,
                        self.adm_volumes_client,
                        volume['id'])

        # Create a volume transfer
        transfer = self.client.create_volume_transfer(
            volume_id=volume['id'])['transfer']
        transfer_id = transfer['id']
        auth_key = transfer['auth_key']
        waiters.wait_for_volume_resource_status(
            self.volumes_client, volume['id'], 'awaiting-transfer')

        # Get a volume transfer
        body = self.client.show_volume_transfer(transfer_id)['transfer']
        self.assertEqual(volume['id'], body['volume_id'])

        # List volume transfers, the result should be greater than
        # or equal to 1
        body = self.client.list_volume_transfers()['transfers']
        self.assertThat(len(body), matchers.GreaterThan(0))

        # Accept a volume transfer by alt_tenant
        body = self.alt_client.accept_volume_transfer(
            transfer_id, auth_key=auth_key)['transfer']
        waiters.wait_for_volume_resource_status(self.alt_volumes_client,
                                                volume['id'], 'available')

    @decorators.idempotent_id('ab526943-b725-4c07-b875-8e8ef87a2c30')
    def test_create_list_delete_volume_transfer(self):
        # Create a volume first
        volume = self.create_volume()
        self.addCleanup(self.delete_volume,
                        self.adm_volumes_client,
                        volume['id'])

        # Create a volume transfer
        body = self.client.create_volume_transfer(
            volume_id=volume['id'])['transfer']
        transfer_id = body['id']
        waiters.wait_for_volume_resource_status(
            self.volumes_client, volume['id'], 'awaiting-transfer')

        # List all volume transfers (looking for the one we created)
        body = self.client.list_volume_transfers()['transfers']
        for transfer in body:
            if volume['id'] == transfer['volume_id']:
                break
        else:
            self.fail('Transfer not found for volume %s' % volume['id'])

        # Delete a volume transfer
        self.client.delete_volume_transfer(transfer_id)
        waiters.wait_for_volume_resource_status(
            self.volumes_client, volume['id'], 'available')
