from ibranch.scraping_scheduler.domain.Profile import Domain


class RecruitingRecord(Domain):
    features = [
        'source'
        , 'position_id'
        , 'organization_name'
        , 'department_name'
        , 'position_title'
        , 'position_remuneration'
        , 'position_location'
        , 'job_category'
        , 'position_schedule'
        , 'description'
        , 'how_to_apply'
        , 'apply_uri'
        , 'publication_start_date'
        , 'application_close_date'
        , 'time'
    ]

    def __init__(self):
        super(RecruitingRecord, self).__init__()
        self._source = None
        self._raw_doc_id = None
        self._position_id = None
        self._organization_name = None
        self._department_name = None
        self._position_title = None
        self._position_remuneration = None
        self._position_location = None
        self._job_category = None
        self._position_schedule = None
        self._description = None
        self._how_to_apply = None
        self._apply_uri = None
        self._publication_start_date = None
        self._application_close_date = None
        self._time = None

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @property
    def raw_doc_id(self):
        return self._raw_doc_id

    @raw_doc_id.setter
    def raw_doc_id(self, raw_doc_id):
        self._raw_doc_id = raw_doc_id

    @property
    def position_id(self):
        return self._position_id

    @position_id.setter
    def position_id(self, position_id):
        self._position_id = position_id

    @property
    def organization_name(self):
        return self._organization_name

    @organization_name.setter
    def organization_name(self, organization_name):
        self._organization_name = organization_name

    @property
    def department_name(self):
        return self._department_name

    @department_name.setter
    def department_name(self, department_name):
        self._department_name = department_name

    @property
    def position_title(self):
        return self._position_title

    @position_title.setter
    def position_title(self, position_title):
        self._position_title = position_title

    @property
    def position_remuneration(self):
        return self._position_remuneration

    @position_remuneration.setter
    def position_remuneration(self, position_remuneration):
        self._position_remuneration = position_remuneration

    @property
    def position_location(self):
        return self._position_location

    @position_location.setter
    def position_location(self, position_location):
        self._position_location = position_location

    @property
    def job_category(self):
        return self._job_category

    @job_category.setter
    def job_category(self, JobCategory):
        self._job_category = JobCategory

    @property
    def position_schedule(self):
        return self._position_schedule

    @position_schedule.setter
    def position_schedule(self, position_schedule):
        self._position_schedule = position_schedule

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def how_to_apply(self):
        return self._how_to_apply

    @how_to_apply.setter
    def how_to_apply(self, how_to_apply):
        self._how_to_apply = how_to_apply

    @property
    def apply_uri(self):
        return self._apply_uri

    @apply_uri.setter
    def apply_uri(self, ApplyURI):
        self._apply_uri = ApplyURI

    @property
    def publication_start_date(self):
        return self._publication_start_date

    @publication_start_date.setter
    def publication_start_date(self, publication_start_date):
        self._publication_start_date = publication_start_date

    @property
    def application_close_date(self):
        return self._application_close_date

    @application_close_date.setter
    def application_close_date(self, application_close_date):
        self._application_close_date = application_close_date

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time


class ScrapingLog(Domain):
    def __init__(self):
        super(ScrapingLog, self).__init__()
        self._raw_data_id = None
        self._url = None
        self._keyword = None
        self._ts = None
        self._http_code = None
        self._comment = None

    @property
    def raw_data_id(self):
        return self._raw_data_id

    @raw_data_id.setter
    def raw_data_id(self, raw_data_id):
        self._raw_data_id = raw_data_id

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, keyword):
        self._keyword = keyword

    @property
    def ts(self):
        return self._ts

    @ts.setter
    def ts(self, ts):
        self._ts = ts

    @property
    def http_code(self):
        return self._http_code

    @http_code.setter
    def http_code(self, http_code):
        self._http_code = http_code

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment
