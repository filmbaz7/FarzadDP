import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jdsports_spider import JDSportsSpider

items = []

class FilteredSpider(JDSportsSpider):
    name = "filtered_jdsports"

    def parse(self, response):
        for result in super().parse(response):
            if isinstance(result, dict) and result.get("discount", 0) >= 30:
                items.append(result)
                yield result
            else:
                yield result  # صفحات بعدی

def run_spider():
    global items
    items = []
    process = CrawlerProcess(get_project_settings())
    process.crawl(FilteredSpider)
    process.start(stop_after_crawl=True)  # ✅ این تغییر لازمه برای اجرای صحیح روی سرور
    return items
