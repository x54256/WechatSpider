# coding:utf-8

import pymongo

client = pymongo.MongoClient('127.0.0.1', 27017)  # 建立与MongoDB的连接
# 有用户名和密码时：pymongo.MongoClient('mongodb://用户名:密码@localhost:27017/基于哪个数据库进行验证的')

db = client.WechatSpider  # 切换使用的数据库

# 增
# db.t1.insert_one({'name':'abc','age':18})

# 查
cursor = db.Wechat.find()     # 返回一个游标对象

for i in cursor:
    print(i)