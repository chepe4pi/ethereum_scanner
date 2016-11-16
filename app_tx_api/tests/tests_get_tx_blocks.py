from constance import config
from django.urls import reverse
from mongoengine.context_managers import switch_db
from rest_framework import status
from rest_framework.test import APITestCase

from app_core.tests.mixins import AuthorizeForTestsMixin, CreateMongoTxsAndBlocksMixin
from app_sync.mongo_models import EthTransactions, EthBlocks
from app_tx_api.mongo_serializers import TxSerializer


class GetTxsTestCase(CreateMongoTxsAndBlocksMixin, AuthorizeForTestsMixin, APITestCase):
    def test_get_all_txs(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'))

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data, TxSerializer(TestEthTransactions.objects.all(), many=True).data)

    def test_get_filter_txs(self):
        to_address = '0x42e6723a0c884e922240e56d7b618bec96f35801'
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'toAddress': to_address})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 2)
                self.assertEqual(response.data,
                                 TxSerializer(TestEthTransactions.objects.filter(toAddress=to_address), many=True).data)
