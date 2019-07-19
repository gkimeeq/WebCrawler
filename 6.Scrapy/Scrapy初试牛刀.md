1.安装

```
pip install configparser  # 依赖
pip install Scrapy
```

2.官网的一个简单例子

[https://docs.scrapy.org/en/latest/intro/overview.html](https://docs.scrapy.org/en/latest/intro/overview.html)

```
#!/usr/bin/env python
# coding=utf-8

import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.xpath('span/small/text()').get()
            }
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
```

在Linux CentOS 6-10下：

```
$cd
$vi quotes_spider.py
```

然后把上面的代码粘上去，`:wq`保存并退出`vi`。然后运行这个爬虫。

```
$scrapy runspider quotes_spider.py -o ./quotes.json
```

跑完后，会在当前目录下生成`quotes.json`。

```
$cat quotes.json
```

显示输出文件的内容：

```
[
{"text": "\u201cThe person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.\u201d", "author": "Jane Austen"},
{"text": "\u201cA day without sunshine is like, you know, night.\u201d", "author": "Steve Martin"},
{"text": "\u201cAnyone who thinks sitting in church can make you a Christian must also think that sitting in a garage can make you a car.\u201d", "author": "Garrison Keillor"},
{"text": "\u201cBeauty is in the eye of the beholder and it may be necessary from time to time to give a stupid or misinformed beholder a black eye.\u201d", "author": "Jim Henson"},
{"text": "\u201cAll you need is love. But a little chocolate now and then doesn't hurt.\u201d", "author": "Charles M. Schulz"},
{"text": "\u201cRemember, we're madly in love, so it's all right to kiss me anytime you feel like it.\u201d", "author": "Suzanne Collins"},
{"text": "\u201cSome people never go crazy. What truly horrible lives they must lead.\u201d", "author": "Charles Bukowski"},
{"text": "\u201cThe trouble with having an open mind, of course, is that people will insist on coming along and trying to put things in it.\u201d", "author": "Terry Pratchett"},
{"text": "\u201cThink left and think right and think low and think high. Oh, the thinks you can think up if only you try!\u201d", "author": "Dr. Seuss"},
{"text": "\u201cThe reason I talk to myself is because I\u2019m the only one whose answers I accept.\u201d", "author": "George Carlin"},
{"text": "\u201cI am free of all prejudice. I hate everyone equally. \u201d", "author": "W.C. Fields"},
{"text": "\u201cA lady's imagination is very rapid; it jumps from admiration to love, from love to matrimony in a moment.\u201d", "author": "Jane Austen"}
]
```

3.执行过程

3.1.当执行命令
```
$scrapy runspider quotes_spider.py -o ./quotes.json
```
Scrapy查找定义在`quotes_spider.py`的Spider（这里是Spider的子类，`QuotesSpider`），然后通过爬虫Engine开始运行。

3.2.爬虫入口

在`QuotesSpider`里定义的`start_urls`是爬虫的初始URL列表。爬虫从这个列表中拿到URL，创建Request，得到返回的Response，然后调用默认的回调方法`parse`，传入的参数就是返回的Response。

3.3.处理响应

在`parse`方法中，通过CSS选择器来提取想要的引用元素，用提取到的内容生成一个字典。对于额外的链接，由调度器生成另外的Request，回调方法同样是`parse`。
