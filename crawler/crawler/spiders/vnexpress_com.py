# -*- coding: utf-8 -*-
import scrapy
from ..items import CrawlerItem


class VnexpressComSpider(scrapy.Spider):
    name = 'vnexpress_com'
    allowed_domains = ['vnexpress.net']
    page_number = 2
    start_urls = ['http://vnexpress.net/thoi-su']

    def parse(self, response):

        all_div_news = response.css("section.sidebar_1 article.list_news")

        for div in all_div_news:
            title = div.css("h4.title_news a::text")[0].extract()
            href = div.xpath('child::h4/child::a[1]').xpath('@href')[0].extract()
            sub_content = div.css("p.description a::text")[0].extract()
            if href:
                request = scrapy.Request(url=href, callback=self.raw_content_parse)
                request.meta['title'] = title
                request.meta['sub_content'] = sub_content
                yield request

        next_page = "https://vnexpress.net/thoi-su/p" + str(VnexpressSpider.page_number)
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

