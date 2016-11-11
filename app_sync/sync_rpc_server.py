import multiprocessing

import asyncio
from concurrent.futures import ThreadPoolExecutor

import mongoengine
from constance import config
from mongoengine.connection import disconnect, connect

from app_core.connectors import RpcServerConnector
from app_core.utils import timestamp_to_utc_datetime
from app_sync.mongo_models import Blocks, Transactions

threads_count = multiprocessing.cpu_count() * 2
THREAD_POOL = ThreadPoolExecutor(threads_count)


def add_block_to_mongo(web3, block_data, Blocks, Transactions):
    block = Blocks(**block_data)
    block.created = timestamp_to_utc_datetime(block_data['timestamp'])
    block.save()
    for tx_hash in block.transactions:
        tx_data = web3.eth.getTransaction(tx_hash)
        tx_data['fromAddress'] = tx_data.pop('from')
        tx_data['toAddress'] = tx_data.pop('to')
        tx = Transactions(**tx_data)
        tx.block = block.id
        tx.save()


def sync_block_and_txs(block_num, web3, connection_alias=None):
    if connection_alias:
        Blocks._meta['db_alias'] = connection_alias
        Transactions._meta['db_alias'] = connection_alias
    if Blocks.objects(number=block_num).count():
        return
    try:
        block_data = web3.eth.getBlock(block_num)
    except AttributeError:
        raise ValueError('block {} does not exist'.format(block_num))

    add_block_to_mongo(web3, block_data, Blocks, Transactions)


async def call_coroutines(sync_blocks, web3s, aliases):
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(THREAD_POOL, sync_block_and_txs, i, web3s[sync_blocks.index(i)],
                             aliases[sync_blocks.index(i)]) for i in sync_blocks]
    await asyncio.wait(futures)


def sync_blocks(start_block, end_block):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    sync_position = start_block

    aliases = []
    web3s = []
    for thread, num in enumerate(range(0, threads_count)):
        alias = 'conn_{}'.format(num)
        aliases.append(alias)
        mongoengine.register_connection(alias, name=config.MONGO_DATABASE_NAME)
        connect(config.MONGO_DATABASE_NAME, alias=alias)

        web3 = RpcServerConnector().get_connection()
        web3s.append(web3)

    with THREAD_POOL:
        while sync_position <= end_block:
            block_end_range = (
            end_block + 1 if sync_position + threads_count > end_block else sync_position + threads_count)
            sync_blocks = [i for i in range(sync_position, block_end_range)]

            loop.run_until_complete(call_coroutines(sync_blocks, web3s, aliases))

            sync_position = sync_blocks[-1] + 1
        loop.close()

    for alias in aliases:
        disconnect(alias)

# # test sync speed result
# web3 = RpcServerConnector().get_connection()
# for block in range(start_block, end_block):
#     sync_block_and_txs(web3, block)
