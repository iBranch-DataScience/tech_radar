from ibranch.scraping_scheduler.domain.Profile import Domain


class RecruitingRecord(Domain):
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
        super(RecruitingRecord, self).__init__()
        self._Source = None
        self._PositionID = None
        self._OrganizationName = None
        self._DepartmentName = None
        self._PositionTitle = None
        self._PositionRemuneration = None
        self._PositionLocation = None
        self._JobCategory = None
        self._PositionSchedule = None
        self._Description = None
        self._HowToApply = None
        self._ApplyURI = None
        self._PublicationStartDate = None
        self._ApplicationCloseDate = None
        self._Time = None

    @property
    def Source(self):
        return self._Source

    @Source.setter
    def Source(self, Source):
        self._Source = Source

    @property
    def PositionID(self):
        return self._PositionID

    @PositionID.setter
    def PositionID(self, PositionID):
        self._PositionID = PositionID

    @property
    def OrganizationName(self):
        return self._OrganizationName

    @OrganizationName.setter
    def OrganizationName(self, OrganizationName):
        self._OrganizationName = OrganizationName

    @property
    def DepartmentName(self):
        return self._DepartmentName

    @DepartmentName.setter
    def DepartmentName(self, DepartmentName):
        self._DepartmentName = DepartmentName

    @property
    def PositionTitle(self):
        return self._PositionTitle

    @PositionTitle.setter
    def PositionTitle(self, PositionTitle):
        self._PositionTitle = PositionTitle

    @property
    def PositionRemuneration(self):
        return self._PositionRemuneration

    @PositionRemuneration.setter
    def PositionRemuneration(self, PositionRemuneration):
        self._PositionRemuneration = PositionRemuneration

    @property
    def PositionLocation(self):
        return self._PositionLocation

    @PositionLocation.setter
    def PositionLocation(self, PositionLocation):
        self._PositionLocation = PositionLocation

    @property
    def JobCategory(self):
        return self._JobCategory

    @JobCategory.setter
    def JobCategory(self, JobCategory):
        self._JobCategory = JobCategory

    @property
    def PositionSchedule(self):
        return self._PositionSchedule

    @PositionSchedule.setter
    def PositionSchedule(self, PositionSchedule):
        self._PositionSchedule = PositionSchedule

    @property
    def Description(self):
        return self._Description

    @Description.setter
    def Description(self, Description):
        self._Description = Description

    @property
    def HowToApply(self):
        return self._HowToApply

    @HowToApply.setter
    def HowToApply(self, HowToApply):
        self._HowToApply = HowToApply

    @property
    def ApplyURI(self):
        return self._ApplyURI

    @ApplyURI.setter
    def ApplyURI(self, ApplyURI):
        self._ApplyURI = ApplyURI

    @property
    def PublicationStartDate(self):
        return self._PublicationStartDate

    @PublicationStartDate.setter
    def PublicationStartDate(self, PublicationStartDate):
        self._PublicationStartDate = PublicationStartDate

    @property
    def ApplicationCloseDate(self):
        return self._ApplicationCloseDate

    @ApplicationCloseDate.setter
    def ApplicationCloseDate(self, ApplicationCloseDate):
        self._ApplicationCloseDate = ApplicationCloseDate

    @property
    def Time(self):
        return self._Time

    @Time.setter
    def Time(self, Time):
        self._Time = Time
