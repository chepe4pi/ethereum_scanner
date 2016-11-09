import multiprocessing

import asyncio
from concurrent.futures import ThreadPoolExecutor

from app_core.connectors import RpcServerConnector
from app_core.utils import timestamp_to_utc_datetime
from app_sync.mongo_models import Blocks, Transactions

from mongoengine import connect

connect('ethereum_scan')
threads_count = multiprocessing.cpu_count() * 2
THREAD_POOL = ThreadPoolExecutor(threads_count)


def sync_block_and_txs(web3, block):
    if Blocks.objects(number=block).count():
        return
    block_data = web3.eth.getBlock(block)
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


async def call_coroutines(sync_blocks):
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(THREAD_POOL, sync_block_and_txs, RpcServerConnector().get_connection(), i)
        for i in sync_blocks]
    await asyncio.wait(futures)


def sync_blocks(start_block, end_block):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    sync_position = start_block
    with THREAD_POOL:
        while sync_position <= end_block:
            sync_blocks = [i for i in range(sync_position, sync_position + threads_count) if i <= end_block]

            loop.run_until_complete(call_coroutines(sync_blocks))

            sync_position = sync_blocks[-1] + 1
        loop.close()

        # test sync speed result
        # web3 = RpcServerConnector('127.0.0.1', 8545).get_connection()
        # for block in range(start_block, end_block):
        #     sync_block_and_txs(web3, block)
