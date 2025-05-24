from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from twisted.internet.asyncioreactor import install
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

# تنظیم لاگ برای نمایش در ترمینال
configure_logging()

try:
    install()
except Exception as e:
    print("Reactor already installed or error installing:", e)

runner = CrawlerRunner(settings={
    'LOG_ENABLED': True,
    'FEEDS': {
        'items.json': {'format': 'json'},
    },
})

class CustomSpider(JDSportsSpider):
    def parse(self, response):
        print(">>> CustomSpider.parse started")
        for item in super().parse(response):
            print(f">>> Found item: {item['title']} | {item['link']}")
            save_discount(item['title'], item['link'])
            yield item

@defer.inlineCallbacks
def run_spider():
    print(">>> Spider started...")
    yield runner.crawl(CustomSpider)
    print(">>> Spider finished")
    reactor.stop()

# اگر مستقیم اجرا بشه
if __name__ == '__main__':
    run_spider()
    reactor.run()
