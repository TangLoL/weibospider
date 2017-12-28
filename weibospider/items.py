# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    issueTime = scrapy.Field() #发布时间
    terminal = scrapy.Field() #发布终端
    media = scrapy.Field() #多媒体
    blogLocation = scrapy.Field() #发布位置
    content = scrapy.Field() #内容
    userName = scrapy.Field() #用户名
    certifyStyle = scrapy.Field() #认证方式
    likesNum = scrapy.Field()  # 称赞数
    commentNum = scrapy.Field()  # 评论数
    transNum = scrapy.Field()  # 转发数
    birthday = scrapy.Field() #生日

    fansNum = scrapy.Field() #粉丝数
    focusNum = scrapy.Field() #关注数
    blogTotalNum = scrapy.Field()  # 总微博数

    userLocation = scrapy.Field() #用户地址
    regTime = scrapy.Field()  # 注册时间
    sex = scrapy.Field() # 性别
    blogLevel = scrapy.Field() #微博等级
    introduction = scrapy.Field() #简介
