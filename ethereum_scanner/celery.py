import os

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
    web3 = RpcServerConnector().get_connection()
    new_block_filter = web3.eth.filter('latest')
    new_block_filter.watch(sync_block_and_txs)


set_web3_filter_task.delay()

# if __name__ == '__main__':
#     app.start()
#     print('a')
#     debug_task()
