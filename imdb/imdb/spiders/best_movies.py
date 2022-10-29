import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.utils.response import open_in_browser


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']
    first = False
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='titleColumn']/a"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        # if not self.first:
        #     open_in_browser(response)
        #     self.first = True

        yield {
            "title": response.xpath("//h1[@data-testid='hero-title-block__title']/text()").get(),
            # "year": response.xpath("//div[@data-testid='hero-title-block__original-title']/following-sibling::ul/li[position()=1]/a/text()").get(),
              "year": response.xpath("//ul[@data-testid='hero-title-block__metadata']/li[position()=1]/a/text()").get(),
            "genre": response.xpath("//div[@data-testid='genres']/div[@class='ipc-chip-list__scroller']/a/span/text()").getall(),
            "duration": response.xpath("//ul[@data-testid='hero-title-block__metadata']/li[position()=3]/text()").getall(),

            "rating": response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[position()=1]/text()").get(),
            "count_rate": response.xpath("//div[@data-testid='hero-rating-bar__aggregate-rating__score']/parent::node()/div[position()=last()]/text()").get(),
            "movie_url": response.url,

        }
        # title = response.xpath("//h1[@data-testid='hero-title-block__title/text()']").get()

        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
