# -*- coding: utf-8 -*-
# import sys
# sys.path.append("..")
import base64
import random
import re
import uuid

import os
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mySpider.items import MyspiderItem
from mySpider import settings
import requests

from mySpider.settings import IPPOOL


class WechatSpider(CrawlSpider):
    name = 'wechat'
    allowed_domains = ['weixin.sogou.com','mp.weixin.qq.com']

    # requests的请求头和代理
    proxy = random.choice(IPPOOL)

    proxies = {'http': 'http://' + proxy['ip']}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3386.1 Safari/537.36',
        "Proxy-Authorization": "Basic %s" % base64.b64encode(proxy['proxy_user_pass'].encode("utf-8")),
    }

    start_urls = []
    with open("微信公众号-定点跟踪.txt", 'r') as f:
        for i in f.readlines():
            start_urls.append('http://weixin.sogou.com/weixin?type=2&query=' + i.strip())


    # 每一页的匹配规则
    pagelink = LinkExtractor(allow=("query"))
    # 每一页里的每个帖子的匹配规则
    contentlink = LinkExtractor(allow=(r"/s"))

    rules = (
        Rule(pagelink),
        Rule(contentlink, callback="parse_item",follow=False)
    )

    def parse_item(self, response):
        item = MyspiderItem()
        # 标题
        item['title'] = response.xpath('//h2[@id="activity-name"]/text()').extract()[0].strip()
        # # 获取来源
        item['source'] = response.xpath('//a[@class="rich_media_meta rich_media_meta_link rich_media_meta_nickname"]/text()').extract()[0]
        # 获取发布时间
        item['datetime'] = response.xpath('//em[@id="post-date"]/text()').extract()[0]
        # 获取内容
        # 0.获取html
        html = response.body.decode('utf-8')
        # 1.获取文档
        text = re.search('<div class="rich_media_content " id="js_content">(.*?)<script nonce=', html, re.S).group(1).strip()

        # 2.获取所有img标签
        everyImg = re.findall('(<img.*?>)', text, re.S)

        for i in everyImg:
            # 3.提取url
            src = re.search('data-src="(.*?)"', i, re.S).group(1).strip()
            # 4.下载图片
            # 图片原始数据
            img = requests.get(src, headers=self.headers,proxies=self.proxies).content
            # 写入到本地磁盘文件内
            with open("pic/"+ str(uuid.uuid1()) + ".jpg", 'wb') as f:
                f.write(img)
            # 5.将原图片的url修改成本地的
            text = text.replace(src, "本地图片位置")

        item['content'] = text

        yield item