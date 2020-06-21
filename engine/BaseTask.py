import logging
from abc import ABC, abstractmethod
from typing import Callable

from api.Client import Client


class Task(ABC):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        self._client = None
        self._pre_exec = None
        self._post_exec = None

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: Client):
        self._client = client

    def run(self):
        try:
            self.pre_exec()
            self.execute()
        except Exception as e:
            self._logger.error(f'Exception when execute the {self.__class__} task , {e}')
        finally:
            self.post_exec()

    def register_pre_exec(self, func: Callable):
        self._pre_exec = func

    def register_post_exec(self, func: Callable):
        self._post_exec = func

    def pre_exec(self):
        if self._pre_exec:
            self._pre_exec()

    def post_exec(self):
        if self._post_exec:
            self._post_exec()

    @abstractmethod
    def execute(self):
        raise NotImplementedError()
