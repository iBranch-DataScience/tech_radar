import sys

from org.ibranch.configuration.Configurator import Configuration
from org.ibranch.engine.Scraper import ScraperEngine


def init_config(args):
    ad_hoc_cfg = dict()
    key, values = None, list()
    for item in args:

        if item.startswith('-'):
            ## Add value to previous key
            if None is not key:
                ad_hoc_cfg[key] = values.copy()

            ## Create new key
            values.clear()
            key = item.replace('-', '')
        else:
            values.append(item)
    ad_hoc_cfg[key] = values

    cfg = Configuration()
    for key, values in ad_hoc_cfg.items():
        value = values
        if len(value) == 0:
            value = ''
        elif len(value) == 1:
            value = value[0]
        cfg.replace_property(key, value)

    cfg.initialize()
    path = cfg.getPropertyWithDefault('cfg_path', None)

    if path:
        cfg.file_path(path)
        cfg.initialize()


if __name__ == "__main__":
    args = sys.argv[1:]
    init_config(args)

    ScraperEngine().start()
