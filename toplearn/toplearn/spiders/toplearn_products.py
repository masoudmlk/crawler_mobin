import scrapy


class ToplearnProductsSpider(scrapy.Spider):
    name = 'toplearn_products'
    allowed_domains = ['www.toplearn.com']
    start_urls = ['https://toplearn.com/courses']
    page_number = 1
    product_list = []
    base_route = 'https://www.toplearn.com/courses'

    def parse(self, response):
        products = response.xpath("//div[@class='col-lg-9 col-md-8 col-sm-12 col-xs-12 courses-view']//div[@class='row']/div[@class='col-lg-4 course-col']/div[@class='box-shadow']")
        get_next_page = False
        for product in products:
            # // div[@class ='col-lg-4 course-col'] / div[@ class ='box-shadow'] / div[@ class ='off-section']
            url = response.urljoin(product.xpath(".//h2/a/@href").get())

            if url in self.product_list:
                continue

            self.product_list.append(url)
            get_next_page = True

            yield {
                'title': product.xpath(".//h2/a/text()").get(),
                'url': url,
                'img_url': response.urljoin(product.xpath(".//div[@class='img-layer']/img[@data-src]/@data-src").get()),
                'discount_rate': product.xpath(".//div[@class='off-section']/text()").get(),
                'author': product.xpath(".//div[@class='detail']/div[@class='top']/a[@title]/text()").get(),
                'author_link': response.urljoin(product.xpath(".//div[@class='detail']/div[@class='top']/a/@href").get()),
                'duration': product.xpath(".//div[@class='detail']/div[@class='bottom']/span[@class='time']/text()").get(),
                'price': response.xpath(".//div[@class='detail']/div[@class='bottom']/span[@class='price']/i/text()").get(),
            }
        self.page_number += 1
        if get_next_page:
            next_page = self.base_route + f"?pageId={self.page_number}"
            yield scrapy.Request(url=next_page, callback=self.parse)
            # yield scrapy.Request(url=next_page, callback=self.parse, headers={"User-Agent": "" })