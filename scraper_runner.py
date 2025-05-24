from scrapy.crawler import CrawlerProcess
from scrapy.utils import ossignal  # ← این خط اضافه شده
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

def run_spider():
    ossignal.install_shutdown_handlers = lambda *a, **kw: None  # ← این خط اضافه شده

    process = CrawlerProcess(settings={
        'LOG_ENABLED': False,
        'FEEDS': {
            'items.json': {'format': 'json'},
        }
    })

    class CustomSpider(JDSportsSpider):
        def parse(self, response):
            for item in super().parse(response):
                save_discount(item['title'], item['link'])
            yield from super().parse(response)

    process.crawl(CustomSpider)
    process.start(stop_after_crawl=True)
