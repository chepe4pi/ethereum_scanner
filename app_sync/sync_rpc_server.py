import concurrent
import multiprocessing

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import mongoengine
from constance import config
from mongoengine.connection import disconnect, connect

from app_core.connectors import RpcServerConnector
from app_sync.mongo_models import EthBlocks, EthTransactions

forks_count = multiprocessing.cpu_count() * 8


def add_block_and_txs_to_mongo(web3, block_data, EthBlocks, EthTransactions):

    # FIXME cheap hack
    block_data.pop('totalDifficulty')

    block = EthBlocks(**block_data)
    block.save()
    for tx_hash in block.transactions:
        tx_data = web3.eth.getTransaction(tx_hash)
        tx_data['fromAddress'] = tx_data.pop('from')
        tx_data['toAddress'] = tx_data.pop('to')
        tx_data['timestamp'] = block_data['timestamp']
        tx = EthTransactions(**tx_data)
        tx.save()


def sync_block_and_txs(block_num, web3, connection_alias=None):
    if connection_alias:
        EthBlocks._meta['db_alias'] = connection_alias
        EthTransactions._meta['db_alias'] = connection_alias
    if EthBlocks.objects(number=block_num).count():
        return
    try:
        block_data = web3.eth.getBlock(block_num)
    except AttributeError:
        raise ValueError('block {} does not exist'.format(block_num))

    add_block_and_txs_to_mongo(web3, block_data, EthBlocks, EthTransactions)


def sync_db_with_rpc_server(start_block, end_block):
    sync_position = start_block

    aliases = []
    web3s = []

    for thread, num in enumerate(range(0, forks_count)):
        alias = 'conn_{}'.format(num)
        aliases.append(alias)
        mongoengine.register_connection(alias, name=config.MONGO_DATABASE_NAME)
        connect(config.MONGO_DATABASE_NAME, alias=alias)

        web3 = RpcServerConnector().get_connection()
        web3s.append(web3)

    with ProcessPoolExecutor(forks_count) as executor:
        while sync_position <= end_block:
            futures = set()
            block_end_range = (
                end_block + 1 if sync_position + forks_count > end_block else sync_position + forks_count)
            sync_blocks = [i for i in range(sync_position, block_end_range)]
            for block in sync_blocks:
                future = executor.submit(sync_block_and_txs, block, web3s[sync_blocks.index(block)],
                                         aliases[sync_blocks.index(block)])
                futures.add(future)
            completed = wait_for(futures)
            sync_position = sync_blocks[-1] + 1

            if not completed:
                executor.shutdown()

    for alias in aliases:
        disconnect(alias)


def wait_for(futures):
    canceled = False
    try:
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err:
                raise err
    except KeyboardInterrupt:
        canceled = True
        for future in futures:
            future.cancel()
    return not canceled

# # test sync speed result
# web3 = RpcServerConnector().get_connection()
# for block in range(start_block, end_block):
#     sync_block_and_txs(web3, block)
