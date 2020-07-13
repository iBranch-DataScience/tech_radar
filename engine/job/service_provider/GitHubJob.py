import logging
from typing import Iterable

import pandas as pd
from ibranch.scraping_scheduler.engine.client.HttpClient import ClientFactory
from ibranch.scraping_scheduler.util.Toolbox import LogicUtil, Formatter

from api.Client import Request, Response, ScrapingStrategy, Deserializable
from domain.Entity import RecruitingRecord
from util.Toolbox import CONSTANT


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
    features = [
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

    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        super(GithubJobDeserializable, self).__init__()
        Deserializable.register(GithubJobDeserializable)

    def from_json(self, json_obj) -> Iterable[RecruitingRecord]:
        self._logger.info('json文件转换Data Frame中...')
        data_frame = pd.DataFrame.from_records(json_obj)
        data_frame['Source'] = CONSTANT.github_job()
        data_frame['Time'] = Formatter.get_timestamp('%Y%m%d%H%M%S')

        for col_name in GithubJobDeserializable.features:
            if col_name not in data_frame.columns:
                data_frame[col_name] = None

        data_frame = data_frame[GithubJobDeserializable.features]
        # rename the column name
        data_frame.columns = RecruitingRecord.features
        self._logger.info('Data Frame转换成功...')

        return list(data_frame.apply(self._to_recruiting_record, axis=1))

    def _to_recruiting_record(self, row: pd.Series) -> RecruitingRecord:
        record = RecruitingRecord()
        for key, value in row.to_dict().items():
            setattr(record, key, value)
        return record


class GitHubJobResponse(Response):
    def __init__(self, response, records: pd.DataFrame):
        super(GitHubJobResponse, self).__init__(response, records)
        Response.register(GitHubJobResponse)


class GitHubJobScrapingStrategy(ScrapingStrategy, GithubJobDeserializable):
    def __init__(self):
        super(GitHubJobScrapingStrategy, self).__init__()
        ScrapingStrategy.register(GitHubJobScrapingStrategy)
        self._http_client = ClientFactory().build()

    @ScrapingStrategy.save_record('raw_github_job')
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
