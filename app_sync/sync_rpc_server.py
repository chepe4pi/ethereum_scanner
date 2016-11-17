import concurrent
import multiprocessing

import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

import mongoengine
from constance import config
from mongoengine.connection import disconnect, connect

from app_core.connectors import RpcServerConnector
from app_sync.mongo_models import EthBlocks, EthTransactions

threads_count = multiprocessing.cpu_count() * 2
# THREAD_POOL = ThreadPoolExecutor(threads_count)


def add_block_and_txs_to_mongo(web3, block_data, EthBlocks, EthTransactions):
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


# async def call_coroutines(sync_blocks, web3s, aliases):
#     loop = asyncio.get_event_loop()
#     futures = [
#         loop.run_in_executor(THREAD_POOL, sync_block_and_txs, i, web3s[sync_blocks.index(i)],
#                              aliases[sync_blocks.index(i)]) for i in sync_blocks]
#     await asyncio.wait(futures)


def sync_db_with_rpc_server(start_block, end_block):
    # loop = asyncio.get_event_loop_policy().new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()

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

    # with THREAD_POOL:
    #     while sync_position <= end_block:
    #         block_end_range = (
    #         end_block + 1 if sync_position + threads_count > end_block else sync_position + threads_count)
    #         sync_blocks = [i for i in range(sync_position, block_end_range)]
    #
    #         loop.run_until_complete(call_coroutines(sync_blocks, web3s, aliases))
    #
    #         sync_position = sync_blocks[-1] + 1
    #     loop.close()

    with ProcessPoolExecutor(threads_count) as executor:
        while sync_position <= end_block:
            futures = set()
            block_end_range = (
                end_block + 1 if sync_position + threads_count > end_block else sync_position + threads_count)
            sync_blocks = [i for i in range(sync_position, block_end_range)]
            for block in sync_blocks:
                future = executor.submit(sync_block_and_txs, block, web3s[sync_blocks.index(block)],
                                         aliases[sync_blocks.index(block)])
                futures.add(future)
            completed = wait_for(futures)

            if not completed:
                executor.shutdown()

    for alias in aliases:
        disconnect(alias)  # # test sync speed result


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



# web3 = RpcServerConnector().get_connection()
# for block in range(start_block, end_block):
#     sync_block_and_txs(web3, block)
