import os

import time

from constance import config
from mongoengine import connect
from mongoengine.connection import disconnect

from app_core.celery_raven_class import RavenCelery
from app_core.connectors import RpcServerConnector
from app_sync.sync_rpc_server import sync_block_and_txs

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethereum_scanner.settings')

app = RavenCelery('ethereum_scanner',
                  broker='redis://', )

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def set_web3_filter_task(self):
    while True:
        sync_blocks_from_position_to_end()
        time.sleep(config.TIME_TO_SLEEP_BEFORE_CHECK_BLOCKS)


def sync_blocks_from_position_to_end():
    web3 = RpcServerConnector().get_connection()
    last_block = web3.eth.blockNumber
    current_block = config.SYNC_BLOCKS_POSITION
    connect(config.MONGO_DATABASE_NAME)

    while current_block < last_block:
        connect(config.MONGO_DATABASE_NAME)

        sync_block_and_txs(current_block, web3)
        current_block += 1
        config.SYNC_BLOCKS_POSITION = current_block
    disconnect(config.MONGO_DATABASE_NAME)


if __name__ == '__main__':
    app.start()
    set_web3_filter_task.delay()
