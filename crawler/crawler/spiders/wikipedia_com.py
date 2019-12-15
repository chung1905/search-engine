import scrapy
import re

from crawler.items import CrawlerItem
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
        item = CrawlerItem()
        item['url'] = response.url
        item['title'] = response.css('#firstHeading::text').get()
        item['content'] = response.css('#mw-content-text div').get()
        yield item

        for a in response.css("#mw-content-text a"):
            href = a.css('::attr(href)').get()
            if WikipediaCom.page_crawled < MAXIMUM_PAGE and isinstance(href, str) and re.match(r"^/wiki/[^:]*$", href):
                WikipediaCom.page_crawled += 1
                yield response.follow(href, callback=self.parse)
