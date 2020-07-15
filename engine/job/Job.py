from ibranch.scraping_scheduler.engine.job.Base import BaseJob
from ibranch.scraping_scheduler.scheduler.executor.TaskExecutor import ThreadExecutor as TaskExecutor
from ibranch.scraping_scheduler.util.DataTraffic import FlowShaper

from engine.job.Task import USAJobTask, GitHubJobTask
from util.Toolbox import CONSTANT


class USAJob(BaseJob):
    def __init__(self):
        super(USAJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(USAJob)

    # Run under interval
    def run(self):
        self.logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            task = USAJobTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())

            TaskExecutor().submit_tasks(type(self).__name__, [task])
            self.logger.info(f"任务已启动. ")
        else:
            self.logger.info(f"任务启动失败. ")


class GitHubJob(BaseJob):
    def __init__(self):
        super(GitHubJob, self).__init__(CONSTANT.global_throttle())
        BaseJob.register(GitHubJob)

    # Run under interval
    def run(self):
        self.logger.info("<<<iBranch 技术雷达 presents>>>")

        flow_shaper = FlowShaper().get(self.cache_name)
        if flow_shaper.acquire():
            task = GitHubJobTask()
            task.register_post_exec(lambda: FlowShaper().get(self.cache_name).release())

            TaskExecutor().submit_tasks(type(self).__name__, [task])
            self.logger.info(f"任务已启动. ")
        else:
            self.logger.info(f"任务启动失败. ")
