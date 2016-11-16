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
                self.assertEqual(len(response.data), 4)
                self.assertEqual(response.data, TxSerializer(TestEthTransactions.objects.all(), many=True).data)

    def test_get_filter_to_txs(self):
        from_address = '0x42e6723a0c884e922240e56d7b618bec96f35800'
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'fromAddress': from_address})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data,
                                 TxSerializer(TestEthTransactions.objects.filter(fromAddress=from_address),
                                              many=True).data)

    def test_get_filter_from_txs(self):
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

    def test_get_filter_from_to_txs(self):
        from_address = '0x42e6723a0c884e922240e56d7b618bec96f35800'
        to_address = '0x1194e966965418c7d73a42cceeb254d875860356'
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'toAddress': to_address, 'fromAddress': from_address})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(toAddress=to_address, fromAddress=from_address), many=True).data)

    def test_get_filter_empty_txs(self):
        from_address = '0x42e6723a0c884e922240e56d7b618bec96f35801'
        to_address = '0x1194e966965418c7d73a42cceeb254d875860356'
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'toAddress': to_address, 'fromAddress': from_address})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 0)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(toAddress=to_address, fromAddress=from_address), many=True).data)

    def test_get_filter_block_num(self):
        block_number = 270678
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'blockNumber': block_number})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 2)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(blockNumber=block_number), many=True).data)

    def test_get_filter_block_num_gte(self):
        block_number = 270677
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'blockNumber__gte': block_number})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(blockNumber__gte=block_number), many=True).data)

    def test_get_filter_block_num_lt(self):
        block_number = 270678
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'blockNumber__lt': block_number})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 2)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(blockNumber__lt=block_number), many=True).data)

    def test_get_filter_timestamp_gte(self):
        timestamp = 1442886050
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'timestamp__gte': timestamp})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(timestamp__gte=timestamp), many=True).data)
