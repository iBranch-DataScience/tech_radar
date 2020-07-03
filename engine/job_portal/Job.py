import logging
from queue import Queue

from ibranch.scraping_scheduler.domain.System import Cache
from ibranch.scraping_scheduler.engine.job.Base import BaseJob
from ibranch.scraping_scheduler.util.DataTraffic import FlowShaper

from engine.job_portal.Task import USAJobTask, GitHubJobTask
from util.Toolbox import CONSTANT


class USAJob(BaseJob):
    def __init__(self):
        super(USAJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(USAJob)
        self._logger = logging.getLogger(type(self).__name__)
        cache_catelog = Cache().get_new_cache(Queue)
        Cache().register_catelog(self.cache_name, cache_catelog)

    @property
    def job_class(self):
        return "usajob"

    # Run under interval
    def run(self):
        self._logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            task = USAJobTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())

            from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
            TaskExecutor().submit_tasks(self.__class__.__name__, [task])
            self._logger.info(f"任务已启动. ")
        else:
            self._logger.info(f"任务启动失败. ")


class GitHubJob(BaseJob):
    def __init__(self):
        super(GitHubJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(GitHubJob)
        self._logger = logging.getLogger(type(self).__name__)
        cache_catelog = Cache().get_new_cache(Queue)
        Cache().register_catelog(self.cache_name, cache_catelog)

    @property
    def job_class(self):
        return "githubjob"

    # Run under interval
    def run(self):
        self._logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            task = GitHubJobTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())

            from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
            TaskExecutor().submit_tasks(self.__class__.__name__, [task])
            self._logger.info(f"任务已启动. ")
        else:
            self._logger.info(f"任务启动失败. ")