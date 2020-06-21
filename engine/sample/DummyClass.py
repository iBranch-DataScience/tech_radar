from api.Client import Request, Response, ScrapingStrategy


class DummyRequest(Request):
    def __init__(self):
        super(DummyRequest, self).__init__()
        Request.register(DummyRequest)
        self._name = None
        self._gender = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender


class DummyResponse(Response):
    def __init__(self):
        super(DummyResponse, self).__init__()
        Response.register(DummyResponse)
        self._language = None
        self._level = None

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level


class DummyScrapingStrategy(ScrapingStrategy):
    def __init__(self):
        super(DummyScrapingStrategy, self).__init__()
        ScrapingStrategy.register(DummyScrapingStrategy)
        self._language = None
        self._level = None

    def get_data(self, request: Request) -> Response:
        response = DummyResponse()
        response.language = 'Python3'
        response.level = 5
        self._logger.info('模拟爬取数据...')
        return response
