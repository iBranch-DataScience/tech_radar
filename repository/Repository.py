import logging

from singleton_decorator import singleton

from repository.DatabaseDriver import MongoDriver


@singleton
class Repository:
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        self._client = MongoDriver().get_client()

    def idempotent_insert(self, doc_name, md5_code, json_dict):
        exist = Repository().check_md5_existance(doc_name, md5_code)
        if exist:
            self._logger.info(f'数据已存在. doc name: {doc_name}, md5: {md5_code}')
            return None
        return self._client[doc_name].insert_one(json_dict).inserted_id

    def check_md5_existance(self, doc_name, md5_code):
        return True if self._client[doc_name].find({'md5': md5_code}).count() > 0 else False
