from ibranch.scraping_scheduler.domain.Profile import Domain


class Action(Domain):
    def __init__(self):
        super(Action, self).__init__()
        self._url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url
