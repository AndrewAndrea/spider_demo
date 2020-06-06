# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AreaItem(scrapy.Item):
    # define the fields for your item here like:
    district_id = scrapy.Field()
    parent_id = scrapy.Field()
    district_name = scrapy.Field()
    level = scrapy.Field()
    # pass
