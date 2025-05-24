import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jdsports_spider import JDSportsSpider

items = []

class FilteredSpider(JDSportsSpider):
    name = "filtered_jdsports"

    def parse(self, response):
        # اگر parse اصلی generator برمی‌گردونه، باید ازش استفاده کنیم
        for result in super().parse(response):
            if isinstance(result, dict):
                if result.get("discount", 0) >= 30:
                    items.append(result)
                    yield result
                # اگر لازم نیست چیز دیگه‌ای yield کنیم، می‌تونیم ردش کنیم

def run_spider():
    global items
    items = []
    process = CrawlerProcess(get_project_settings())
    process.crawl(FilteredSpider)
    process.start(stop_after_crawl=True)  # برای اجرای درست در سرور
    return items
