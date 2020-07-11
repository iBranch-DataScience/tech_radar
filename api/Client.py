import json
import logging
from abc import ABC, abstractmethod


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
    features = [
        'Source'
        , 'PositionID'
        , 'OrganizationName'
        , 'DepartmentName'
        , 'PositionTitle'
        , 'PositionRemuneration'
        , 'PositionLocation'
        , 'JobCategory'
        , 'PositionSchedule'
        , 'Description'
        , 'HowToApply'
        , 'ApplyURI'
        , 'PublicationStartDate'
        , 'ApplicationCloseDate'
        , 'Time'
    ]

    def from_json(self, json_obj):
        raise NotImplementedError()


class Request(ABC):
    def __init__(self):
        pass


class Response(ABC):
    def __init__(self):
        pass


class ScrapingStrategy(ABC):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)

    @abstractmethod
    def scrape(self, request: Request) -> Response:
        raise NotImplementedError()


class Client:
    def __init__(self, scraping_strategy: ScrapingStrategy):
        self._scraping_strategy = scraping_strategy

    def get_data(self, request: Request) -> Response:
        if not self._scraping_strategy:
            raise AttributeError('爬虫策略未指定')

        return self._scraping_strategy.scrape(request)
