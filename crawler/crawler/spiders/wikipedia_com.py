import scrapy


class WikipediaCom(scrapy.Spider):
    name = "wikipedia_com"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Arch_Linux',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        yield response.css('#mw-content-text')
