from constance import config
from django.urls import reverse
from mongoengine.context_managers import switch_db
from rest_framework import status
from rest_framework.test import APITestCase

from app_auth.models import ApiKey
from app_auth.models import ClientInfo
from app_auth.serializers import ApiKeySerializer
from app_core.tests.mixins import AuthorizeForTestsMixin, CreateMongoTxsAndBlocksMixin
from app_sync.mongo_models import EthTransactions, EthBlocks
from app_tx_api.mongo_serializers import TxSerializer


class GetTxsNotApiKeyTestCase(CreateMongoTxsAndBlocksMixin, AuthorizeForTestsMixin, APITestCase):
    def test_get_all_txs_not_api_key(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'))

                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_txs_fake_api_key(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': '321'})
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetTxsTestCase(CreateMongoTxsAndBlocksMixin, AuthorizeForTestsMixin, APITestCase):
    def test_get_all_txs(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': self.api_key.key})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 4)
                self.assertEqual(response.data, TxSerializer(TestEthTransactions.objects.all(), many=True).data)

    def test_get_filter_to_txs(self):
        from_address = '0x42e6723a0c884e922240e56d7b618bec96f35800'
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'),
                                           {'fromAddress': from_address, 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'), {'toAddress': to_address, 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'), {'toAddress': to_address, 'fromAddress': from_address,
                                                                 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'), {'toAddress': to_address, 'fromAddress': from_address,
                                                                 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'),
                                           {'blockNumber': block_number, 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'),
                                           {'blockNumber__gte': block_number, 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'),
                                           {'blockNumber__lt': block_number, 'api_key': self.api_key.key})
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

                response = self.client.get(reverse('txs-list'),
                                           {'timestamp__gte': timestamp, 'api_key': self.api_key.key})
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data, TxSerializer(
                    TestEthTransactions.objects.filter(timestamp__gte=timestamp), many=True).data)


class GetAllTxsPaginationTestCase(CreateMongoTxsAndBlocksMixin, AuthorizeForTestsMixin, APITestCase):
    def test_get_all_limit_offset_txs(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': self.api_key.key, 'offset': 1, 'limit': 2})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 2)
                self.assertEqual(response.data, TxSerializer([TestEthTransactions.objects.all()[1],
                                                              TestEthTransactions.objects.all()[2]], many=True).data)

    def test_get_all_limit_offset_two_txs(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': self.api_key.key, 'offset': 2, 'limit': 2})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 2)
                self.assertEqual(response.data, TxSerializer([TestEthTransactions.objects.all()[2],
                                                              TestEthTransactions.objects.all()[3]], many=True).data)

    def test_get_all_limit_no_offset_txs(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': self.api_key.key, 'limit': 3})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data, TxSerializer([TestEthTransactions.objects.all()[0],
                                                              TestEthTransactions.objects.all()[1],
                                                              TestEthTransactions.objects.all()[2]], many=True).data)

    def test_get_all_no_limit_offset_txs(self):
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': self.api_key.key, 'offset': 1})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 3)
                self.assertEqual(response.data, TxSerializer([TestEthTransactions.objects.all()[1],
                                                              TestEthTransactions.objects.all()[2],
                                                              TestEthTransactions.objects.all()[3]], many=True).data)

    def test_get_all_system_limit_txs(self):
        system_pagination = config.MAX_ROWS_IN_API_RESPONSE
        config.MAX_ROWS_IN_API_RESPONSE = 2
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
                self.assertEqual(TestEthTransactions.objects.count(), 4)
                self.assertEqual(TestEthBlocks.objects.count(), 3)

                response = self.client.get(reverse('txs-list'), {'api_key': self.api_key.key, 'offset': 1})

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data), 2)
                self.assertEqual(response.data, TxSerializer([TestEthTransactions.objects.all()[1],
                                                              TestEthTransactions.objects.all()[2]], many=True).data)
        config.MAX_ROWS_IN_API_RESPONSE = system_pagination


class CreateApiKeyAuthTestCase(AuthorizeForTestsMixin, APITestCase):
    def test_create_api_key_authorized(self):
        response = self.client.post(reverse('api-key-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client_info = ClientInfo.objects.get()
        self.assertEqual(client_info.user, self.user)
        self.assertEqual(client_info.ip_address, '127.0.0.1')

        api_key = ApiKey.objects.get()
        self.assertEqual(api_key.client_info, client_info)
        self.assertEqual(api_key.is_active, True)
        self.assertEqual(response.data, ApiKeySerializer(api_key).data)


class CreateApiKeyUnAuthTestCase(APITestCase):
    def test_create_api_key_unauthorized(self):
        response = self.client.post(reverse('api-key-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client_info = ClientInfo.objects.get()
        self.assertEqual(client_info.user, None)
        self.assertEqual(client_info.ip_address, '127.0.0.1')

        api_key = ApiKey.objects.get()
        self.assertEqual(api_key.client_info, client_info)
        self.assertEqual(api_key.is_active, True)
        self.assertEqual(response.data, ApiKeySerializer(api_key).data)
