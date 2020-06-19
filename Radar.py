import sys

from org.ibranch.configuration.Configurator import Configuration
from org.ibranch.engine.Scraper import ScraperEngine


if __name__ == "__main__":
    args = sys.argv[1:]
    Configuration(args)

    ScraperEngine().start()
