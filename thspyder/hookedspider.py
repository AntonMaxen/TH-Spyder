import datetime
# local imports
from thspyder.spider import Spider
from thspyder.webhook import Webhook


class HookedSpider(Spider):
    """Supercharged Spider with webhookintegration, posts what it finds to a url"""
    def __init__(self, model, webhook):
        super().__init__(model)
        self.web_hook = Webhook(webhook['url'], **webhook['settings'])

    def run(self):
        print(f'Spider: "{self.spider_name}" started a round of scraping, time: {datetime.datetime.now()}')

        diff_list = self.scrape_and_get_difference()
        for folder_name in diff_list.keys():
            for filename, changes in diff_list[folder_name].items():
                if len(changes) > 0:
                    self.web_hook.send(changes, filename)

        print(f'Spider: "{self.spider_name}" ended a round of scraping, time: {datetime.datetime.now()}')
