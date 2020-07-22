from queue import Queue, Empty

from ibranch.scraping_scheduler.domain.System import Cache
from ibranch.scraping_scheduler.engine.job.Base import BaseJob
from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
from ibranch.scraping_scheduler.util.DataTraffic import FlowShaper

from engine.job.Task import USAJobTask, GitHubJobTask
from repository.Repository import ScrapingLogRepository
from util.Toolbox import CONSTANT


class InitializationJob(BaseJob):
    def __init__(self):
        super(InitializationJob, self).__init__()
        BaseJob.register(InitializationJob)
        self._job_register = list()
        self.register()

    def run(self):
        self.logger.info(f'填充缓存 {type(self).__name__}')

        keywords = ScrapingLogRepository().get_pending_keywords()
        for job in self._job_register:
            cache = Cache().get_existing_cache(job)
            [cache.put(keyword) for keyword in keywords if keyword not in cache.queue]

    def register(self):
        self._register(USAJob.__name__)
        self._register(GitHubJob.__name__)

    def _register(self, cache_name: BaseJob):
        self._job_register.append(cache_name)
        cache_catalog = Cache().get_new_cache(Queue)
        Cache().register_catelog(cache_name, cache_catalog)


class USAJob(BaseJob):
    def __init__(self):
        super(USAJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(USAJob)

    # Run under interval
    def run(self):
        self.logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if not flow_shaper.acquire():
            self.logger.info(f"任务列表已满")

        try:
            keyword = Cache().get_existing_cache(type(self).__name__).get_nowait()
        except Empty:
            self.logger.info(f"任务启动失败, 缓存无数据.")
        else:
            task = USAJobTask(keyword)
            task.register_post_exec(self.log_scraping_result)

            TaskExecutor().submit_tasks(type(self).__name__, [task])
            self.logger.info(f"任务已启动. ")

    def log_scraping_result(self):
        FlowShaper().get(self.cache_name).release()


class GitHubJob(BaseJob):
    def __init__(self):
        super(GitHubJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(GitHubJob)
        cache_catalog = Cache().get_new_cache(Queue)
        Cache().register_catelog(type(self).__name__, cache_catalog)

    # Run under interval
    def run(self):
        self.logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if not flow_shaper.acquire():
            self.logger.info(f"任务列表已满")

        try:
            keyword = Cache().get_existing_cache(type(self).__name__).get_nowait()
        except Empty:
            self.logger.info(f"任务启动失败, 缓存无数据.")
        else:
            task = GitHubJobTask(keyword)
            task.register_post_exec(self.log_scraping_result)

            TaskExecutor().submit_tasks(type(self).__name__, [task])
            self.logger.info(f"任务已启动. ")

    def log_scraping_result(self):
        FlowShaper().get(self.cache_name).release()
