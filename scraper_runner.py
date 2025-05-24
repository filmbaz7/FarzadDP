import asyncio
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import asyncioreactor
from jdsports_spider import JDSportsSpider
from db_helper import save_discount

# حتما باید اول ری‌اکتور asyncio ست بشه
asyncioreactor.install()

def run_spider():
    async def crawl():
        runner = CrawlerRunner(settings={
            'LOG_ENABLED': False,
            'FEEDS': {
                'items.json': {'format': 'json'},
            }
        })

        class CustomSpider(JDSportsSpider):
            def parse(self, response):
                for item in super().parse(response):
                    save_discount(item['title'], item['link'])
                    yield item

        await runner.crawl(CustomSpider)

    asyncio.run(crawl())
