# ✅ این خط باید قبل از هر ایمپورتی باشه که از twisted استفاده می‌کنه
import sys
if "twisted.internet.reactor" in sys.modules:
    raise RuntimeError("reactor already installed before asyncioreactor.install()")

# ری‌اکتور رو خیلی زود نصب کن
from twisted.internet import asyncioreactor
asyncioreactor.install()

# حالا بقیه ماژول‌ها رو ایمپورت کن
from scrapy.crawler import CrawlerRunner
from twisted.internet import defer, reactor
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

runner = CrawlerRunner(settings={
    'LOG_ENABLED': True,
    'FEEDS': {
        'items.json': {'format': 'json'},
    }
})

class CustomSpider(JDSportsSpider):
    def parse(self, response):
        for item in super().parse(response):
            save_discount(item['title'], item['link'])
            yield item

@defer.inlineCallbacks
def run_spider():
    yield runner.crawl(CustomSpider)
    reactor.stop()
