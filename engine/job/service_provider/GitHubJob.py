import datetime
import logging

import pandas as pd
from ibranch.scraping_scheduler.engine.client.HttpClient import ClientFactory
from ibranch.scraping_scheduler.util.Toolbox import LogicUtil

from api.Client import Request, Response, ScrapingStrategy, Deserializable


class GitHubJobRequest(Request):
    def __init__(self):
        super(GitHubJobRequest, self).__init__()
        Request.register(GitHubJobRequest)
        # Read only fields
        self._url = 'https://jobs.github.com/positions.json'

        # Dynamic fields
        self._keyword = None
        self._location = None
        self._full_time = None
        self._latitude = None
        self._longitude = None

    @property
    def url(self) -> str:
        return self._url

    @property
    def keyword(self) -> str:
        return self._keyword

    @keyword.setter
    def keyword(self, keyword: str):
        self._keyword = keyword

    @property
    def location(self) -> str:
        return self._location

    @location.setter
    def location(self, location: str):
        self._location = location

    @property
    def full_time(self) -> str:
        return self._full_time

    @full_time.setter
    def full_time(self, full_time: str):
        self._full_time = full_time

    @property
    def latitude(self) -> str:
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: str):
        self._latitude = latitude

    @property
    def longitude(self) -> str:
        return self._longitude

    @latitude.setter
    def longitude(self, longitude: str):
        self._longitude = longitude


class GithubJobDeserializable(Deserializable):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        super(GithubJobDeserializable, self).__init__()
        Deserializable.register(GithubJobDeserializable)

    def from_json(self, json_obj) -> pd.DataFrame:
        self._logger.info('json文件转换Data Frame中...')
        data_frame = pd.DataFrame.from_records(json_obj, index=range(len(json_obj)))
        data_frame['Source'] = 'GithubJobs'
        data_frame['Time'] = datetime.datetime.now()
        original_feature_names = [
            'Source'
            , 'id'
            , 'company'
            , 'DepartmentName'
            , 'title'
            , 'PositionRemuneration'
            , 'location'
            , 'JobCategory'
            , 'type'
            , 'description'
            , 'how_to_apply'
            , 'created_at'
            , 'ApplicationCloseDate'
            , 'url'
            , 'Time'
        ]
        for col_name in original_feature_names:
            if col_name not in data_frame.columns:
                data_frame[col_name] = None
        data_frame = data_frame[original_feature_names]
        # rename the column name
        data_frame.columns = [Deserializable.features]
        self._logger.info('Data Frame转换成功...')
        return data_frame


class GitHubJobResponse(Response):
    def __init__(self, response, records: pd.DataFrame):
        super(GitHubJobResponse, self).__init__()
        Response.register(GitHubJobResponse)
        self._response = response
        self._records = records

    @property
    def records(self) -> pd.DataFrame:
        return self._records

    @property
    def raw_response(self):
        return self._response


class GitHubJobScrapingStrategy(ScrapingStrategy, GithubJobDeserializable):
    def __init__(self):
        super(GitHubJobScrapingStrategy, self).__init__()
        ScrapingStrategy.register(GitHubJobScrapingStrategy)
        self._http_client = ClientFactory().build()

    def scrape(self, request: GitHubJobRequest) -> GitHubJobResponse:
        api = self._build_api_url(request)
        try:
            res = self._http_client.get(url=api)
            if None is res.response:
                self._logger.info("GitHubJob 访问异常. 返回值为空")
                return None
            if not res.is_success():
                self._logger.info("GitHubJob 访问异常. HTTP 状态码: %s" % res.status_code)
                return None
            self._logger.info("GitHubJob 访问成功")

            raw_json = res.json
            records = self.from_json(raw_json)
            return GitHubJobResponse(raw_json, records)
        except Exception as e:
            self._logger.error(f"GitHubJob 请求异常: {e}")
            return None

    def _build_parameter(self, request: GitHubJobRequest) -> str:
        if_else = lambda x: LogicUtil.if_else_default(x, '')
        return f"?description={if_else(request.keyword)}" \
               f"&location={if_else(request.location)}" \
               f"&full_time={if_else(request.full_time)}" \
               f"&lat={if_else(request.latitude)}" \
               f"&long={if_else(request.longitude)}"

    def _build_api_url(self, request: GitHubJobRequest) -> str:
        return f'%s%s' % (request.url, self._build_parameter(request))
