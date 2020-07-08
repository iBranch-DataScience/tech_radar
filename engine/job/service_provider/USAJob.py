import logging
import time

import pandas as pd
from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.engine.client.HttpClient import ClientFactory
from ibranch.scraping_scheduler.util.Toolbox import LogicUtil

from api.Client import Request, Response, ScrapingStrategy, Deserializable
import datetime

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
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        super(USAJobResponse, self).__init__()
        Deserializable.register(USAJobResponse)

    def from_json(self, json_obj) -> pd.DataFrame:
        self._logger.info('json文件转换Data Frame中...')
        # transform json to data frame
        elements = json_obj['SearchResult']['SearchResultItems']
        # list
        feature_names = {
            'PositionID'
            , 'PositionTitle'
            , 'ApplyURI'
            , 'PositionLocation'
            , 'OrganizationName'
            , 'DepartmentName'
            , 'JobCategory'
            , 'PositionSchedule'
            , 'PositionRemuneration'
            , 'PublicationStartDate'
            , 'ApplicationCloseDate'
        }
        row_records = [
            {
                key: value for key, value in element['MatchedObjectDescriptor'].items() if key in feature_names
            } for element in elements
        ]
        how_to_apply_records = [
            element['MatchedObjectDescriptor']['UserArea']['Details']['HowToApply']
            for element in elements

        ]
        description_records = [
            self._concat_description(element)
            for element in elements
        ]
        data_frame = pd.DataFrame(row_records)
        data_frame['HowToApply'] = how_to_apply_records
        data_frame['Description'] = description_records
        data_frame['Source'] = 'USAJobs'
        data_frame['Time'] = datetime.datetime.now()
        data_frame = data_frame[
            [
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
        ]

        self._logger.info('Data Frame转换成功...')
        return data_frame

    def _concat_description(self, element):
        qualification_summary = element['MatchedObjectDescriptor']['QualificationSummary']
        inner_dict = element['MatchedObjectDescriptor']['UserArea']['Details']
        return f"QualificationSummary:{qualification_summary}" \
               f"MajorDuties:{inner_dict['MajorDuties']}" \
               f"Requirements:{inner_dict['Requirements']}" \
               f"Evaluations:{inner_dict['Evaluations']}" \
               f"WhatToExpectNext:{inner_dict['WhatToExpectNext']}" \
               f"RequiredDocuments:{inner_dict['RequiredDocuments']}" \
               f"Benefits:{inner_dict['Benefits']}" \
               f"JobSummary:{inner_dict['JobSummary']}" \
               f"OtherInformation:{inner_dict['OtherInformation']}" \
               f"Benefits:{inner_dict['Benefits']}"


class USAJobResponse(Response):
    def __init__(self, response, page_num: str, records: pd.DataFrame):
        super(USAJobResponse, self).__init__()
        Response.register(USAJobResponse)
        self._response = response
        self._page_num = page_num
        self._records = records

    @property
    def records(self) -> pd.DataFrame:
        return self._records

    @property
    def raw_response(self):
        return self._response

    @property
    def page_num(self) -> int:
        return self._page_num


class USAJobScrapingStrategy(ScrapingStrategy, USAJobDeserializable):
    def __init__(self):
        self._logger = logging.getLogger(type(self).__name__)
        super(USAJobScrapingStrategy, self).__init__()
        ScrapingStrategy.register(USAJobScrapingStrategy)
        self._http_client = ClientFactory().build()

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
            return USAJobResponse(raw_json, page_num, records)
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
