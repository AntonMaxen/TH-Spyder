from apscheduler.schedulers.blocking import BlockingScheduler
import json
# local imports
from thspyder.hookedspider import HookedSpider


class Bot:
    """Class for creating, managining and queueing spider objects with help of
    a BlockingScheduler object that have integrated cron-scheduler, this
    is the center of the program."""
    def __init__(self):
        self.spiders = []
        self.jobs = BlockingScheduler()

    def add_spider(self, model, webhook, cron_time):
        spider = HookedSpider(model, webhook)
        self.spiders.append({
            "name": spider.spider_name,
            "spider": spider,
            "cron_time": cron_time
        })

    def add_spiders_from_config(self, config_path):
        """Loads model, webhook_url and cron_time from a json-structure"""
        with open(config_path) as json_file:
            spider_configs = json.load(json_file)

        for config in spider_configs:
            self.add_spider(config["model"], config["webhook"], config["cron_time"])

    def load_spiders(self):
        """queueing spiders for scheduled scraping"""
        for spider in self.spiders:
            self.jobs.add_job(spider["spider"].run, "cron", **spider["cron_time"])

    def start(self):
        for spider_dict in self.spiders:
            print(f'Starting {spider_dict["name"]}, scheduled with: {spider_dict["cron_time"]}')

        self.jobs.start()
