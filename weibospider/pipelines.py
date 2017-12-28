# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import datetime


class WeibospiderPipeline(object):



    def __init__(self):
        print('pipelines的init---')
        pass

    def process_item(self, item, spider):
        print('正在写入文件')
        line = item['issueTime'] + '\t' + \
            item['userName'] + '\t' + \
            item['content'] + '\t' + \
            item['media'] + '\t' + \
            item['likesNum'] + '\t' + \
            item['commentNum'] + '\t' + \
            item['transNum'] + '\t' + \
            item['blogLocation'] + '\t' + \
            item['terminal'] + '\t' + \
            item['certifyStyle'] + '\t' + \
            item['fansNum'] + '\t' + \
            item['focusNum'] + '\t' + \
            item['blogTotalNum'] + '\t' + \
            item['userLocation'] + '\t' + \
            item['regTime'] + '\t' + \
            item['birthday'] + '\t' + \
            item['sex'] + '\t' + \
            item['blogLevel'] + '\t' + \
            item['introduction'] + '\n'
        self.file.write(line)
        return item

    def open_spider(self, spider):
        filename = str(datetime.datetime.now()).split('.')[0]\
                       .replace('-','').replace(':','')\
                       .replace(' ','') + '.csv'

        print('生成文件，文件地址为'+ filename)

        self.file = open(filename,mode='w+',encoding='utf-8')

        self.file.write('发布时间'+'\t'+'用户名'+'\t'+'内容'+'\t'+'多媒体'+'\t'+'称赞数'+'\t'+
                        '评论数'+'\t'+'转发数'+'\t'+'发布位置'+'\t'+'发布终端'+'\t'+'认证方式'+'\t'+
                        '粉丝数'+'\t'+'关注数'+'\t'+'总微博数'+'\t'+'用户地址'+'\t'+'注册时间'+'\t'+
                        '生日'+'\t'+'性别'+'\t'+'微博等级'+'\t'+'简介'+'\n')


    def close_spider(self,spider):
        self.file.close()
        print('文件关闭')

