import enum

import pandas as pd

from api.Client import Client, Serializable
from engine.BaseTask import Task
from engine.sample.dummytest import APIRequest, APIResponse, APIScrapingStrategy


class JsonSerializeTask(Task):
    def __init__(self):
        super(JsonSerializeTask, self).__init__()
        JsonSerializeTask.register(JsonSerializeTask)


    def run(self):
        try:
            self.execute()
        except Exception as e:
            self._logger.error(f'Exception when execute the {self.__class__} task , {e}')

    def execute(self):
        self._logger.info('开启Json序列化模拟任务...')
        request = APIRequest('USAJobs')
        request.location = 'sf'
        request.keyword = 'python'
        request.set_parameters()
        self._logger.info(f'使用API名称: {request._APIName}...')
        self._logger.info(f'设置查询关键词: {request._keyword}...')
        self._logger.info(f'设置查询地点: {request._location}...')
        strategy = APIScrapingStrategy()
        client = Client(strategy)
        response = client.get_data(request)
        self._logger.info('获取数据成功，返回APIResponse对象...')
        self._logger.info(f'json数据共计页数: {response.PageNum}...')
        res = [response.df]
        if response.PageNum > 0:
            for i in range(1, response.PageNum):
                request.set_PageNum(i+1)
                res.append(client.get_data(request).df)
                self._logger.info(f'正在获取第{i+1}页数据 ...')
        self._logger.info('获取所有数据成功，合并data frame返回...')



    @enum.unique
    class Gender(enum.IntEnum):
        FEMALE = 0
        MALE = 1
