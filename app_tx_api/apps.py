from django.apps import AppConfig, config
from mongoengine import connect


class AppTxApiConfig(AppConfig):
    name = 'app_tx_api'

    def ready(self):
        connect(config.MONGO_DATABASE_NAME)
