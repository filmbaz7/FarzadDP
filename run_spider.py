import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
from jdsports_spider import JDSportsSpider
from db_helper import save_discounts

# راه‌اندازی Crochet برای استفاده از Twisted در اپلیکیشن معمولی
setup()

@wait_for(timeout=30.0)
def run_spider():
    from scrapy import signals

    items = []

    # زمانی که هر آیتم scrape شد این تابع فراخوانی میشه
    def handle_result(item):
        items.append(item)

    # اجرای spider
    runner = CrawlerRunner()
    crawler = runner.create_crawler(JDSportsSpider)
    crawler.signals.connect(handle_result, signal=scrapy.signals.item_scraped)

    d = runner.crawl(crawler)
    return items


if __name__ == '__main__':
    print(">>> Spider started...")
    try:
        items = run_spider()
        print(f">>> Found {len(items)} products on this page")
        for item in items:
            print(f">>> Item: {item}")
        save_discounts(items)
    except Exception as e:
        print(f">>> Spider error: {e}")
