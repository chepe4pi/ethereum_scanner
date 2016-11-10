import os

import celery
import raven
from raven.contrib.celery import register_logger_signal, register_signal


class RavenCelery(celery.Celery):
    def on_configure(self):
        client = raven.Client(os.getenv('SENTRY_KEY'))

        register_logger_signal(client)

        register_signal(client)
