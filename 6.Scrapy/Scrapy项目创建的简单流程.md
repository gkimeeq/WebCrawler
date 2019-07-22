1.进入到一个要创建Scrapy项目的文件夹，然后运行以下命令来生成默认的Scrapy项目结构。

在Linux CentOS-6.10中，运行

```
#scrapy startproject tutorial
```

然后生成的目录结构如下：

```
tutorial/
    scrapy.cfg
    tutorial/
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
```

2.定义Item

打开`items.py`，把`TutorialItem`类改为：

```
class TutorialItem(scrapy.Item):  # 继承于scrapy.Item类
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()  # 标题字段
    content = scrapy.Field()  # 内容字段
```

3.Spider爬虫

在`spiders`文件夹中新建`TutorialSpider.py`，代码如下：

```
# coding=utf-8

import scrapy

class TutorialSpider(scrapy.spiders.Spider):
    name = 'tutorial'  # 爬虫名称，要唯一，不同的Spider不能有相同的名称
    start_urls = ['http://www.example.com']  # 包含Spider在启动时进行爬取的URL列表，第一个被爬取的页面是列表中的其中一个，后续的URL则可从获取的数据中提取

    '''
    这是Spider的一个方法，被调用时，每个初始的URL完成下载后生成的Response对象会传递给这个方法。
    这个方法负责解析返回的Response数据、提取数据、生成进一步处理的URL的Request对象。
    '''
    def parse(self, response):
        filename = './tutorial.txt'
        with open(filename, 'wb') as f:
            f.write(response.url)  # 把URL写入文件
            f.write('\n')  # 写入换行
            f.write(response.body)  # 把响应的内容写入文件
```

然后在`tutorial`的目录下，运行
```
#scrapy crawl tutorial
```
运行完，会在此目录下生成`tutorial.txt`文件，运行`cat tutorial.txt`，得到的输出为：
```
http://www.example.com
<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style type="text/css">
    body {
        background-color: #f0f0f2;
        margin: 0;
        padding: 0;
        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;

    }
    div {
        width: 600px;
        margin: 5em auto;
        padding: 50px;
        background-color: #fff;
        border-radius: 1em;
    }
    a:link, a:visited {
        color: #38488f;
        text-decoration: none;
    }
    @media (max-width: 700px) {
        body {
            background-color: #fff;
        }
        div {
            width: auto;
            margin: 0 auto;
            border-radius: 0;
            padding: 1em;
        }
    }
    </style>
</head>

<body>
<div>
    <h1>Example Domain</h1>
    <p>This domain is established to be used for illustrative examples in documents. You may use this
    domain in examples without prior coordination or asking for permission.</p>
    <p><a href="http://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>
```

4.提取Item

Scrapy使用基于XPath和CSS表达式机制的选择器（Selector）来提取数据。

在`TutorialSipder.py`中，添加另一个Spider的子类，代码如下：

```
class TutorialSpider2(scrapy.spiders.Spider):
    name = 'tutorial2'  # 爬虫名称，要唯一，不同的Spider不能有相同的名称
    start_urls = ['http://www.example.com']  # 包含Spider在启动时进行爬取的URL列表，第一个被爬取的页面是列表中的其中一个，后续的URL则可从获取的数据中提取

    '''
    这是Spider的一个方法，被调用时，每个初始的URL完成下载后生成的Response对象会传递给这个方法。
    这个方法负责解析返回的Response数据、提取数据、生成进一步处理的URL的Request对象。
    '''

    def parse(self, response):
        filename = './tutorial2.txt'
        f = open(filename, 'wb')  # 打开文件
        title = response.xpath('//div/h1/text()').extract_first()  # 获取h1里的文本
        f.write(title)  # h1文本写入文件
        f.write('\n')  # 写入换行
        content = response.xpath('//div/p')[0].xpath('text()').get()  # 获取第一个p里的文本
        f.write(content)  # 第一个p里的文本写入文件
        f.write('\n')  # 写入换行
        f.close()  # 关闭文件
```

然后在`tutorial`的目录下，运行
```
#scrapy crawl tutorial2
```
运行完，会在此目录下生成`tutorial2.txt`文件，运行`cat tutorial2.txt`，得到的输出为：
```
Example Domain
This domain is established to be used for illustrative examples in documents. You may use this
    domain in examples without prior coordination or asking for permission.
```

接下来使用`TutorialItem`这个类。在`TutorialSipder.py`中，再添加一个Spider的子类，代码如下：
```
from tutorial.items import TutorialItem  # 导入TutorialItem

class TutorialSpider3(scrapy.spiders.Spider):
    name = 'tutorial3'  # 爬虫名称，要唯一，不同的Spider不能有相同的名称
    start_urls = ['http://www.example.com']  # 包含Spider在启动时进行爬取的URL列表，第一个被爬取的页面是列表中的其中一个，后续的URL则可从获取的数据中提取

    '''
    这是Spider的一个方法，被调用时，每个初始的URL完成下载后生成的Response对象会传递给这个方法。
    这个方法负责解析返回的Response数据、提取数据、生成进一步处理的URL的Request对象。
    '''

    def parse(self, response):
        title = response.xpath('//div/h1/text()').extract_first()  # 获取h1里的文本
        content = response.xpath('//div/p')[0].xpath('text()').get()  # 获取第一个p里的文本
        item = TutorialItem()
        item['title'] = title
        item['content'] = content
        yield item
```
然后在`tutorial`的目录下，运行
```
#scrapy crawl tutorial3
```
可以在终端看到运行信息。

5.保存数据

为了保存数据，可以在`pipelines.py`里编写item的管道，可以把item保存到数据库、文件等。这里不用管道，直接在运行时指定输出到一个JSON文件。

然后在`tutorial`的目录下，运行
```
#scrapy crawl tutorial3 -o tutorial3.json
```
运行完，会在此目录下生成`tutorial3.json`文件，运行`cat tutorial3.json`，得到的输出为：

```
[
{"content": "This domain is established to be used for illustrative examples in documents. You may use this\n    domain in examples without prior coordination or asking for permission.", "title": "Example Domain"}
]
```

源码可于github下载：[https://github.com/gkimeeq/WebCrawler](https://github.com/gkimeeq/WebCrawler)。
