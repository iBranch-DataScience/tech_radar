from api.Client import Client
from engine.BaseTask import Task
from engine.job.service_provider.GitHubJob import GitHubJobScrapingStrategy, GitHubJobRequest

from engine.job.service_provider.USAJob import USAJobScrapingStrategy, USAJobRequest


class USAJobTask(Task):
    def __init__(self):
        super(USAJobTask, self).__init__()
        Task.register(USAJobTask)
        self._client = Client(USAJobScrapingStrategy())

    def execute(self):
        self._logger.info('开始获取USAJob 的数据...')
        request = USAJobRequest()
        request.keyword = 'python'
        request.location = 'sf'
        request.page_num = 1
        self._logger.info(f'设置查询关键词: {request._keyword}...')
        self._logger.info(f'设置查询地点: {request._location}...')
        response = self._client.get_data(request)
        self._logger.info('获取数据成功，返回USAJobResponse对象...')
        self._logger.info(f'json数据共计页数: {response.page_num}...')
        self._logger.info(response.records)


class GitHubJobTask(Task):
    def __init__(self):
        super(GitHubJobTask, self).__init__()
        Task.register(GitHubJobTask)
        self._client = Client(GitHubJobScrapingStrategy())

    def execute(self):
        self._logger.info('开始获取GitHubJob 的数据...')
        request = GitHubJobRequest()
        request.keyword = 'python'
        request.location = 'sf'
        request.page_num = 1
        self._logger.info(f'设置查询关键词: {request._keyword}...')
        self._logger.info(f'设置查询地点: {request._location}...')
        response = self._client.get_data(request)
        self._logger.info('获取数据成功，返回GitHubJobResponse对象...')
        self._logger.info(response.records)
