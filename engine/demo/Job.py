from queue import Queue

from scraping_scheduler.ibranch.domain.System import CONSTANT, Cache
from scraping_scheduler.ibranch.engine.job.Base import BaseJob

from domain.Entity import Action
from engine.BaseTask import *
from engine.demo.Task import OpenIBranchLinkedInTask


class PresentationJob(BaseJob):
    def __init__(self):
        super(PresentationJob, self).__init__(CONSTANT.presentation())
        BaseJob.register(PresentationJob)
        self._logger = logging.getLogger(type(self).__name__)
        cache_catelog = Cache().get_new_cache(Queue)
        Cache().register_catelog(self.cache_name, cache_catelog)
        self.mock_cache_initialization()

    @property
    def job_class(self):
        return "presentation"

    def mock_cache_initialization(self):
        act = Action()
        act.url = 'http://www.google.com'
        cache = Cache().get_existing_cache(self.cache_name)
        cache.put(act, block=False)

    # Run under interval
    def run(self):
        self._logger.info("<<<iBranch 技术雷达 presents>>>")

        cache = Cache().get_existing_cache(self.cache_name)
        act = cache.get_nowait()

        task = OpenIBranchLinkedInTask(act)

        from scraping_scheduler.ibranch.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
        TaskExecutor().submit_tasks(self.cache_name, [task])
        self._logger.info(f"任务已启动. ")
