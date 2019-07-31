当抓取网页时，最常见的任务是从HTML源码中提取数据，用Beautiful Soup或lxml都可以。Beautiful Soup是基于HTML代码的结构来构造一个Python对象，对不良标记的处理也很合理，缺点就是慢。而lxml是基于ElementTree（不是Python标准库的一部分）的Python化的XML解析库，也可以解析HTML。

Scrapy提取数据的机制被称为选择器（Selector），通过特定的XPath或者CSS表达式来选择HTML文件中的某部分。Scrapy选择器构建于lxml之上，因此，选择器的速度与解析准确性都与lxml相似。

1.Selector对象

选择器的实例是对选择某些内容响应的封装。

```
class scrapy.selector.Selector(response=None, text=None, type=None, root=None, **kwargs)：
参数：
response：HtmlResponse或XmlResponse的对象，被用来选择和提取数据。
text：response不可用时的一个unicode字符串或utf-8编码的文本。与response一起用是未定义行为。
type：选择器的类型，可以为html，xml或None，None为默认。如不指定，HtmlResponse对应html，XmlResponse对应xml，其它为html。如果设定，不检测，而是强制用指定的。
root：根。
kwargs：其实的字典类型参数。

方法和属性：
xpath(query, namespaces=None, **kwargs)：找到匹配query的节点，返回SelectorList对象
css(query)：应用给定的css选择器，返回SelectorList对象。
get()：将匹配的节点通过一个unicode字符串进行串行化并返回。
attrib：属性字典。
re(regex, replace_entities=True)：用给定的正则表达式来返回匹配的unicode字符串列表。
re_first(regex, default=None, replace_entities=True)：用给定的正则表达式来返回第一个匹配的unicode字符串。如果没有匹配的，返回default。
register_namespace(prefix, uri)：注册给定的命名空间，此命名空间将会在选择器中使用。
remove_namespaces()：移除所有的命名空间。
__bool__()：如果选择了真实的内容，返回True，否则返回False。即选择器的布尔值通过它选择的内容决定。
getall()：将匹配的节点通过只有一个元素列表的unicode字符串进行串行化并返回。
```

2.SelectorList对象

Python内建list类的子类，只是提供了一些额外的方法。

```
class scrapy.selector.SelectorList

方法和属性：
xpath(xpath, namespaces=None, **kwargs)：对列表中每个元素调用xpath()方法。
css(query)：对列表中每个元素调用css()方法。
getall()：对列表中每个元素调用getall()方法。
get(default=None)：对列表中第一个元素调用get()方法。
re(regex, replace_entities=True)：对列表中每个元素调用re()方法。
re_first(regex, default=None, replace_entities=True)：对列表中每个元素调用re_first()方法。
attrib：返回列表中第一个元素的属性字典。
```

3.构造选择器

可以通过文本或TextResponse构造。

```
def construct_selector():
    # 通过文本构建
    body = '<html><body><span>good</span></body></html>'
    s = Selector(text=body)
    print s.xpath('//span/text()').extract()
    print s.xpath('//span/text()').get()

    # 通过TextResponse构建，HtmlResponse是TextResponse的一个子类
    response = HtmlResponse(url='http://example.com', body=body)
    s = Selector(response=response)
    print s.xpath('//span/text()').extract()
    print s.xpath('//span/text()').get()

    # response对象的selector属性
    print response.selector.xpath('//span/text()').extract()
    print response.selector.xpath('//span/text()').get()
```

4.使用选择器

Scrapy提供两个快捷方式使用选择器：`xpath(), css()`。

