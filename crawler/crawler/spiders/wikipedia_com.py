import scrapy
import re

from crawler.settings import MAXIMUM_PAGE


class WikipediaCom(scrapy.Spider):
    name = "wikipedia_com"
    page_crawled = 0

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Arch_Linux',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'url': response.url,
            'title': response.css('#mw-content-text div').get(),
            'content': response.css('#mw-content-text div').get(),
        }
        for a in response.css("#mw-content-text a"):
            href = a.css('::attr(href)').get()
            if WikipediaCom.page_crawled < MAXIMUM_PAGE and isinstance(href, str) and re.match(r"^/wiki/[^:]*$", href):
                WikipediaCom.page_crawled += 1
                yield response.follow(href, callback=self.parse)
        # self.log(response.css('#mw-content-text').get())
