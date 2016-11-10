from constance import config
from pymongo import MongoClient


def set_mongo_test_db(func):
    def func_wrapper(*args, **kwargs):
        config.MONGO_DATABASE_NAME = config.MONGO_TEST_DATABASE_NAME
        client = MongoClient()
        client.drop_database(config.MONGO_TEST_DATABASE_NAME)
        to_return = func(*args, **kwargs)
        client.drop_database(config.MONGO_TEST_DATABASE_NAME)
        return to_return
    return func_wrapper
