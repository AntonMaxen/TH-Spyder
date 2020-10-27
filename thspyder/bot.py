from apscheduler.schedulers.blocking import BlockingScheduler
from thspyder.hookedspider import HookedSpider


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
