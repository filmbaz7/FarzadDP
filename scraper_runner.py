from scrapy.crawler import CrawlerProcess
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

def run_spider():
    process = CrawlerProcess(settings={
        'LOG_ENABLED': False,
        'FEEDS': {
            'items.json': {'format': 'json'},
        }
    })

    class CustomSpider(JDSportsSpider):
        def parse(self, response):
            # فرض کن اسپایدر تخفیف‌ها رو می‌گیره و اینجا ذخیره می‌کنیم
            for item in super().parse(response):
                save_discount(item['title'], item['link'])
            yield from super().parse(response)

    process.crawl(CustomSpider)
    process.start(stop_after_crawl=True)
