import hashlib
import json
import pathlib

import pandas as pd
from ibranch.scraping_scheduler.domain.System import CONSTANT as BaseConstant
from ibranch.scraping_scheduler.util.Toolbox import LogicUtil
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


@singleton
class Keyword:
    def __init__(self):
        root_dir = pathlib.Path(__file__).parent.parent.absolute()
        with open(f'{root_dir}/resource/property/keyword.properties', 'rb') as config_file:
            configs = Properties()
            configs.load(config_file)

            params = {k: v.data.lower().split(',') for k, v in configs.items()}
            {k: v.append(' ') for k, v in params.items()}
            self._keyword_matrix = ParameterGenerator.create_combination_matrix(params)

    def get_combination(self) -> pd.DataFrame:
        """

        :rtype: object
        """
        return self._keyword_matrix

    def get_combination_str(self) -> list:
        return self._keyword_matrix.iloc[0:100,:].apply(self.concat_function, axis=1)

    def concat_function(self, row):
        if_else = lambda x: LogicUtil.if_else_default(x+'+', '')
        concat_keyword =if_else(row['db'])\
                + if_else(row['app'])\
                + if_else(row['algorithm'])\
                + if_else(row['protocol'])\
                + if_else(row['framework'])\
                + if_else(row['midware'])\
                + row['cicd']
        return concat_keyword


