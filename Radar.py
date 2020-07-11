import sys

from ibranch.scraping_scheduler.configuration.Configurator import Configuration
from ibranch.scraping_scheduler.engine.Scraper import ScraperEngine

from configuration_hub.StartupConfigurator import StartupConfigurator

if __name__ == "__main__":
    args = sys.argv[1:]
    Configuration(args)
    StartupConfigurator()

    ScraperEngine().start()

# import requests
#
# url = 'https://api.linkedin.com/v1/job-search'
# url = 'https://www.linkedin.com/oauth/v2/accessToken'
#
# api_key = '777b1llupsoymo'
# sharedsecret = 'FxDwRiiMEhUL9Y1o'
#
#
# data = {
#     'grant_type': 'client_credentials'
#     ,'client_id': api_key
#     ,'client_secret': sharedsecret
# }
#
# headers = {'Content-type': 'application/x-www-form-urlencoded'}
# r = requests.post(url, headers=headers, params=data)
# print(r.content)