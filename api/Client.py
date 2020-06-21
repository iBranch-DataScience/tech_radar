import json
import logging
from abc import ABC, abstractmethod


class Serializable:

    def to_json(self):
        attributes = self.__dict__
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


class Request(ABC, Serializable):
    def __init__(self):
        pass


class Response(ABC, Serializable):
    def __init__(self):
        pass


class ScrapingStrategy(ABC):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)

    def scrape(self, request):
        return self.get_data(request)

    @abstractmethod
    def get_data(self, request: Request) -> Response:
        raise NotImplementedError()


class Client:
    def __init__(self, scraping_strategy: ScrapingStrategy):
        self._scraping_strategy = scraping_strategy

    def get_data(self, request: Request) -> Response:
        if not self._scraping_strategy:
            raise AttributeError('爬虫策略未指定')

        return self._scraping_strategy.scrape(request)
