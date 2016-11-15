import copy

import mongoengine
from constance import config
from mongoengine.context_managers import switch_db
from pymongo import MongoClient

from app_core.tests.factories import UserFactory
from app_core.tests.tx_data_for_tests import test_block_data_list, test_tx_data_list
from app_core.utils import timestamp_to_utc_datetime
from app_sync.mongo_models import EthBlocks, EthTransactions


class AuthorizeForTestsMixin:
    def setUp(self):
        super(AuthorizeForTestsMixin, self).setUp()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)


class CreateMongoTxsAndBlocksMixin:
    def setUp(self):
        super(CreateMongoTxsAndBlocksMixin, self).setUp()
        blocks = []
        mongoengine.register_connection(config.MONGO_TEST_DATABASE_NAME, name=config.MONGO_TEST_DATABASE_NAME)
        with switch_db(EthBlocks, config.MONGO_TEST_DATABASE_NAME) as TestEthBlocks:
            for test_block_data in test_block_data_list:
                block = TestEthBlocks(**test_block_data)
                block.created = timestamp_to_utc_datetime(test_block_data['timestamp'])
                block.save()
                blocks.append(block)
        with switch_db(EthTransactions, config.MONGO_TEST_DATABASE_NAME) as TestEthTransactions:
            for test_tx_data in test_tx_data_list:
                data_to_create = copy.deepcopy(test_tx_data)
                data_to_create['fromAddress'] = test_tx_data.get('from')
                data_to_create['toAddress'] = test_tx_data.get('to')
                tx = TestEthTransactions(**data_to_create)
                tx.block = blocks[0]
                tx.save()

    def tearDown(self):
        super().tearDown()
        client = MongoClient()
        client[config.MONGO_TEST_DATABASE_NAME].eth_blocks.remove()
        client[config.MONGO_TEST_DATABASE_NAME].eth_transactions.remove()
