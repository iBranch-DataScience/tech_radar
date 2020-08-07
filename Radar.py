import sys

from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.engine.Scraper import ScraperEngine

if __name__ == "__main__":
    args = sys.argv[1:]
    Configuration(args)

    ScraperEngine().start()
