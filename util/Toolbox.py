import hashlib
import itertools
import json
import pathlib

import pandas as pd
from ibranch.scraping_scheduler.domain.System import CONSTANT as BaseConstant
from jproperties import Properties
from singleton_decorator import singleton


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


class ParameterGenerator:
    @staticmethod
    def create_combination_matrix(params: dict) -> pd.DataFrame:
        combination_list = pd.DataFrame({'dummy': [1]})
        for key, values in params.items():
            combination_list = pd.merge(combination_list, pd.DataFrame({key: values, 'dummy': [1] * len(values)}))
        combination_list.drop('dummy', axis=1, inplace=True)
        return combination_list

    @staticmethod
    def create_keyword_list(params: dict) -> list:
        return list(itertools.chain.from_iterable(params.values()))


@singleton
class Keyword:
    def __init__(self):
        root_dir = pathlib.Path(__file__).parent.parent.absolute()
        with open(f'{root_dir}/resource/property/keyword.properties', 'rb') as config_file:
            configs = Properties()
            configs.load(config_file)

            params = {k: v.data.lower().split(',') for k, v in configs.items()}
            self._keyword_list = ParameterGenerator.create_keyword_list(params)

            {k: v.append(' ') for k, v in params.items()}
            self._keyword_matrix = ParameterGenerator.create_combination_matrix(params)

    def get_keyword_list(self) -> list:
        return self._keyword_list

    def get_combination(self) -> pd.DataFrame:
        return self._keyword_matrix
