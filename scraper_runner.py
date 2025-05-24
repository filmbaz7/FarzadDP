import asyncio
from scrapy.crawler import CrawlerRunner
from twisted.internet import asyncioreactor, defer
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

# حتما اول ری‌اکتور asyncio نصب بشه، قبل از هرچیز
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
def crawl():
    yield runner.crawl(CustomSpider)
    # اگر کرولرهای دیگه‌ای بود اینجا می‌تونی اضافه کنی
    reactor.stop()  # وقتی تموم شد، ری‌اکتور رو متوقف کن

if __name__ == '__main__':
    from twisted.internet import reactor
    crawl()
    reactor.run()
