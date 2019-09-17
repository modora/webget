# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ExampleSpider(CrawlSpider):
    name = "example"
    start_urls = [
        'http://example.webscraping.com/',
        # 'https://example.com'
    ]

    rules = (Rule(LinkExtractor(), callback="parse_item", follow=True),)

    def parse_item(self, response):
        items = {}
        items['response'] = response.copy()
        # item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        # item['name'] = response.xpath('//div[@id="name"]').get()
        # item['description'] = response.xpath('//div[@id="description"]').get()
        return items
