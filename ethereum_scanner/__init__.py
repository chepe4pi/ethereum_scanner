from constance import config
from mongoengine import connect
import django

from .celery import app as celery_app

__all__ = ['celery_app']

django.setup()
connect(config.MONGO_DATABASE_NAME)
