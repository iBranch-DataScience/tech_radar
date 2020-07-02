import logging
from queue import Queue

import requests
import pandas as pd

from api.Client import Request, Response, ScrapingStrategy, Client
from scraping_scheduler.ibranch.engine.client import RequestsClient
from scraping_scheduler.ibranch.domain.System import CONSTANT, Cache
from scraping_scheduler.ibranch.engine.job.Base import BaseJob


class APIRequest(Request):
    def __init__(self, APIName='USAJobs'):
        self._logger = logging.getLogger(type(self).__name__)
        super(APIRequest, self).__init__()
        Request.register(APIRequest)
        self._keyword = ''
        self._location = ''
        self._url = ''
        self._paras = ''
        self._header = None
        self._APIName = APIName
        self._PageNum = 1

    def set_PageNum(self, PageNum):
        self._PageNum = PageNum

    def set_APIName(self, APIName):
        self._APIName = APIName

    def APIName(self):
        return self._APIName

    def set_parameters(self):
        if self._APIName == 'USAJobs':
            self._USAJobs()
        elif self._APIName == 'GithubJobs':
            self._GithubJobs()
        else:
            raise ValueError("API名称不正确...")

    def _USAJobs(self):
        self._set_url('https://data.usajobs.gov/api/search')
        host = 'data.usajobs.gov'
        user_agent = 'rj_jnu@outlook.com'
        auth_key = '2Gkkyrddz2Skk1czvO03iqRzUmPBqB6WCaTXUV1O/pc='

        header = {
            "Host": host,
            "User-Agent": user_agent,
            "Authorization-Key": auth_key
        }

        self._set_header(header=header)
        self._set_USAJobs_parameters()

    def _GithubJobs(self):
        self._set_url("https://jobs.github.com/positions.json")
        self._set_GithubJobs_parameters()

    def get(self):
        r = requests.get(self._url + self._paras, headers=self._header)
        if r.status_code == 200:
            self._logger.info("API访问成功...")
        return r.json()

    def _set_url(self, url):
        self._url = url

    def _set_header(self, header):
        self._header = header

    def _set_GithubJobs_parameters(self, full_time="", lat="", long=""):
        """
        :type String
        """
        paras = ("?description=" + self._keyword
                 + "&location=" + self._location
                 + "&full_time=" + full_time
                 + "&lat=" + lat
                 + "&long=" + long
                 )

        self._paras = paras

    def _set_USAJobs_parameters(self, JobCategoryCode=""):
        """
        :type String
        """
        paras = ("?JobCategoryCode=" + JobCategoryCode
                 + "&Keyword" + self.keyword
                 + "&LocationName" + self._location
                 + "&ResultsPerPage=500"
                 + "&Page=" + str(self._PageNum)
                 )

        self._paras = paras

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        self._keyword = keyword

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, location):
        self._location = location


class APIResponse(Response):
    def __init__(self, APIName='USAJobs'):
        self._logger = logging.getLogger(type(self).__name__)
        super(APIResponse, self).__init__()
        Response.register(APIResponse)
        self._language = None
        self._level = None
        self.df = None
        self._APIName = APIName
        self.PageNum = 0

    def set_APIname(self, APIName):
        self._APIName = APIName

    def APIName(self):
        return self._APIName

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

    def transform_to_df(self, json):
        if self._APIName == 'USAJobs':
            self._get_USAJobs_df(json)
        elif self._APIName == 'GithubJobs':
            self._get_GithubJobs_df(json)
        else:
            raise ValueError("API名称不正确...")

    def get_df(self):
        return self.df

    def _get_GithubJobs_df(self, json):
        self._logger.info('json文件转换Data Frame中...')
        self.df = pd.DataFrame(json, index=range(len(json)))
        self._logger.info('Data Frame转换成功...')

    def _get_USAJobs_df(self, json):
        self._logger.info('json文件转换Data Frame中...')
        # transform jason data to data frame
        l = json['SearchResult']['SearchResultItems']
        # list
        names = {'PositionTitle', 'PositionURI', 'ApplyURI', 'PositionLocation', 'OrganizationName'
            , 'DepartmentName', 'JobCategory', 'PositionSchedule', 'PositionOfferingType', 'QualificationSummary'
            , 'PublicationStartDate', 'ApplicationCloseDate'}
        p = [{key: value for key, value in element['MatchedObjectDescriptor'].items() if key in names} for element in l]

        # Note: The number of results returned per request defaults to 25
        # but can be defined in your request up to 500 per request.
        self.PageNum = int(json['SearchResult']['UserArea']['NumberOfPages'])
        self.df = pd.DataFrame(p)
        self._logger.info('Data Frame转换成功...')


class APIScrapingStrategy(ScrapingStrategy):
    def __init__(self):
        super(APIScrapingStrategy, self).__init__()
        ScrapingStrategy.register(APIScrapingStrategy)
        self._language = None
        self._level = None

    def get_data(self, request: APIRequest) -> Response:
        """
        :APIName type String ("USAJob" or "GithubJobs)
        :return pandas DataFrame
        """
        response = APIResponse(request.APIName())
        response.transform_to_df(request.get())
        response.language = 'Python3'
        response.level = 5
        return response
