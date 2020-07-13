import logging
from queue import Queue

import pandas as pd
from ibranch.scraping_scheduler.domain.System import Cache
from ibranch.scraping_scheduler.engine.job.Base import BaseJob
from ibranch.scraping_scheduler.util.DataTraffic import FlowShaper

from engine.job.Task import USAJobTask, GitHubJobTask
from util.Toolbox import CONSTANT, Keyword
from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor


class USAJob(BaseJob):
    def __init__(self):
        super(USAJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(USAJob)
        self._logger = logging.getLogger(type(self).__name__)
        cache_catelog = Cache().get_new_cache(Queue)
        Cache().register_catelog(self.cache_name, cache_catelog)

        # keywords = Keyword().get_combination_str()
        # Cache().register_catelog("keywords", keywords)
        # print(keywords[0])
    # Run under interval
    def run(self):
        self._logger.info("<<<iBranch 技术雷达 presents>>>")
        # keyword row numbers
        # len_keywords = len(Cache().get_existing_cache("keywords"))
        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            # for i in range(0, len_keywords):
            #     current_keyword = Cache().get_existing_cache("keywords")[i]
            # task = USAJobTask(keyword=current_keyword)
            task = USAJobTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())
            TaskExecutor().submit_tasks(type(self).__name__, [task])
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

    # Run under interval
    def run(self):
        self._logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            task = GitHubJobTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())

            from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
            TaskExecutor().submit_tasks(type(self).__name__, [task])
            self._logger.info(f"任务已启动. ")
        else:
            self._logger.info(f"任务启动失败. ")
