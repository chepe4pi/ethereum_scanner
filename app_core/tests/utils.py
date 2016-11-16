import django
from constance import config
from pymongo import MongoClient

# django.setup()


def set_mongo_test_db(func):
    def func_wrapper(*args, **kwargs):
        real_db = config.MONGO_DATABASE_NAME
        config.MONGO_DATABASE_NAME = config.MONGO_TEST_DATABASE_NAME
        client = MongoClient()
        client.drop_database(config.MONGO_TEST_DATABASE_NAME)

        to_return = func(*args, **kwargs)

        client.drop_database(config.MONGO_TEST_DATABASE_NAME)
        # TODO I have to find other way
        config.MONGO_DATABASE_NAME = real_db
        return to_return
    return func_wrapper
