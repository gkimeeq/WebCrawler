当Spider收集Item后会把它传递到Item管道，按照一定的顺序执行处理。每个Item管道组件是实现了简单方法的Python类，接收到Item后执行一些行为，可以决定此Item是否继续通过管道，或被丢弃。

Item管道的典型应用有：
```
1.清理HTML数据。
2.验证爬取的数据，检查Item是否有某些字段。
3.检查是否重复，可以丢弃。
4.将爬取的结果保存到数据库等。
```

1.编写Item管道

每个Item管道组件是一个独立的Python类，必须实现如下方法：

```
process_item(self, item, spider)：每个Item管道都调用此方法，返回一个字典，或Item对象，或抛出DropItem异常，抛出DropItem的将不会被后续的管道处理。

参数：
item：被爬取的Item对象
spider：爬取Item对象的Spider对象
```

每个Item管道组件也可以实现以下的额外方法：

```
open_spider(self, spider)：当spider被打开时调用。参数spider为被打开的Spider对象。
close_spider(self, spider)：当spider被关闭时调用。参数spider为被关闭的Spider对象。
from_crawler(cls, crawler)：如果实现了这个类方法，就会调用这个方法从Crawler创建管道实例。必须返回一个新的管道实例。而Crawler对象提供对所有Scrapy核心组件（如设置和信号）的访问。这样为管道提供了访问核心组件和链接Scrapy的方法。参数crawler为项目爬虫对象。
```

2.简单的例子

```
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
```

```
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
```

```
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
```

```
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
```

3.激活管道组件

在爬虫的配置文件（`settings.py`）中，添加`ITEM_PIPELINES`配置，如

```
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,
    'myproject.pipelines.JsonWriterPipeline': 800,
}
```

键表示引入的管道类，值用于指定执行的先后顺序，按数字从低到高的顺序执行，数字定义通常在0-1000的范围。

源码可于github下载：[https://github.com/gkimeeq/WebCrawler](https://github.com/gkimeeq/WebCrawler)。
