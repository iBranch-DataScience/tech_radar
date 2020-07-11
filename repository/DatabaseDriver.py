from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from pymongo import MongoClient, WriteConcern
from singleton_decorator import singleton


@singleton
class MongoDriver:
    def __init__(self):
        cfg = Configuration(None)
        ip = cfg.getProperty("mongodb.ip")
        port = cfg.getProperty("mongodb.port")
        user_name = cfg.getProperty("mongodb.user_name")
        password = cfg.getProperty("mongodb.password")
        self._db_name = cfg.getProperty("mongodb.db_name")

        # password = Cryptor.decode(password)
        # password = Cryptor.decode(password)
        # self._mongo_client = MongoClient(f"mongodb://{user_name}:{password}@{ip}:{port}/")
        self._mongo_client = MongoClient(ip, port)

    def get_client(self):
        wc_majority = WriteConcern("0", wtimeout=1000)
        return self._mongo_client.get_database(self._db_name)

    def close(self):
        self._mongo_client.close()

    def __exit__(self):
        self.close()
