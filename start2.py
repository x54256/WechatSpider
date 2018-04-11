#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# from scrapy import cmdline
# cmdline.execute("scrapy crawl wechat".split())

from scrapy.crawler import CrawlerProcess
from scrapy.conf import settings

from mySpider.spiders.wechat2 import Wechat2Spider

process = CrawlerProcess(settings)
process.crawl(Wechat2Spider)
process.start()