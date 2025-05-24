import scrapy

class JDSportsSpider(scrapy.Spider):
    name = "jdsports"
    start_urls = ["https://www.jdsports.it/saldi/"]

    def parse(self, response):
        products = response.css("div.productListItem")
        for product in products:
            name = product.css("div.itemTitle a::text").get()
            price_was_text = product.css("div.was span::text").get()
            price_is_text = product.css("div.now span::text").get()

            if not price_was_text or not price_is_text:
                continue

            try:
                price_was = float(price_was_text.replace("€", "").replace(",", ".").strip())
                price_is = float(price_is_text.replace("€", "").replace(",", ".").strip())
            except ValueError:
                continue

            discount = round((price_was - price_is) * 100 / price_was, 0)
            difference = price_was - price_is
            link = response.urljoin(product.css("a.itemImage::attr(href)").get())
            image = response.urljoin(product.css("img.thumbnail::attr(src)").get())

            yield {
                "name": name,
                "priceWas": price_was,
                "priceIs": price_is,
                "difference": difference,
                "discount": discount,
                "link": link,
                "image": image,
            }

        next_page = response.css("a.btn.btn-default.pageNav[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
