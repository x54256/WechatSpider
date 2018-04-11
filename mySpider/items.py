# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):

    title = scrapy.Field()   # 标题
    content = scrapy.Field()    # 内容
    source = scrapy.Field()    # 来源
    datetime = scrapy.Field() # 发布日期

