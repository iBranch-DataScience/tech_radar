import logging
from typing import Iterable

import pandas as pd
from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.engine.client.HttpClient import ClientFactory
from ibranch.scraping_scheduler.util.Toolbox import LogicUtil, Formatter

from api.Client import Request, Response, ScrapingStrategy, Deserializable
from domain.Entity import RecruitingRecord
from util.Toolbox import CONSTANT


class USAJobRequest(Request):
    def __init__(self):
        super(USAJobRequest, self).__init__()
        Request.register(USAJobRequest)
        # Read only fields
        self._url = 'https://data.usajobs.gov/api/search'
        self._host = 'data.usajobs.gov'
        self._user_agent = Configuration().getProperty(f'jobs.list.USAJob.user_agent')
        self._auth_key = Configuration().getProperty(f'jobs.list.USAJob.auth_key')

        # Dynamic fields
        self._job_category_code = None
        self._keyword = None
        self._location = None
        self._page_num = None
        self._results_per_page = 500

    @property
    def url(self) -> str:
        return self._url

    @property
    def host(self) -> str:
        return self._host

    @property
    def user_agent(self) -> str:
        return self._user_agent

    @property
    def auth_key(self) -> str:
        return self._auth_key

    @property
    def job_category_code(self) -> str:
        return self._job_category_code

    @job_category_code.setter
    def job_category_code(self, job_category_code: str):
        self._job_category_code = job_category_code

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
    def page_num(self) -> int:
        return self._page_num

    @page_num.setter
    def page_num(self, page_num: int):
        self._page_num = page_num

    @property
    def results_per_page(self) -> int:
        return self._results_per_page

    @results_per_page.setter
    def results_per_page(self, results_per_page: int):
        self._results_per_page = results_per_page


class USAJobDeserializable(Deserializable):
    features = [
        'Source'
        , 'PositionID'
        , 'OrganizationName'
        , 'DepartmentName'
        , 'PositionTitle'
        , 'PositionRemuneration'
        , 'PositionLocation'
        , 'JobCategory'
        , 'PositionSchedule'
        , 'Description'
        , 'HowToApply'
        , 'ApplyURI'
        , 'PublicationStartDate'
        , 'ApplicationCloseDate'
        , 'Time'
    ]

    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        super(USAJobResponse, self).__init__()
        Deserializable.register(USAJobResponse)

    def from_json(self, json_obj) -> Iterable[RecruitingRecord]:
        self._logger.info('json文件转换Data Frame中...')
        # transform json to data frame
        elements = json_obj['SearchResult']['SearchResultItems']
        elements = [e['MatchedObjectDescriptor'] for e in elements]

        jobs = pd.DataFrame.from_dict(elements)
        job_discriptions = pd.DataFrame.from_dict(jobs.UserArea.tolist())
        job_discriptions = pd.DataFrame.from_dict(job_discriptions.Details.tolist())
        jobs.loc[:, 'Source'] = CONSTANT.usa_job()
        jobs.loc[:, 'Time'] = Formatter.get_timestamp('%Y%m%d%H%M%S')
        jobs.loc[:, 'Description'] = "QualificationSummary:" + jobs.QualificationSummary.astype(str) \
                                     + " MajorDuties:" + job_discriptions.MajorDuties.astype(str) \
                                     + " Requirements:" + job_discriptions.Requirements.astype(str) \
                                     + " Evaluations:" + job_discriptions.Evaluations.astype(str) \
                                     + " WhatToExpectNext:" + job_discriptions.WhatToExpectNext.astype(str) \
                                     + " RequiredDocuments:" + job_discriptions.RequiredDocuments.astype(str) \
                                     + " Benefits:" + job_discriptions.Benefits.astype(str) \
                                     + " JobSummary:" + job_discriptions.JobSummary.astype(str) \
                                     + " OtherInformation:" + job_discriptions.OtherInformation.astype(str) \
                                     + " Benefits:" + job_discriptions.Benefits.astype(str)
        jobs.loc[:, 'HowToApply'] = job_discriptions.HowToApply

        jobs = jobs.loc[:, USAJobDeserializable.features]
        jobs.columns = RecruitingRecord.features
        self._logger.info('Data Frame转换成功...')
        return list(jobs.apply(self._to_recruiting_record, axis=1))

    def _to_recruiting_record(self, row: pd.Series) -> RecruitingRecord:
        record = RecruitingRecord()
        for key, value in row.to_dict().items():
            setattr(record, key, value)
        return record


class USAJobResponse(Response):
    def __init__(self, response, records: pd.DataFrame, page_num: str):
        super(USAJobResponse, self).__init__(response, records)
        Response.register(USAJobResponse)
        self._page_num = page_num

    @property
    def page_num(self) -> int:
        return self._page_num


class USAJobScrapingStrategy(ScrapingStrategy, USAJobDeserializable):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        super(USAJobScrapingStrategy, self).__init__()
        ScrapingStrategy.register(USAJobScrapingStrategy)
        USAJobDeserializable.register(USAJobScrapingStrategy)
        self._http_client = ClientFactory().build()

    @ScrapingStrategy.save_record('raw_usa_job')
    def scrape(self, request: USAJobRequest) -> USAJobResponse:
        api = self._build_api_url(request)
        headers = self._build_headers(request)
        try:
            res = self._http_client.get(url=api, headers=headers)

            if None is res.response:
                self._logger.info("USAJob 访问异常. 返回值为空")
                return None
            if not res.is_success():
                self._logger.info("USAJob 访问异常. HTTP 状态码: %s" % res.status_code)
                return None
            self._logger.info("USAJob 访问成功")

            raw_json = res.json
            # Note: The number of results returned per request defaults to 25
            # but can be defined in your request up to 500 per request.
            page_num = int(raw_json['SearchResult']['UserArea']['NumberOfPages'])
            records = self.from_json(raw_json)
            return USAJobResponse(raw_json, records, page_num)
        except Exception as e:
            self._logger.error(f"USAJob 请求异常: {e}")
            return None

    def _build_parameter(self, request: USAJobRequest) -> str:
        if_else = lambda x: LogicUtil.if_else_default(x, '')
        return f"?JobCategoryCode={if_else(request.job_category_code)}" \
               f"&Keyword={if_else(request.keyword)}" \
               f"&LocationName={if_else(request.location)}" \
               f"&ResultsPerPage={if_else(request.results_per_page)}" \
               f"&Page={if_else(request.page_num)}"

    def _build_headers(self, request: USAJobRequest) -> dict:
        header = dict()
        header["Host"] = request.host
        header["User-Agent"] = request.user_agent
        header["Authorization-Key"] = request.auth_key
        return header

    def _build_api_url(self, request: USAJobRequest) -> str:
        return f'%s%s' % (request.url, self._build_parameter(request))
