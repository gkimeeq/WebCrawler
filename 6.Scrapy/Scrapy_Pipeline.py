# coding=utf-8

from scrapy.exceptions import DropItem
import json
import pymongo


# 过滤价格的管道
class PricePipeline(object):
    vat_factor = 1.15

    def process_item(self, item, spider):
        if item.get('price'):
            if item.get('price_excludes_vat'):
                item['price'] = item['price'] * self.vat_factor  # 重新设置价格
            return item
        else:
            raise DropItem(u'缺失价格字段的Item：%s' % item)  # 没有price字段的Item，丢弃


# 把Item输出到JSON文件
class JsonWriterPipeline(object):
    def open_spider(self, spider):  # 打开spider时调用
        self.file = open('item.jl', 'w')  # 打开文件

    def close_spider(self, spider):  # 关闭spider时调用
        self.file.close()  # 关闭文件

    def process_item(self, item, spider):  # 实现把Item写入JSON
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item


# 把Item保存到MongoDB，如何使用from_crawler()清理资源
class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.collection_name = 'scrapy_items'
        self.mongo_uir = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):  # 用于创建管道实例
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),  # 从爬虫的设置里拿mongo_uri
                   mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'))  # 从爬虫的设置里拿mongo_db

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uir)  # Mongo客户端
        self.db = self.client[self.mongo_db]  # Mongo数据库

    def close_spider(self, spider):
        self.client.close()  # 关闭Mongo

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))  # 把Item保存到Mongo数据库
        return item


# 过滤重复的Item
class DuplicatePipeline(object):
    def __init__(self):
        self.ids_exist = set()  # 保存Item的id，每个id都唯一

    def process_item(self, item, spider):
        if item['id'] in self.ids_exist:
            raise DropItem(u'重复的Item：%s' % item)  # 丢弃id已经存在的Item
        else:
            self.ids_exist.add(item['id'])  # 把id加入到集合
            return item
