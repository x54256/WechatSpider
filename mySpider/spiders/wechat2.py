# -*- coding: utf-8 -*-
import base64
import json
import random
import re
import uuid

import requests
import scrapy
from pyvirtualdisplay import Display
from selenium import webdriver

from mySpider.items import MyspiderItem
from mySpider.settings import IPPOOL


class Wechat2Spider(scrapy.Spider):
    name = 'wechat2'
    allowed_domains = ['weixin.sogou.com', 'mp.weixin.qq.com']

    start_urls = []
    with open("微信公众号-主题跟踪.txt", 'r') as f:
        for i in f.readlines():
            start_urls.append('http://weixin.sogou.com/weixin?type=1&query=' + i.strip())

    # requests的请求头和代理
    proxy = random.choice(IPPOOL)

    proxies = {'http': 'http://' + proxy['ip']}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3386.1 Safari/537.36',
        "Proxy-Authorization": "Basic %s" % base64.b64encode(proxy['proxy_user_pass'].encode("utf-8")),
    }

    # 初始化浏览器
    display = Display(visible=0, size=(800, 600))  # 初始化屏幕
    display.start()
    driver = webdriver.PhantomJS()  # 初始化PhantomJS
    # driver = webdriver.Chrome()  # 初始化ChromeDirver

    def parse(self, response):

        # 获取当前页面的所有微信公众号，只去第一个的链接
        url = response.xpath('//p/a/@href').extract()[0]

        # 用ChromeDirver发送请求，调用回调函数
        self.driver.get(url)

        html = self.driver.page_source
        self.driver.save_screenshot("test.png")
        # with open('1.html','wb') as f :
        #     f.write(html.decode('utf-8'))
        text = re.search('msgList = (.*?)seajs', html, re.S).group(1).strip()
        str = text[0:-1]
        print(str)
        jsonList = json.loads(str)['list']

        for i in jsonList:
            url = "http://mp.weixin.qq.com" + i['app_msg_ext_info']['content_url'].replace('amp;','')

            yield scrapy.Request(url=url, callback=self.detail_parse)


    # 数据解析方法，获取文章标题和内容
    def detail_parse(self, response):
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
            img = requests.get(src,proxies=self.proxies, headers=self.headers).content
            # 写入到本地磁盘文件内
            with open("pic/"+ str(uuid.uuid1()) + ".jpg", 'wb') as f:
                f.write(img)
            # 5.将原图片的url修改成本地的
            text = text.replace(src, "本地图片位置")

        item['content'] = text

        yield item