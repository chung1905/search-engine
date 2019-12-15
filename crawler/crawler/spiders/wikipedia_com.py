import pymongo
import scrapy
import re

from crawler.items import CrawlerItem
from crawler.pipelines import CrawlerPipeline


class WikipediaCom(scrapy.Spider):
    name = "wikipedia_com"
    page_crawled = 0
    conn = None
    collection = None

    url_regex = re.compile(r"^/wiki/[^:]*$")

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/Arch_Linux',
        ]
        self.conn = pymongo.MongoClient(self.settings.get('MONGO_URI'), self.settings.get('MONGO_PORT', 27017))
        db = self.conn[self.settings.get('MONGO_DATABASE', 'items')]
        self.collection = db[CrawlerPipeline.collection_name]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def closed(self, reason):
        self.conn.close()

    def parse(self, response):
        yield self.parse_item(response)

        for a in response.css("#mw-content-text a"):
            href = a.css('::attr(href)').get()
            if WikipediaCom.page_crawled <= self.settings.get('MAXIMUM_PAGE') \
                    and isinstance(href, str) \
                    and re.match(self.url_regex, href)\
                    and self.collection.find_one({"url": response.urljoin(href)}) is None:
                WikipediaCom.page_crawled += 1
                yield response.follow(href, callback=self.parse)

    content_regex = re.compile(r"(<[^<>]+>|</\w+>|NaN)", re.MULTILINE)
    def parse_item(self, response):
        item = CrawlerItem()
        item['url'] = response.url
        item['title'] = response.css('#firstHeading::text').get()
        item['overview'] = re.sub(
            self.content_regex,
            '',
            response.css('#mw-content-text div p:not(.mw-empty-elt)').get()
        )
        item['content'] = re.sub(
            self.content_regex,
            '',
            response.css('#mw-content-text div').get()
        )
        return item
