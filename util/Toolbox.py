from ibranch.scraping_scheduler.domain.System import CONSTANT as BaseConstant


class CONSTANT(BaseConstant):

    @staticmethod
    def usajob():
        return "usajob"

    @staticmethod
    def githubjob():
        return "githubjob"
