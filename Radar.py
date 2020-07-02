import sys

from scraping_scheduler.ibranch.configuration.Configurator import Configuration
from scraping_scheduler.ibranch.engine.Scraper import ScraperEngine


if __name__ == "__main__":
    args = sys.argv[1:]
    Configuration(args)

    ScraperEngine().start()

