import unittest

from helpers import configuration
from helpers.resources import resource, wait_for_completion
from profitbricks.client import Server, Volume
from six import assertRegex

from profitbricks.client import Datacenter
from profitbricks.client import ProfitBricksService


class TestDatacenter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.resource = resource()
        self.client = ProfitBricksService(
            username=configuration.USERNAME,
            password=configuration.PASSWORD,
            headers=configuration.HEADERS)

        # Create test datacenter.
        self.datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))

    @classmethod
    def tearDownClass(self):
        self.client.delete_datacenter(datacenter_id=self.datacenter['id'])

    def test_list(self):
        datacenters = self.client.list_datacenters()

        self.assertGreater(len(datacenters), 0)
        self.assertEqual(datacenters['items'][0]['type'], 'datacenter')

    def test_get(self):
        datacenter = self.client.get_datacenter(
            datacenter_id=self.datacenter['id'])

        assertRegex(self, datacenter['id'], self.resource['uuid_match'])
        self.assertEqual(datacenter['type'], 'datacenter')
        self.assertEqual(datacenter['id'], self.datacenter['id'])
        self.assertEqual(datacenter['properties']['name'], self.resource['datacenter']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter']['description'])
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter']['location'])

    def test_delete(self):
        datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        wait_for_completion(self.client, datacenter, 'create_datacenter')

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])

        self.assertTrue(response)

    def test_update(self):
        datacenter = self.client.update_datacenter(
            datacenter_id=self.datacenter['id'],
            description=self.resource['datacenter']['name']+' - RENAME')
        wait_for_completion(self.client, datacenter, 'update_datacenter')
        datacenter = self.client.get_datacenter(datacenter_id=self.datacenter['id'])

        assertRegex(self, datacenter['id'], self.resource['uuid_match'])
        self.assertEqual(datacenter['id'], self.datacenter['id'])
        self.assertEqual(datacenter['properties']['name'], self.resource['datacenter']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter']['name']+' - RENAME')
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter']['location'])
        self.assertGreater(datacenter['properties']['version'], 1)

    def test_create_simple(self):
        datacenter = self.client.create_datacenter(
            datacenter=Datacenter(**self.resource['datacenter']))
        wait_for_completion(self.client, datacenter, 'create_datacenter')

        self.assertEqual(datacenter['properties']['name'], self.resource['datacenter']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter']['description'])
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter']['location'])

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])
        self.assertTrue(response)

    def test_create_complex(self):
        datacenter_resource = Datacenter(**self.resource['datacenter_complex'])
        datacenter_resource.servers = [Server(**self.resource['server'])]
        datacenter_resource.volumes = [Volume(**self.resource['volume'])]

        datacenter = self.client.create_datacenter(
            datacenter=datacenter_resource)
        wait_for_completion(self.client, datacenter, 'create_datacenter_complex')

        self.assertEqual(datacenter['properties']['name'],
                         self.resource['datacenter_complex']['name'])
        self.assertEqual(datacenter['properties']['description'],
                         self.resource['datacenter_complex']['description'])
        self.assertEqual(datacenter['properties']['location'],
                         self.resource['datacenter_complex']['location'])
        self.assertGreater(len(datacenter['entities']['servers']), 0)
        self.assertGreater(len(datacenter['entities']['volumes']), 0)

        response = self.client.delete_datacenter(
            datacenter_id=datacenter['id'])
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
