import os
import sys
import django
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jdsports_spider import JDSportsSpider
from db_helper import add_discount

class CustomJDSportsSpider(JDSportsSpider):
    def parse(self, response):
        print(">>> Spider parsing...")
        for product in response.css("span.itemContainer"):
            name = product.css("span.itemTitle a::text").get()
            priceWasText = product.css("span.was span::text").get()
            priceIsText = product.css("span.now span::text").get()

            if not priceWasText or not priceIsText:
                continue

            try:
                priceWas = float(priceWasText.replace("€", "").replace(",", ".").strip())
                priceIs = float(priceIsText.replace("€", "").replace(",", ".").strip())
            except ValueError:
                continue

            discount = round((priceWas - priceIs) * 100 / priceWas, 0)
            difference = priceWas - priceIs
            link = response.urljoin(product.css("a.itemImage").attrib.get("href", ""))
            image = response.urljoin(product.css("img.thumbnail").attrib.get("src", ""))

            item = {
                "name": name,
                "priceWas": priceWas,
                "priceIs": priceIs,
                "difference": difference,
                "discount": discount,
                "link": link,
                "image": image,
            }

            print(f">>> Item: {item}")
            add_discount(name, link, priceWas, priceIs, discount, image)
            yield item

        next_page = response.css("a.btn.btn-default.pageNav[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)


def run_spider():
    print(">>> Spider started...")
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
    })
    process.crawl(CustomJDSportsSpider)
    process.start()
    print(">>> Spider finished.")


if __name__ == "__main__":
    run_spider()
