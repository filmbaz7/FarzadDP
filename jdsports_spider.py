import scrapy

class JDSportsSpider(scrapy.Spider):
    name = "jdsports"
    allowed_domains = ["jdsports.it"]
    start_urls = ["https://www.jdsports.it/plp/new-balance"]

    def parse(self, response):
        self.logger.info(">>> Spider started...")

        # انتخاب همه کارت‌های محصول
        products = response.css("div[data-testid='product-item']")
        self.logger.info(f">>> Found {len(products)} products on this page")

        for product in products:
            name = product.css("a.text-default-primary::text").get()
            link = product.css("a.text-default-primary::attr(href)").get()
            price = product.css("h4.text-default-primary::text").get()
            image = product.css("img::attr(src)").get()

            if not (name and price and link):
                continue

            yield {
                "name": name.strip(),
                "price": price.strip(),
                "link": response.urljoin(link),
                "image": response.urljoin(image),
            }

        # صفحه بعد (اگه وجود داره)
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
