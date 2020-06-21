import enum

from api.Client import Client, Serializable
from engine.BaseTask import Task
from engine.sample.DummyClass import DummyRequest, DummyScrapingStrategy


class JsonSerializeTask(Task):
    def __init__(self):
        super(JsonSerializeTask, self).__init__()
        JsonSerializeTask.register(JsonSerializeTask)

    def execute(self):
        self._logger.info('开启Json序列化模拟任务')
        request = DummyRequest()
        request.name = '老何'
        request.gender = JsonSerializeTask.Gender.MALE
        self._logger.info(f'Request 转 Json: {request.to_json()}')
        strategy = DummyScrapingStrategy()
        client = Client(strategy)
        response = client.get_data(request)
        self._logger.info(f'Response 转 Json: {response.to_json()}')

    @enum.unique
    class Gender(enum.IntEnum):
        FEMALE = 0
        MALE = 1
