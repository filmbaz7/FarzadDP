from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jdsports_spider import JDSportsSpider
from db_helper import save_discounts
from twisted.internet import reactor
from crochet import setup, wait_for
setup()

@wait_for(timeout=60.0)
def run_spider():
    items_collected = []

    def handle_result(item, response, spider):
        items_collected.append(item)

    process = CrawlerProcess(settings={
        "LOG_ENABLED": False,
        "ITEM_PIPELINES": {},
    })

    crawler = process.create_crawler(JDSportsSpider)
    crawler.signals.connect(handle_result, signal=scrapy.signals.item_scraped)
    process.crawl(crawler)
    process.start()

    return items_collected

if __name__ == '__main__':
    print(">>> Spider started...")
    items = run_spider()
    print(f">>> Found {len(items)} items")
    save_discounts(items)
