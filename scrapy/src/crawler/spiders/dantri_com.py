import scrapy
from ..items import CrawlerItem


class VnexpressSpider(scrapy.Spider):
    name = "dantri"
    page_number = 1
    start_urls = ["https://dantri.com.vn/xa-hoi.html"]

    def parse(self, response):

        all_div = response.css("mt2 newszone")

        for div in all_div:
            title = div.css("div.mt3.clearfix div.mr1 h2 a:text")[0].extract()
            href = div.xpath('child::h4/child::a[1]').xpath('@href')[0].extract()
            sub_content = div.css("p.description a::text")[0].extract()
            if href:
                request = scrapy.Request(url=href, callback=self.raw_content_parse)
                request.meta['title'] = title
                request.meta['sub_content'] = sub_content
                yield request

        next_page = "https://vnexpress.net/the-thao/p" + str(VnexpressSpider.page_number)
        if VnexpressSpider.page_number <= 1600:
            VnexpressSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)

    def raw_content_parse(self, response):
        title = response.meta.get('title')
        sub_content = response.meta.get('sub_content')
        href = response.url
        str = ''
        for raw_content in response.css("article.content_detail p.Normal::text").extract():
            str += raw_content
        items = CrawlerItem()
        items['title'] = title
        items['href'] = href
        items['sub_content'] = sub_content
        items['raw_content'] = str
        yield items
