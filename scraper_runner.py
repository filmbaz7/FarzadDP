from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from jdsports.jdsports_spider import JDSportsSpider  # فرض بر این است که داخل فولدر jdsports هست

items = []

class CustomSpider(JDSportsSpider):
    def parse(self, response):
        for item in super().parse(response):
            if item["discount"] >= 30:
                items.append(item)
                yield item  # مهم برای ذخیره آیتم‌ها توسط Scrapy

def run_spider():
    global items
    items = []  # ریست قبل از اجرای هر بار
    process = CrawlerProcess(get_project_settings())
    process.crawl(CustomSpider)
    process.start()
    return items
