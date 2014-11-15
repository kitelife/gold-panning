#coding: utf-8

from datetime import datetime

import scrapy
from scrapy.selector import Selector

from ..items import P2pEyeItem


class P2pEyeSpider(scrapy.Spider):
    name = 'p2peye'
    allowed_domains = ['www.p2peye.com']
    start_urls = ['http://www.p2peye.com/forum-42-1.html']
    
    def parse(self, response):
        today = datetime.now().strftime('%Y-%m-%d')
        items = []
        target_tbodys = Selector(response=response).xpath('//tbody[contains(@id, "normalthread")]')

        for tbody in target_tbodys:
            new_item = P2pEyeItem()

            new_item['link'] = tbody.xpath('tr/th/a[3]/@href').extract()
            new_item['title'] = tbody.xpath('tr/th/a[3]/text()').extract()
            new_item['provider'] = u'网贷天眼'
            new_item['date'] = tbody.xpath('tr/td[2]/em/span/span/@title').extract()
            new_item['scrape_date'] = today

            items.append(new_item)

        print items