from apscheduler.schedulers.blocking import BlockingScheduler
from thspyder.hookedspider import HookedSpider
import json


class Bot:
    def __init__(self):
        self.spiders = []
        self.jobs = Jobs()

    def add_spider(self, model, url_hook, **kwargs):
        spider = HookedSpider(model, url_hook)
        self.spiders.append({
            "name": spider.spider_name,
            "spider": spider,
            "kwargs": kwargs
        })

    def add_spiders_from_config(self, config_path):
        with open(config_path) as json_file:
            spider_configs = json.load(json_file)

        for config in spider_configs:
            self.add_spider(config['model'], config['webhook_url'], **config['cron_time'])

    def load_spiders(self):
        for spider in self.spiders:
            self.jobs.add(spider['spider'].run, **spider["kwargs"])

    def start(self):
        self.jobs.start()


class Jobs(BlockingScheduler):
    def add(self, func, **kwargs):
        self.add_job(func, 'cron', **kwargs)

    def list_jobs(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
