from mongoengine import connect

from ethereum_scanner.settings import MONGO_DATABASE_NAME
from .celery import app as celery_app

__all__ = ['celery_app']

connect(MONGO_DATABASE_NAME)
