import scrapy

class JDSportsSpider(scrapy.Spider):
    name = "jdsports"
    start_urls = ["https://www.jdsports.it/saldi/"]

    def parse(self, response):
        for product in response.css("div.itemContainer"):
            name = product.css("span.itemTitle a::text").get()

            price_was_text = product.css("span.was > span[data-oi-price]::text").get()
            price_now_text = product.css("span.now > span[data-oi-price]::text").get()
            discount_text = product.css("span.sav::text").get()

            if not price_was_text or not price_now_text:
                continue

            # تبدیل قیمت از فرمت ایتالیایی (کاما به نقطه)
            try:
                price_was = float(price_was_text.replace("€", "").replace(",", ".").strip())
                price_now = float(price_now_text.replace("€", "").replace(",", ".").strip())
            except ValueError:
                continue

            # استخراج عدد تخفیف از رشته مثل "(Risparmia 21%)"
            discount = None
            if discount_text:
                import re
                match = re.search(r"(\d+)%", discount_text)
                if match:
                    discount = int(match.group(1))

            link = response.urljoin(product.css("a.itemImage::attr(href)").get() or "")
            image = response.urljoin(product.css("img.thumbnail::attr(src)").get() or "")

            yield {
                "name": name,
                "priceWas": price_was,
                "priceNow": price_now,
                "discount": discount,
                "link": link,
                "image": image,
            }

        # صفحه بعد
        next_page = response.css("a.btn.btn-default.pageNav[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