```
def using_selector():
    text = '''
    <html>
     <head>
      <base href="http://example.com/" />
      <title>Example website</title>
     </head>
     <body>
      <div id="images">
       <a href="image1.html">Name: My image 1 <br /><img src="image1_thumb.jpg" /></a>
       <a href="image2.html">Name: My image 2 <br /><img src="image2_thumb.jpg" /></a>
       <a href="image3.html">Name: My image 3 <br /><img src="image3_thumb.jpg" /></a>
       <a href="image4.html">Name: My image 4 <br /><img src="image4_thumb.jpg" /></a>
       <a href="image5.html">Name: My image 5 <br /><img src="image5_thumb.jpg" /></a>
      </div>
     </body>
    </html>
    '''
    s = Selector(text=text)  # 构建选择器

    # title标签的内容，返回选择器列表
    print s.xpath('//title/text()')
    print s.css('title::text')

    # 提取title标签的内容
    print s.xpath('//title/text()').extract()
    print s.css('title::text').extract()

    # base标签的href属性
    print s.xpath('//base/@href').extract()
    print s.css('base::attr(href)').extract()

    # 具有href属性，且属性值包含image的a标签的href属性
    print s.xpath('//a[contains(@href, "image")]/@href').extract()
    print s.css('a[href*=image]::attr(href)').extract()

    # 具有href属性，且属性值包含image的a标签下的img标签的src属性
    print s.xpath('//a[contains(@href, "image")]/img/@src').extract()
    print s.css('a[href*=image] img::attr(src)').extract()

    # img标签的src属性
    print s.css('img').xpath('@src').getall()  # 返回列表
    print s.css('img').attrib['src']  # 只返回第一个
```

5.XPath的使用

```
def working_with_xpath():
    text = '''
        <html>
         <body>
          <p>out</p>
          <div>
            <p>one</p>
          </div>
          <div>
            <p>two</p>
            <div>
                <p>three</p>
            </div>
          </div>
         </body>
        </html>
        '''
    s = Selector(text=text)  # 构建选择器

    # 相对XPaths
    divs = s.xpath('//div')
    for p in divs.xpath('//p'):  # 错误用法，仍然会从整个文档中取得p标签
        print p.get()
    print '-' * 50
    for p in divs.xpath('.//p'):  # div里面的p标签
        print p.get()
    print '-' * 50
    for p in divs.xpath('p'):  # div直系的p标签
        print p.get()

    # 如果由类查询，用css
    s = Selector(text='<div class="hero shout"><time datetime="2014-07-23 19:00">Special date</time></div>')
    print s.css('.shout').xpath('./time/@datetime').getall()

    # //node[1]与(//node)[1]的区别
    s = Selector(text='''
        <ul class="list">
            <li>1</li>
            <li>2</li>
            <li>3</li>
        </ul>
        <ul class="list">
            <li>4</li>
            <li>5</li>
            <li>6</li>
        </ul>
    ''')
    print s.xpath('//li[1]').getall()  # 所有父标签下的li的第一个
    print s.xpath('(//li)[1]').getall()  # 文档里的第一个li
    print s.xpath('//ul/li[1]').getall()  # 所有ul标签下的第一个li
    print s.xpath('(//ul/li)[1]').getall()  # 文档里的第一个ul下的第一个li

    # 文本节点，避免使用.//text()来传递给XPath的string函数，应使用.，因为.//text()返回一个节点集，只传递节点集中的第一个
    s = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')
    print s.xpath('//a//text()').getall()  # 返回节点集
    print s.xpath('string(//a[1]//text())').getall()  # 转换成string，只传递了节点集的第一个值
    print s.xpath("//a[1]").getall()  # 第一个节点
    print s.xpath('string(//a[1])').getall()  # 子孙节点的文本放一起传递
    print s.xpath('string(//a)').getall()  # 子孙节点的文本放一起传递
    print s.xpath("//a[contains(.//text(), 'Next Page')]").getall()  # 使用.//text()返回的是空列表
    print s.xpath("//a[contains(., 'Next Page')]").getall()  # 使用.，返回当前节点

    # XPath中的变量
    text = '''
        <html>
         <head>
          <base href="http://example.com/" />
          <title>Example website</title>
         </head>
         <body>
          <div id="images">
           <a href="image1.html">Name: My image 1 <br /><img src="image1_thumb.jpg" /></a>
           <a href="image2.html">Name: My image 2 <br /><img src="image2_thumb.jpg" /></a>
           <a href="image3.html">Name: My image 3 <br /><img src="image3_thumb.jpg" /></a>
           <a href="image4.html">Name: My image 4 <br /><img src="image4_thumb.jpg" /></a>
           <a href="image5.html">Name: My image 5 <br /><img src="image5_thumb.jpg" /></a>
          </div>
         </body>
        </html>
    '''
    s = Selector(text=text)
    print s.xpath('//div[@id=$val]/a/text()', val='images').get()  # $val是变量，通过参数val来传递
    print s.xpath('//div[count(a)=$cnt]/@id', cnt=5).get()  # $cnt是变量，通过参数cnt来传递

    # 移除命名空间（看不出区别）
    html = requests.get(url='https://feeds.feedburner.com/PythonInsider')
    response = HtmlResponse(url='https://feeds.feedburner.com/PythonInsider', body=html.text, encoding='utf-8')
    print response.xpath('//link')
    response.selector.remove_namespaces()  # 移除命名空间
    print response.xpath('//link')
```

