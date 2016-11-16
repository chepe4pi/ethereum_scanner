from django.apps import AppConfig
from raven.contrib.django.raven_compat.models import client


class AppCoreConfig(AppConfig):
    name = 'app_core'

    def ready(self):
        client.captureException()
