# -*- coding: utf-8 -*-
import scrapy
from oldHouse.items import OldhouseItem


class Old58houseSpider(scrapy.Spider):
    name = 'old58House'
    start_url = 'https://bj.58.com/ershoufang/'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_urls)

    def parse_urls(self, response):
        urls = response.xpath('//h2[@class="title"]/a/@href').extract()
        for url in urls:
            if '?' in url:
                url = url.split('?')[0]
            if not url.startswith('https:'):
                url = 'https:' + url
            yield scrapy.Request(url, callback=self.parse_detail)

    def parse_detail(self, response):

        title = response.xpath('//div[4]/div[1]/h1/text()').extract_first()
        addr_lis = response.xpath('//ul[@class="house-basic-item3"]/li[2]//a/text()').extract()[:2]
        addr = '-'.join([part.strip('\n').strip() for part in addr_lis])
        type = response.xpath('//p[@class="room"]/span[@class="main"]/text()').extract_first().strip('\n').strip()
        area = response.xpath('//p[@class="area"]/span[1]/text()').extract_first().strip('\n').strip()
        decoration = response.xpath('//ul[@class="general-item-right"]/li[2]/span[@class="c_000"]/text()').extract_first()
        build_year = response.xpath('//ul[@class="general-item-right"]/li[4]/span[@class="c_000"]/text()').extract_first()
        price = response.xpath('//p/span[@class="price"]/text()').extract_first()
        sale_point = response.xpath('//*[@id="generalDesc"]/div/div[1]/p/text()').extract()
        item = OldhouseItem()
        for field in item.fields:
            try:
                item[field] = eval(field)
            except:
                pass
        yield item



