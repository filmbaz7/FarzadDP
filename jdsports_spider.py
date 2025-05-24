import scrapy
import re

class JDSportsSpider(scrapy.Spider):
    name = "jdsports"
    allowed_domains = ["jdsports.it"]
    start_urls = ["https://www.jdsports.it/saldi/"]

    def parse(self, response):
        self.logger.info(">>> Spider started...")

        products = response.css("div.itemContainer")
        self.logger.info(f">>> Found {len(products)} products on this page")

        for product in products:
            name = product.css("span.itemTitle a::text").get()

            price_was_text = product.css("span.was span[data-oi-price]::text").get()
            price_now_text = product.css("span.now span[data-oi-price]::text").get()
            discount_text = product.css("span.sav::text").get()

            if not (price_was_text and price_now_text):
                continue

            try:
                price_was = float(price_was_text.replace("€", "").replace(",", ".").strip())
                price_now = float(price_now_text.replace("€", "").replace(",", ".").strip())
                difference = round(price_was - price_now, 2)
            except ValueError:
                continue

            # استخراج درصد تخفیف (مثلاً "Risparmia 21%")
            discount = None
            if discount_text:
                match = re.search(r"(\d+)%", discount_text)
                if match:
                    discount = int(match.group(1))

            link = response.urljoin(product.css("a.itemImage::attr(href)").get() or "")
            image = response.urljoin(product.css("img.thumbnail::attr(src)").get() or "")

            yield {
                "name": name,
                "priceWas": price_was,
                "priceNow": price_now,
                "difference": difference,
                "discount": discount,
                "link": link,
                "image": image,
            }

        # رفتن به صفحه بعدی اگر وجود داشت
        next_page = response.css("a.btn.btn-default.pageNav[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
