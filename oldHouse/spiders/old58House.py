# -*- coding: utf-8 -*-

import json
import scrapy
from scrapy.utils.project import get_project_settings
from six.moves.urllib.parse import urljoin
from oldHouse.items import OldhouseItem


class Old58houseSpider(scrapy.Spider):
    name = 'old58House'
    start_url = 'https://bj.58.com/ershoufang/'
    base_url = 'https://bj.58.com'
    # redis_key = 'old_house'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = get_project_settings()
        self._proxy_lis = self.proxies

    @property
    def proxies(self):
        proxy_file = open(self.settings.get('PROXY_JSON_FILE'), 'r', encoding='utf-8')
        return json.load(proxy_file)

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse_urls)

    def parse_urls(self, response):
        url_items = response.xpath('//ul[contains(@class, "house-list")]/li').extract()
        for item in url_items:
            sele_item = scrapy.Selector(text=item)
            url = sele_item.xpath('//h2[@class="title"]/a/@href').extract_first()
            node = sele_item.xpath('//p[@class="sum"]').extract_first()
            sele_node = scrapy.Selector(text=node)
            price = sele_node.xpath('string(.)').extract_first()    # get price, pack to item

            if '?' in url:
                url = url.split('?')[0]
            if not url.startswith('https:'):
                url = 'https:' + url
            item = OldhouseItem()
            item['price'] = price
            request = scrapy.Request(url, callback=self.parse_detail, meta={'item': item})
            yield request

        new_url = response.xpath('//a[@class="next"]/@href').extract_first()
        if new_url:    # crawl more page
            next_page_url = urljoin(self.base_url, new_url)
            yield scrapy.Request(next_page_url, callback=self.parse_urls)

    def parse_detail(self, response):
        title = response.xpath('//div[4]/div[1]/h1/text()').extract_first()
        addr_lis = response.xpath('//ul[@class="house-basic-item3"]/li[2]//a/text()').extract()[:2]
        addr = ''.join([part.replace(' ', '').strip('\n') for part in addr_lis])
        type = response.xpath('//p[@class="room"]/span[@class="main"]/text()').extract_first(default='').strip('\n').strip()
        area = response.xpath('//p[@class="area"]/span[1]/text()').extract_first().strip('\n').strip()
        decoration = response.xpath('//ul[@class="general-item-right"]/li[2]/span[@class="c_000"]/text()').extract_first()
        build_year = response.xpath('//ul[@class="general-item-right"]/li[4]/span[@class="c_000"]/text()').extract_first()
        sale_point = response.xpath('//*[@id="generalDesc"]/div/div[1]/p/text()').extract()
        item = response.meta['item']
        for field in item.fields:
            try:
                item[field] = eval(field)
            except NameError:
                pass
        yield item



