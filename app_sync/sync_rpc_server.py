import multiprocessing

import asyncio

from app_core.connectors import RpcServerConnector
from app_core.utils import timestamp_to_utc_datetime
from app_sync.mongo_models import Blocks, Transactions

from mongoengine import connect


connect('ethereum_scan')


async def sync_block_and_txs(web3, block):
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
    coroutines = [sync_block_and_txs(RpcServerConnector().get_connection(), i) for i in sync_blocks]
    await asyncio.wait(coroutines)


def sync_blocks(start_block, end_block):
    cpu_count = multiprocessing.cpu_count()

    loop = asyncio.get_event_loop_policy().new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()

    sync_position = start_block
    while sync_position <= end_block:
        sync_blocks = [i for i in range(sync_position, sync_position + cpu_count) if i <= end_block]

        loop.run_until_complete(call_coroutines(sync_blocks))

        sync_position = sync_blocks[-1] + 1

    loop.close()
