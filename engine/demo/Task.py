import logging
import time

from scraping_scheduler.ibranch.engine.client.SeleniumClient import SeleniumClientBuilder
from scraping_scheduler.ibranch.util.DataTraffic import FlowShaper


class Task:
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        self._driver = None

    @property
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    def run(self):
        try:
            self.execute()
        except Exception as e:
            self._logger.error(f'Exception when execute the {self.__class__} task , {e}')
        finally:
            FlowShaper().get(self.cache_name).release()

    def execute(self):
        raise NotImplementedError()


class OpenIBranchLinkedInTask(Task):
    def __init__(self, act):
        super(OpenIBranchLinkedInTask, self).__init__()
        self.act = act
        self._selenium_client = None

    def execute(self):
        try:
            self._logger.info(f'开始扫描 url: {self.act.url}')
            self._selenium_client = SeleniumClientBuilder().build()
            time.sleep(2)
            # Open www.google.com
            self._selenium_client.open_url(self.act.url)
            time.sleep(2)
            # Search linkedIn
            self._selenium_client.input_text('ibranch ', 'q')
            time.sleep(1)
            self._selenium_client.input_text('syracuse', 'q')
            # Open the link
            time.sleep(2)
            self._selenium_client.enter()
            # Search for iBranch
            # Open the link
            time.sleep(2)
            self._selenium_client.click('cssa-ibranch')
            time.sleep(3)
            for idx in range(1000):
                self._selenium_client.execute_script(f"window.scrollTo(0, {idx})")

            pass
        except Exception as e:
            self._logger.error(f'扫描异常: {e}')
        finally:
            self._logger.info('扫描完成!')
            pass
