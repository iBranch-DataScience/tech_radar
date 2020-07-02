import logging
from queue import Queue

from ibranch.scraping_scheduler.domain.System import CONSTANT, Cache
from ibranch.scraping_scheduler.engine.job.Base import BaseJob
from ibranch.scraping_scheduler.util.DataTraffic import FlowShaper

from engine.sample.Task import JsonSerializeTask


class SampleJob(BaseJob):
    def __init__(self):
        super(SampleJob, self).__init__(CONSTANT.sample())
        BaseJob.register(SampleJob)
        self._logger = logging.getLogger(type(self).__name__)
        cache_catelog = Cache().get_new_cache(Queue)
        Cache().register_catelog(self.cache_name, cache_catelog)

    @property
    def job_class(self):
        return "presentation"

    # Run under interval
    def run(self):
        self._logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            task = JsonSerializeTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())

            from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
            TaskExecutor().submit_tasks(self.cache_name, [task])
            self._logger.info(f"任务已启动. ")
        else:
            self._logger.info(f"任务启动失败. ")
