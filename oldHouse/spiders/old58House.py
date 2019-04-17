# -*- coding: utf-8 -*-

import scrapy
from oldHouse.items import OldhouseItem


class Old58houseSpider(scrapy.Spider):
    name = 'old58House'
    start_url = 'https://bj.58.com/ershoufang/'
    base_url = 'https://bj.58.com'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_urls, meta={'dont_redirect': True})

    def parse_urls(self, response):
        urls = response.xpath('//h2[@class="title"]/a/@href').extract()
        for url in urls:
            if '?' in url:
                url = url.split('?')[0]
            if not url.startswith('https:'):
                url = 'https:' + url
            if 'zd_p' in url:
                yield scrapy.Request(url, callback=self.parse_detail)
            elif 'zd_p' not in url:
                yield scrapy.Request(url, callback=self.parse_detail, meta={'dont_redirect': True})

            yield scrapy.Request(url, callback=self.parse_detail)
        # new_url = response.xpath('//a[@class="next"]/@href').extract_first()
        # if new_url:
        #     next_page_url = self.base_url + new_url
        #     yield scrapy.Request(next_page_url, callback=self.parse_urls)

    def parse_detail(self, response):
        title = response.xpath('//div[4]/div[1]/h1/text()').extract_first()
        addr_lis = response.xpath('//ul[@class="house-basic-item3"]/li[2]//a/text()').extract()[:2]
        addr = ''.join([part.replace(' ', '').strip('\n') for part in addr_lis])
        type = response.xpath('//p[@class="room"]/span[@class="main"]/text()').extract_first().strip('\n').strip()
        area = response.xpath('//p[@class="area"]/span[1]/text()').extract_first().strip('\n').strip()
        decoration = response.xpath('//ul[@class="general-item-right"]/li[2]/span[@class="c_000"]/text()').extract_first()
        build_year = response.xpath('//ul[@class="general-item-right"]/li[4]/span[@class="c_000"]/text()').extract_first()
        sale_point = response.xpath('//*[@id="generalDesc"]/div/div[1]/p/text()').extract()
        item = OldhouseItem()
        for field in item.fields:
            try:
                item[field] = eval(field)
            except NameError:
                pass
        yield item



