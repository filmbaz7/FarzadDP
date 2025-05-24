from scrapy.crawler import CrawlerRunner
from twisted.internet import asyncioreactor, defer, reactor
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

# حتما اول ری‌اکتور asyncio نصب بشه
asyncioreactor.install()

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
