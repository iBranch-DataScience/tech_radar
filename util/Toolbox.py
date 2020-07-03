from ibranch.scraping_scheduler.domain.System import CONSTANT as BaseConstant


class CONSTANT(BaseConstant):

    @staticmethod
    def global_throttle():
        return "global_throttle"
