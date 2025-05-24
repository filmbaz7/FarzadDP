from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from jdsports_spider import JDSportsSpider

items = []

class CustomSpider(JDSportsSpider):
    def parse(self, response):
        for item in super().parse(response):
            if item["discount"] >= 30:
                items.append(item)
                yield item

@defer.inlineCallbacks
def crawl():
    configure_logging()
    runner = CrawlerRunner()
    yield runner.crawl(CustomSpider)
    reactor.stop()

def run_spider():
    global items
    items = []
    crawl()
    reactor.run()
    return items
