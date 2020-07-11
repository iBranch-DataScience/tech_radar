import hashlib
import json

from ibranch.scraping_scheduler.domain.System import CONSTANT as BaseConstant


class CONSTANT(BaseConstant):
    @staticmethod
    def global_throttle():
        return "global_throttle"

    @staticmethod
    def usa_job():
        return "usa_job"

    @staticmethod
    def github_job():
        return "github_job"


class MD5Encoder:
    @staticmethod
    def encode_json(json_obj, charset='utf-8'):
        json_str = json.dumps(json_obj, sort_keys=True, indent=0)
        return hashlib.md5(json_str.encode(charset)).hexdigest()
