import datetime

import pytz
from constance import config
from django.urls import reverse
from mongoengine.context_managers import switch_db
from rest_framework import status
from rest_framework.test import APITestCase

from app_core.tests.mixins import AuthorizeForTestsMixin, CreateMongoTxsAndBlocksMixin
from app_follows.tests.factories import FollowFactory, EthAccountInfoFactory
from app_sync.mongo_models import EthTransactions, EthBlocks


class GetTimelineTestCase(CreateMongoTxsAndBlocksMixin, AuthorizeForTestsMixin, APITestCase):
    def test_get_all_follow_txs(self):
        self.address = '0x42e6723a0c884e922240e56d7b618bec96f35800'
        follow = FollowFactory(user=self.user, address=self.address)
        follow.created = datetime.datetime.fromtimestamp(1442885501).replace(tzinfo=pytz.utc)
        follow.save()
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('timeline-list'))

                self.assertEqual(len(response.data), 4)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data[0]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[0]['address2'], '0x1194e966965418c7d73a42cceeb254d875860356')
                self.assertEqual(response.data[0]['sent'], True)
                self.assertEqual(response.data[1]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[1]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35801')
                self.assertEqual(response.data[1]['sent'], True)
                self.assertEqual(response.data[2]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[2]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35801')
                self.assertEqual(response.data[2]['sent'], True)
                self.assertEqual(response.data[3]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[3]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35801')
                self.assertEqual(response.data[3]['sent'], False)

    def test_get_all_follow_txs_two(self):
        self.address = '0x42e6723a0c884e922240e56d7b618bec96f35800'
        follow = FollowFactory(user=self.user, address=self.address)
        follow.created = datetime.datetime.fromtimestamp(1442886501).replace(tzinfo=pytz.utc)
        follow.save()
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('timeline-list'))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data[0]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[0]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35801')
                self.assertEqual(response.data[0]['sent'], True)
                self.assertEqual(response.data[1]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[1]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35801')
                self.assertEqual(response.data[1]['sent'], True)
                self.assertEqual(response.data[2]['address'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[2]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35801')
                self.assertEqual(response.data[2]['sent'], False)

    def test_get_all_follow_txs_three(self):
        self.address = '0x1194e966965418c7d73a42cceeb254d875860356'
        EthAccountInfoFactory(address=self.address)
        follow = FollowFactory(user=self.user, address=self.address)
        follow.created = datetime.datetime(1971, 2, 1, 2, 3).replace(tzinfo=pytz.utc)
        follow.save()
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('timeline-list'))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]['address'], '0x1194e966965418c7d73a42cceeb254d875860356')
                self.assertEqual(response.data[0]['address2'], '0x42e6723a0c884e922240e56d7b618bec96f35800')
                self.assertEqual(response.data[0]['sent'], False)
                self.assertEqual(response.data[0]['timestamp'], 1442886001)
                self.assertEqual(response.data[0]['amount_in_wei'], 1)
                self.assertEqual(response.data[0]['address_name'], 'Test Eth Account Name')
                self.assertTrue(response.data[0]['address_avatar'].endswith('jpg'), True)
