from singleton_decorator import singleton

from repository.DatabaseDriver import MongoDriver


@singleton
class Repository:
    def __init__(self):
        self._client = MongoDriver().get_client()

    def insert_raw_data(self, doc_name, json):
        return self._client[doc_name].insert_one(json)


