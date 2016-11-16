from django.apps import AppConfig
from constance import config
from mongoengine import connect


class AppCoreConfig(AppConfig):
    name = 'app_core'

    def ready(self):
        connect(config.MONGO_DATABASE_NAME)
