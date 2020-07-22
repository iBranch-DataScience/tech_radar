import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Iterable

import pandas as pd

from domain.Entity import RecruitingRecord, ScrapingLog
from repository.Repository import Repository, ScrapingLogRepository
from util.Toolbox import MD5Encoder


class Serializable(ABC):
    def to_json(self):
        raise NotImplementedError()


class JsonSerializable(Serializable):
    def __init__(self):
        super(JsonSerializable, self).__init__()
        Serializable.register(JsonSerializable)

    def to_json(self, obj: object):
        attributes = obj.__dict__
        self._convert_key(attributes)
        return json.dumps(attributes)

    def _convert_key(self, attributes: dict):
        for k, v in attributes.items():
            if str(k).startswith('_'):
                attributes[k[1:]] = attributes[k]
                del attributes[k]
                k = k[1:]
            if isinstance(attributes[k], dict):
                self._convert_key(attributes[k])


class Deserializable(ABC):
    def from_json(self, json_obj) -> Iterable[RecruitingRecord]:
        raise NotImplementedError()


class Request(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def keyword(self) -> str:
        raise NotImplementedError()


class Response(ABC):
    def __init__(self, response, records: pd.DataFrame, http_code: int):
        self._response = response
        self._records = records
        self._http_code = http_code

    @property
    def records(self) -> pd.DataFrame:
        return self._records

    @property
    def raw_response(self):
        return self._response

    @property
    def http_code(self):
        return self._http_code


class ScrapingStrategy(ABC):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)

    @abstractmethod
    def scrape(self, request: Request) -> Response:
        raise NotImplementedError()

    @staticmethod
    def save_record(portal_name):
        def _record_raw_data(func):
            def wrapper_func(*args, **kwargs):
                try:
                    x = func(*args, **kwargs)

                    md5_code = MD5Encoder.encode_json(x.raw_response)

                    raw_doc_id = Repository().idempotent_insert(portal_name, md5_code, {
                        'md5': md5_code,
                        'raw_data': x.raw_response,
                    })

                    if not raw_doc_id:
                        return x

                    for record in x.records:
                        md5_code = MD5Encoder.encode_json(record.to_dict())
                        record.raw_doc_id = raw_doc_id
                        Repository().idempotent_insert('recruiting_record', md5_code, {
                            'md5': md5_code,
                            **record.to_dict()
                        })

                    return x
                except Exception as e:
                    comment = str(e)
                finally:
                    try:
                        comment
                    except NameError:
                        comment = None

                    request = args[1]
                    log_record = ScrapingLog()
                    log_record.recruiting_record_id = raw_doc_id
                    log_record.raw_data_id = raw_doc_id
                    log_record.url = request.url
                    log_record.keyword = request.keyword
                    log_record.ts = datetime.now()
                    log_record.http_code = x.http_code
                    log_record.comment = comment

                    ScrapingLogRepository().log(log_record)
            return wrapper_func
        return _record_raw_data


class Client:
    def __init__(self, scraping_strategy: ScrapingStrategy):
        self._scraping_strategy = scraping_strategy

    def get_data(self, request: Request) -> Response:
        if not self._scraping_strategy:
            raise AttributeError('爬虫策略未指定')

        return self._scraping_strategy.scrape(request)
