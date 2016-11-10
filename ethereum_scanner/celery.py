import os

import time

from constance import config
from mongoengine import connect

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
        web3 = RpcServerConnector().get_connection()
        last_block = web3.eth.blockNumber
        current_block = config.SYNC_BLOCKS_POSITION
        while current_block < last_block:
            connect(config.MONGO_DATABASE_NAME)
            sync_block_and_txs(current_block, web3)
            current_block += 1
            config.SYNC_BLOCKS_POSITION = current_block
        connect(config.MONGO_DATABASE_NAME)
        time.sleep(10)


set_web3_filter_task.delay()

if __name__ == '__main__':
    app.start()
# print('a')
#     debug_task()
