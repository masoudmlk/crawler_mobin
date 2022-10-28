import scrapy
import logging

class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']
    # country_name = ''
    def parse(self, response):
        title = response.xpath("//h1/text()").get()
        countries = response.xpath("//td/a")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            # self.country_name = name
            # yield {
            #     "country_name": name,
            #     "country_link": link,
            # }
            # yield {
            #     "country_name": name,
            #     "country_link": self.allowed_domains[0]+link,
            # }
            # # when we use relative url and we want to change to full url
            # # manaually
            # absolute_url = f"https://{self.allowed_domains[0]}{link}"
            # # via join funciton
            # absolute_url = response.urljoin(link)
            # print(absolute_url)
            # yield scrapy.Request(url=absolute_url)

            # # via yield command
            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        # logging.info(response.url)
        country_name = response.request.meta.get("country_name")
        rows = response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population = row.xpath(".//td[2]/strong/text()").get()
            yield {
                # 'country_name':self.country_name,
                'country_name': country_name,
                'year': year,
                'population': population
            }

