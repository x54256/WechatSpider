# -*- coding: utf-8 -*-
import json
from scrapy.conf import settings
import pymongo
import redis

class MyspiderPipeline(object):

    def __init__(self):
        # 获取mongoDB的setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host,port=port)

        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]

        # 创建redis的连接
        self.redis_cli = redis.StrictRedis(host=settings['REDIS_HOST'], port=settings['REDIS_PORT'])


    def process_item(self, item, spider):
        data = dict(item)

        """进行去重"""
        # 判断该数据的title是否存在redis中
        flag = self.redis_cli.exists(item['title'])
        if not flag:
            # 不存在，插入mongo和redis中
            # redis
            self.redis_cli.set(item['title'],str(data))
            # mongo 向指定的表里添加数据
            self.post.insert(data)
        return item