# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class OldhouseItem(Item):
    # define the fields for your item here like:
    title = Field()
    addr = Field()
    area = Field()
    type = Field()
    decoration = Field()
    build_year = Field()
    sale_point = Field()


