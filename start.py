#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings

from mySpider.spiders.wechat import WechatSpider

process = CrawlerProcess(settings)
process.crawl(WechatSpider)
process.start()