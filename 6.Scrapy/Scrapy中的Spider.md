`Spider`类定义如何爬取指定的一个或多个网站，包括是否要跟进网页里的链接和如何提取网页内容中的数据。

爬取的过程是类似以下步骤的循环：

```
1.通过指定的初始URL初始化Request，并指定回调函数。当Request下载完后，生成Response作为参数传给回调函数。初始的Request是通过start_requests()读取start_urls中的URL来生成的，回调函数为parse()。
2.在回调函数中分析Response的内容，返回Item对象或者Request或包含二者的可迭代容器。返回Request对象经过Scrapy处理，下载相应的内容，并调用设置的回调函数。
3.在回调函数中，可以用选择器（或者Beautiful Soup，lxml这些解析器）来分析网页内容，生成Item。
4.生成的Item可以存入数据库，或存入到文件。
```

1.`Spider`类

```
class scrapy.spiders.Spider：最简单的爬虫类。

方法与属性：
name：爬虫名，要唯一。
allowed_domains：允许爬取的域名列表。
start_urls：初始的URL列表。
custom_settings：参数配置字典，必须是类属性，因为参数配置在实例化前被更新。
crawler：此属性是由from_crawler()设置的。
settings：运行此爬虫的设置。
logger：Python的日志记录器，通过爬虫名创建。
from_crawler(crawler, *args, **kwargs)：类方法，用于创建爬虫。crawler是Crawler的实例对象。
start_requests()：当打开爬虫时调用此方法。会用初始URL列表创建Request。只调用一次。
parse(response)：用于处理Response。
log(message[, level, component])：通过封装logger来发送日志消息。
closed(reason)：爬虫关闭时调用此方法。
```

2.爬虫参数

爬虫可以接受参数来改变它的行为。这些参数一般用来定义初始URL，或者限定爬取网站的部分内容，也可以用来配置其它任何功能。

在运行`crawl`命令时，通过`-a`选项来传递参数（键值对）：

```
scrapy crawl myspider -a category=electronics
```

然后可以在`__init__()`初始化函数里获取参数，如：

```
class MySpider(scrapy.Spider):
    name = 'myspider'
    
    def __init__(self, category=None, *args, **kwargs):  # 直接作为一个函数参数
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.example.com/categories/%s' % category]
```

而默认的`__init__()`函数会把这些参数定义为爬虫的属性，因此也可以这样用：

```
class MySpider(scrapy.Spider):
    name = 'myspider'
    
    def start_requests(self):
        yield scrapy.Request('http://www.example.com/categories/%s' % self.category)  # 作为一个属性
```

3.CrawlSpider

```
class scrapy.spiders.CrawlSpider：爬取一般网站的常用Spider。定义一些规则来跟进链接的方便机制。

方法和属性：
rules：包含一个或多个Rule对象的列表。如多个Rule匹配了相同链接，第一个被使用。
parse_start_url(response)：当start_urls的请求返回时调用此方法。分析最初的返回值并返回Item对象或者Request或包含二者的可迭代容器。
```

爬取规则（Rule）

```
class scrapy.spiders.Rule(link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=None)
参数：
link_extractor：LinkExtractor对象，定义了如何从页面提取链接。
callback：可调用对象或字符串，如果是字符串，Spider中同名的函数被调用。从link_extractor中每次获取到链接时调用。接受的参数为Repsonse，返回Item对象或者Request或包含二者的可迭代容器。编写爬虫规则时，不要使用parse作为回调，因为CrawlSpider使用parse来实现逻辑，如果覆盖了parse，CrawlSpider会运行失败。
cb_kwargs：传递给回调函数的参数字典。
follow：布尔值，从Response提取的链接是否跟进。如果callback为None，follow默认为True，否则默认为False。
process_links：可调用对象或字符串，如果是字符串，Spider中同名的函数被调用。从link_extractor中获取链接列表时调用，主要用来过滤。
process_request：可调用对象或字符串，如果是字符串，Spider中同名的函数被调用。提取到每个Request时调用，返回Request或None，用来过滤Request。
```

CrawlSpider配合Rule的例子：
```
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # 提取匹配 'category.php'，但不匹配'subsection.php'的链接，并跟进链接。
        # 没有callback，意味着follow的默认值为True
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # 提取匹配'item.php'的链接，并用parse_item这个方法来处理
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):  # TODO
        item = scrapy.Item()
        return item
```

4.XMLFeedSpider

```
class scrapy.spiders.XMLFeedSpider：通过迭代各个节点用于分析XML。迭代器可以从iternodes，xml和html中选择。而xml和html要先读取所有DOM，可能有性能问题，一般推荐使用iternodes。而html则能应对错误的XML。

方法和属性：
iterator：选用哪种迭代器，iternodes（默认），html，或xml。
itertag：开始迭代的节点名。
namespaces：(prefix, uri)形式的元组组成的列表。定义文档中会被处理的命名空间。register_namespace()被自动调用把prefix和uri生成命名空间。
adapt_response(response)：在分析Response前被调用，可以用来修改内容，返回的也是一个Response。
parse_node(response, selector)：当节点符合itertag时被调用。返回Item对象或者Request或包含二者的可迭代容器。
process_results(response, results)：返回结果（Item或Request）时被调用。用于对结果作最后的处理。返回结果的列表（Item或Request）。
```

5.CSVFeedSpider

```
class scrapy.spiders.CSVFeedSpider：与XMLFeedSpider相似，只是遍历的不是节点，而是行。

方法和属性：
delimiter：分隔符，默认为逗号。
quotechar：每个字段的特征，默认为双引号。
headers：用来提取字段的行的列表。
parse_row(response, row)：row是一个字典，键为提供的或检测出来的header。可以覆盖adapt_response和process_results来进行前处理和后处理。
```

6.SitemapSpider

```
class scrapy.spiders.SitemapSpider：通过Sitemaps来发现爬取的URL。支持嵌套的sitemap，并能从robots.txt中获取sitemap的URL。

方法和属性：
sitemap_urls：sitemap的URL列表，也可以是robots.txt。
sitemap_rules：(regex, callback)形式的元组列表。regex是匹配sitemap提供的URL的正则表达式。callback指定匹配后用于处理的函数。
sitemap_follow：用于匹配要跟进的sitemap的正则表达式的列表。默认情况所有sitemap都跟进。
sitemap_alternate_links：当一个URL有可选链接时，是否跟进。
sitemap_filter(entries)：过滤函数，可以覆盖它来基于sitemap入口的属性来选择它们。
```