6.使用EXSLT扩展

```
# 使用EXSLT扩展
def using_exslt_extension():
    # 正则表达式操作
    doc = '''
        <div>
            <ul>
                <li class="item-0"><a href="link1.html">first item</a></li>
                <li class="item-1"><a href="link2.html">second item</a></li>
                <li class="item-inactive"><a href="link3.html">third item</a></li>
                <li class="item-1"><a href="link4.html">fourth item</a></li>
                <li class="item-0"><a href="link5.html">fifth item</a></li>
            </ul>
        </div>
    '''
    s = Selector(text=doc, type='html')
    print s.xpath('//li//@href').getall()
    # 当starts-with()或contains()失效时，使用test()函数
    print s.xpath('//li[re:test(@class, "tem-\d$")]//@href').getall()  # 类名以数字结尾

    # 集合操作
    doc = '''
        <div itemscope itemtype="http://schema.org/Product">
            <span itemprop="name">Kenmore White 17" Microwave</span>
            <img src="kenmore-microwave-17in.jpg" alt='Kenmore 17" Microwave' />
            <div itemprop="aggregateRating"
                itemscope itemtype="http://schema.org/AggregateRating">
                Rated <span itemprop="ratingValue">3.5</span>/5
                based on <span itemprop="reviewCount">11</span> customer reviews
            </div>
            
            <div itemprop="offers" itemscope itemtype="http://schema.org/Offer">
                <span itemprop="price">$55.00</span>
                <link itemprop="availability" href="http://schema.org/InStock" />In stock
            </div>
            
            Product description:
            <span itemprop="description">0.7 cubic feet countertop microwave.
            Has six preset cooking categories and convenience features like
            Add-A-Minute and Child Lock.</span>
            
            Customer reviews:
            
            <div itemprop="review" itemscope itemtype="http://schema.org/Review">
                <span itemprop="name">Not a happy camper</span> -
                by <span itemprop="author">Ellie</span>,
                <meta itemprop="datePublished" content="2011-04-01">April 1, 2011
                <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
                    <meta itemprop="worstRating" content = "1">
                    <span itemprop="ratingValue">1</span>/
                    <span itemprop="bestRating">5</span>stars
                </div>
                <span itemprop="description">The lamp burned out and now I have to replace
                it. </span>
            </div>
            
            <div itemprop="review" itemscope itemtype="http://schema.org/Review">
                <span itemprop="name">Value purchase</span> -
                by <span itemprop="author">Lucas</span>,
                <meta itemprop="datePublished" content="2011-03-25">March 25, 2011
                <div itemprop="reviewRating" itemscope itemtype="http://schema.org/Rating">
                    <meta itemprop="worstRating" content = "1"/>
                    <span itemprop="ratingValue">4</span>/
                    <span itemprop="bestRating">5</span>stars
                </div>
                <span itemprop="description">Great microwave for the price. It is small and
                fits in my apartment.</span>
            </div>
            ...
        </div>
    '''
    s = Selector(text=doc, type='html')
    for scope in s.xpath('//div[@itemscope]'):
        print u'当前scope：', scope.xpath('@itemtype').getall()
        props = scope.xpath('set:difference(./descendant::*/@itemprop, .//*[@itemscope]/*/@itemprop)')
        print u'    属性：%s' % props.getall()

    # 其它XPath扩展
    text = '''
        <p class="foo bar-baz">First</p>
        <p class="foo">Second</p>
        <p class="bar">Third</p>
        <p>Fourth</p>
    '''
    s = Selector(text=text)
    print s.xpath('//p[has-class("foo")]')  # 有foo这个类的p标签
    print s.xpath('//p[has-class("foo", "bar-baz")]')  # 同时有foo，bar-baz这两个类的p标签
    print s.xpath('//p[has-class("foo", "bar")]')  # 同时有foo，bar这两个类的p标签
```

源码可于github下载：[https://github.com/gkimeeq/WebCrawler](https://github.com/gkimeeq/WebCrawler)。
