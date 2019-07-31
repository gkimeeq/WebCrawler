#!/usr/bin/env python
# coding=utf-8

from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import requests


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

    # title标签的子text节点
    print s.css('title::text').get()
    # id为images的所有子孙text节点
    print s.css('#images *::text').getall()

    # img标签存在，但没有text，所有空列表
    print s.css('img::text').getall()

    # a标签的href属性
    print s.css('a::attr(href)').getall()

    # 嵌套使用
    links = s.xpath('//a[contains(@href, "image")]')  # 具有href属性，且属性值包含image的a标签
    print links.getall()
    for index, link in enumerate(links):
        args = (index, link.xpath('@href').get(), link.xpath('img/@src').get())
        print u'第%d号链接指向的URL为%r，图片为%r' % args

    # 使用正则表达式
    print s.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')
    print s.xpath('//a[contains(@href, "image")]/text()').re_first(r'Name:\s*(.*)')


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


if __name__ == '__main__':
    print 'construct_selector()', '*' * 80
    construct_selector()
    print 'using_selector()', '*' * 80
    using_selector()
    print 'working_with_xpath()', '*' * 80
    working_with_xpath()
    print 'using_exslt_extension()', '*' * 80
    using_exslt_extension()

'''
输出为：

construct_selector() ********************************************************************************
[u'good']
good
[u'good']
good
[u'good']
good
using_selector() ********************************************************************************
[<Selector xpath='//title/text()' data=u'Example website'>]
[<Selector xpath=u'descendant-or-self::title/text()' data=u'Example website'>]
[u'Example website']
[u'Example website']
[u'http://example.com/']
[u'http://example.com/']
[u'image1.html', u'image2.html', u'image3.html', u'image4.html', u'image5.html']
[u'image1.html', u'image2.html', u'image3.html', u'image4.html', u'image5.html']
[u'image1_thumb.jpg', u'image2_thumb.jpg', u'image3_thumb.jpg', u'image4_thumb.jpg', u'image5_thumb.jpg']
[u'image1_thumb.jpg', u'image2_thumb.jpg', u'image3_thumb.jpg', u'image4_thumb.jpg', u'image5_thumb.jpg']
[u'image1_thumb.jpg', u'image2_thumb.jpg', u'image3_thumb.jpg', u'image4_thumb.jpg', u'image5_thumb.jpg']
image1_thumb.jpg
Example website
[u'\n       ', u'Name: My image 1 ', u'\n       ', u'Name: My image 2 ', u'\n       ', u'Name: My image 3 ', u'\n       ', u'Name: My image 4 ', u'\n       ', u'Name: My image 5 ', u'\n      ']
[]
[u'image1.html', u'image2.html', u'image3.html', u'image4.html', u'image5.html']
[u'<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>', u'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>', u'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>', u'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>', u'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']
第0号链接指向的URL为u'image1.html'，图片为u'image1_thumb.jpg'
第1号链接指向的URL为u'image2.html'，图片为u'image2_thumb.jpg'
第2号链接指向的URL为u'image3.html'，图片为u'image3_thumb.jpg'
第3号链接指向的URL为u'image4.html'，图片为u'image4_thumb.jpg'
第4号链接指向的URL为u'image5.html'，图片为u'image5_thumb.jpg'
[u'My image 1 ', u'My image 2 ', u'My image 3 ', u'My image 4 ', u'My image 5 ']
My image 1 
working_with_xpath() ********************************************************************************
<p>out</p>
<p>one</p>
<p>two</p>
<p>three</p>
<p>out</p>
<p>one</p>
<p>two</p>
<p>three</p>
<p>out</p>
<p>one</p>
<p>two</p>
<p>three</p>
--------------------------------------------------
<p>one</p>
<p>two</p>
<p>three</p>
<p>three</p>
--------------------------------------------------
<p>one</p>
<p>two</p>
<p>three</p>
[u'2014-07-23 19:00']
[u'<li>1</li>', u'<li>4</li>']
[u'<li>1</li>']
[u'<li>1</li>', u'<li>4</li>']
[u'<li>1</li>']
[u'Click here to go to the ', u'Next Page']
[u'Click here to go to the ']
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
[u'Click here to go to the Next Page']
[u'Click here to go to the Next Page']
[]
[u'<a href="#">Click here to go to the <strong>Next Page</strong></a>']
Name: My image 1 
images
[<Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="next" type="application/atom+'>, <Selector xpath='//link' data=u'<link xmlns:atom10="http://www.w3.org/20'>, <Selector xpath='//link' data=u'<link xmlns:atom10="http://www.w3.org/20'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>]
[<Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="next" type="application/atom+'>, <Selector xpath='//link' data=u'<link xmlns:atom10="http://www.w3.org/20'>, <Selector xpath='//link' data=u'<link xmlns:atom10="http://www.w3.org/20'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>, <Selector xpath='//link' data=u'<link rel="edit" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="self" type="application/atom+'>, <Selector xpath='//link' data=u'<link rel="alternate" type="text/html" h'>]
using_exslt_extension() ********************************************************************************
[u'link1.html', u'link2.html', u'link3.html', u'link4.html', u'link5.html']
[u'link1.html', u'link2.html', u'link4.html', u'link5.html']
当前scope： [u'http://schema.org/Product']
    属性：[u'name', u'aggregateRating', u'offers', u'description', u'review', u'review']
当前scope： [u'http://schema.org/AggregateRating']
    属性：[u'ratingValue', u'reviewCount']
当前scope： [u'http://schema.org/Offer']
    属性：[u'price', u'availability']
当前scope： [u'http://schema.org/Review']
    属性：[u'name', u'author', u'datePublished', u'reviewRating', u'description']
当前scope： [u'http://schema.org/Rating']
    属性：[u'worstRating', u'ratingValue', u'bestRating']
当前scope： [u'http://schema.org/Review']
    属性：[u'name', u'author', u'datePublished', u'reviewRating', u'description']
当前scope： [u'http://schema.org/Rating']
    属性：[u'worstRating', u'ratingValue', u'bestRating']
[<Selector xpath='//p[has-class("foo")]' data=u'<p class="foo bar-baz">First</p>'>, <Selector xpath='//p[has-class("foo")]' data=u'<p class="foo">Second</p>'>]
[<Selector xpath='//p[has-class("foo", "bar-baz")]' data=u'<p class="foo bar-baz">First</p>'>]
[]
'''
