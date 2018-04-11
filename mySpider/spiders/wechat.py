# -*- coding: utf-8 -*-
# import sys
# sys.path.append("..")
import re
import uuid

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from mySpider.items import MyspiderItem
import requests


class WechatSpider(CrawlSpider):
    name = 'wechat'
    allowed_domains = ['weixin.sogou.com','mp.weixin.qq.com']
    start_urls = ['http://weixin.sogou.com/weixin?type=2&query=中国']
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    # # 每一页的匹配规则
    # pagelink = LinkExtractor(allow=("dr"))
    # # 每一页里的每个帖子的匹配规则
    # contentlink = LinkExtractor(allow=("/s"))
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
        # # 获取内容
        # # 0.获取html
        # html = response.body.decode('utf-8')
        # # 1.获取文档
        # text = re.search('<div class="rich_media_content " id="js_content">(.*?)<script nonce=', html, re.S).group(1).strip()
        #
        # # 2.获取所有img标签
        # everyImg = re.findall('(<img.*?>)', text, re.S)
        #
        # for i in everyImg:
        #     # 3.提取url
        #     src = re.search('data-src="(.*?)"', i, re.S).group(1).strip()
        #     # 4.下载图片
        #     # 图片原始数据
        #     img = requests.get(src, headers=self.headers).content
        #     # 写入到本地磁盘文件内
        #     with open("pic/"+ str(uuid.uuid1()) + ".jpg", 'wb') as f:
        #         f.write(img)
        #     # 5.将原图片的url修改成本地的
        #     text = text.replace(src, "本地图片位置")
        #
        # item['content'] = text

        print(item)

        yield item
