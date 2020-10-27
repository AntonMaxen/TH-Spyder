from thspyder.spider import Spider
from thspyder.webhook import Webhook
from thspyder.models.model_pp import modelpp

import os
import datetime
from dotenv import load_dotenv
load_dotenv()
WHOOK = os.getenv("WHOOK")


class HookedSpider(Spider):
    def __init__(self, model, web_hook_url):
        super().__init__(model)
        self.web_hook = Webhook(web_hook_url)

    def run(self):
        print(f'Spider: "{self.spider_name}" started a round of scraping, time: {datetime.datetime.now()}')
        diff_list = self.scrape_and_get_difference()
        for folder_name in diff_list.keys():
            for filename, changes in diff_list[folder_name].items():
                if len(changes) > 0:
                    self.web_hook.send(changes, filename, ignore_empty=True, formatting="*", items_per_request=5)

        print(f'Spider: "{self.spider_name}" ended a round of scraping, time: {datetime.datetime.now()}')


def main():
    spooder = HookedSpider(modelpp, WHOOK)
    spooder.run()


if __name__ == '__main__':
    main()
