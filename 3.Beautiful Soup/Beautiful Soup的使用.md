1.安装Beautiful Soup4
```
pip install beautifulsoup4
```

2.Linux CentOS-6.10安装lxml

Beautiful Soup支持一些第三方的解析器，如果不安装第三方的，则默认会用Python标准库中的HTML解析器。lxml解析器更加强大，速度更快，因此安装。

```
#yum install python-lxml
```

3.解析器对比

| 解析器 | 用法 | 优点 | 缺点 |
| :- | :- | :- | :- |
| Python标准库中的解析器，html.parser | BeautifulSoup(html, 'html.parser') | Python自带，不需要另外安装，速度还可以，兼容Python2.7.3和3.2 | 对Python2.7.3和3.2之前版本，兼容性不好 |
| lxml的HTML解析器，lxml | BeautifulSoup(html, 'lxml') | 速度更快，兼容性好 | 需要外部C的依赖 |
| lxml的XML解析器，lxml-xml，xml | BeautifulSoup(html, 'lxml-xml'), BeautifulSoup(html, 'xml') | 速度更快，只支持XML解析器 | 需要外部C的依赖 |
| html5lib解析器，html5lib | BeautifulSoup(html, 'html5lib') | 兼容性极好，用浏览器一样的方式解析网页，创建合法的HTML5 | 很慢，外部的Python依赖 |

4.四类对象Tag, NavigableString, BeautifulSoup, Comment

```
Tag：HTML中的标签。有两个重要的属性：name和attrs。
NavigableString：可以遍历的字符串，即Tag标签内部的文字。
BeautifulSoup：表示一个文档的全部内容。有时可以把它当作一个特殊Tag对象。没有attrs属性，而name属性返回[document]。
Comment：特殊类型的NavigableString对象，输出的内容不包括注释符号，如果处理不好，对文本处理会造成一定的麻烦。
```

5.遍历文档树
```
contents：将tag的子节点以列表的方式输出。仅包含tag的直接子节点。
children：子节点生成器，返回的是生成器，并不是列表。仅包含tag的直接子节点。
descendants：返回tag子孙节点的生成器。对所有的子孙节点进行递归。
string：如果tag只有一个NavigableString类型子节点，那么这个tag可以使用string得到子节点。如果tag包含多个子节点，输出结果则为None。
strings：遍历来获取多个内容。
stripped_string：类似strings，会把字符串中多余的空格空行等空白内容去除。
parent：父节点。
parents：递归得到元素的所有父辈节点。
next_sibling：当前节点的下一个兄弟节点。
previous_sibling：当前节点的前一个兄弟节点。
next_siblings：递归当前节点后的兄弟节点。
previous_siblings：递归当前节点前的兄弟节点。
next_element：当前节点的下一个节点，不分层次。
previous_element：当前节点的前一个节点，不分层次。
next_elements：向前依次访问节点，不分层次。
previous_elements：向后依次访问节点，不分层次。
```

6.搜索文档树

```
find_all(name, attrs, recursive, string, limit, **kwargs)：搜索当前tag的所有tag子节点，并过滤符合条件的节点。
name：按指定名查找tag，字符串对象自动忽略掉。如传入字符串，则查找与字符串完整匹配的内容。如传入正则表达式，则按正则表达式来匹配内容。如传入列表，则返回与列表中任一元素匹配的内容。如传入True，则匹配任何值，查找所有的tag，但不会返回字符串节点。如传入方法，该方法接受一个元素参数，如果返回True表示当前元素匹配并且被找到，如果不是要匹配到的，返回False。
attrs：通过指定css类（class）属性来搜索。由于class在Python是关键字，要用class_来指定。
recursive：默认会检索当前tag的所有子孙节点，如果只想搜索直接子节点，传入False。
string：通过指定字符串来搜索，而不是指定tag。同样可以传入字符串、正则表达式、列表、True和方法。
limit：指定要搜索多少条。如果文档比较大，可以节省搜索时间，而不需要搜索整个文档。
kwargs：如果指定的参数名不在find_all()的内置参数名之列（name, attrs, recursive, string, limit)，则会把这个参数当作tag的属性来搜索。

find(name, attrs, recursive, string, **kwargs)：直接返回找到的结果，与find_all()指定limit=1大致相同，只是find_all()返回一个列表，列表中是找到的所有结果。

find_parents(name, attrs, string, limit, **kwargs)：find_parent(name, attrs, string, **kwargs)：搜索当前节点的父辈节点。

find_next_siblings(name, attrs, string, limit, **kwargs)：find_next_sibling(name, attrs, string, **kwargs)：搜索当前节点所有后面的兄弟节点。

find_previous_siblings(name, attrs, string, limit, **kwargs)：find_previous_sibling(name, attrs, string, **kwargs)：搜索当前节点所有前面的兄弟节点。

find_all_next(name, attrs, string, limit, **kwargs)：find_next(name, attrs, string, **kwargs)：当前节点之后的节点和字符串。

find_all_previous(name, attrs, string, limit, **kwargs)：find_previous(name, attrs, string, **kwargs)：当前节点之前的节点和字符串。
```

7.CSS选择器

```
select()：通过CSS选择器来筛选。返回类型是列表。可以通过标签名、类名、id名、组合、属性等CSS选择器来查找。
```

8.修改文档树

```
修改tag名、属性和内容：name，['class']，string。
append()：添加到tag的内容。
extend()：把列表添加到tag的内容。
new_tag()：新的tag。
insert()：插入元素。
insert_before()：insert_after()：在前或后插入元素。
clear()：移除tag的内容。
extract()：移除tag或字符串，并返回移除的内容。
decompose()：移除tag或字符串，并销毁。
replace_with()：移除，并用新的替代。
wrap()：把元素包装到tag中。
unwrap()：wrap()的反向操作。
```

9.示例演示
```
#!/usr/bin/env python
# coding=utf-8

from bs4 import BeautifulSoup, NavigableString, Comment
import re

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""


def simple_use():
    soup = BeautifulSoup(html_doc, 'lxml')  # 创建BeautifulSoup对象，指定lxml解析器
    print soup.title  # title标签
    print soup.title.name  # 标签名
    print soup.title.string  # 标签内部内容
    print soup.title.parent.name  # 父标签名
    print soup.p  # p标签
    print soup.p['class']  # p标签的class属性
    print soup.a  # a标签
    print soup.find_all('a')  # 所有a标签，放在列表中
    print soup.find(id='link3')  # id='link3'的标签
    print soup.prettify()  # 格式化打印整个文档内容


def four_kinds_objects():
    # Tag
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'lxml')  # 创建BeautifulSoup对象，指定lxml解析器
    tag = soup.b  # b标签
    print '---------- Tag ----------'
    print type(tag)  # 类型
    print tag.name  # 标签名
    print tag['class']  # 标签的class属性
    print tag.attrs  # 标签的所有属性
    tag['id'] = 'verybold'  # 增加id属性
    print tag  # 打印标签
    print tag.attrs  # 标签的所有属性
    del tag['id']  # 删除id属性
    print tag.get('id')  # 获取id属性

    css_soup = BeautifulSoup('<p class="body strikeout"></p>', 'html.parser')  # 创建BeautifulSoup对象，使用Python的解析器
    print css_soup.p['class']  # 多值的属性
    id_soup = BeautifulSoup('<p id="my id"></p>', 'lxml')  # 创建BeautifulSoup对象，指定lxml解析器
    print id_soup.p['id']  # 单值属性

    # NavigableString
    print '---------- NavigableString ----------'
    print tag.string  # NavigableString对象
    print type(tag.string)  # 类型
    tag.string.replace_with('No longer bold')  # 把内容替换掉
    print tag

    # BeautifulSoup
    print '---------- BeautifulSoup ----------'
    print type(soup)  # 类型
    print soup.name  # 名字

    # Comment
    print '---------- Comment ----------'
    markup = '<b><!--Hey, buddy. Want to buy a used parser?--></b>'
    soup = BeautifulSoup(markup, 'lxml')
    comment = soup.b.string  # Comment对象
    print comment
    print type(comment)


def navigating_tree():
    soup = BeautifulSoup(html_doc, 'lxml')  # 创建BeautifulSoup对象，指定lxml解析器
    # 使用tag名
    print u'---------- 使用tag名 ----------'
    print soup.head
    print soup.title
    print soup.body.b
    print soup.a

    # contents
    print u'---------- contents ----------'
    print soup.head.contents
    print soup.head.contents[0]
    print soup.head.contents[0].contents

    # children
    print u'---------- children ----------'
    for child in soup.head.contents[0].children:
        print child

    # descendants
    print u'---------- descendants ----------'
    for c in soup.head.descendants:
        print c

    # string
    print u'---------- string ----------'
    print soup.head.contents[0].string
    print soup.head.string
    print soup.html.string

    # strings
    print u'---------- strings ----------'
    for s in soup.strings:
        print repr(s)

    # stripped_strings
    print u'---------- stripped_strings ----------'
    for s in soup.stripped_strings:
        print repr(s)

    # parent
    print u'---------- parent ----------'
    print soup.head.contents[0].parent
    print soup.html.parent
    print soup.parent

    # parents
    print u'---------- parents ----------'
    print soup.a
    for p in soup.a.parents:
        if p is None:
            print p
        else:
            print p.name

    sibling_soup = BeautifulSoup('<a><b>text1</b><c>text2</c></b></a>', 'lxml')
    # next_sibling, previous_sibling
    print u'---------- next_sibling, previous_sibling ----------'
    print sibling_soup.b.next_sibling
    print sibling_soup.c.previous_sibling
    print sibling_soup.b.previous_sibling
    print sibling_soup.c.next_sibling
    print sibling_soup.b.string.next_sibling
    print soup.a.next_sibling  # 一个逗号+换行
    print soup.a.next_sibling.next_sibling

    # next_siblings, previous_siblings
    print u'---------- next_siblings, previous_siblings ----------'
    for sibling in soup.a.next_siblings:
        print repr(sibling)
    for sibling in soup.find(id='link3').previous_siblings:
        print repr(sibling)

    # next_element, previous_element
    print u'---------- next_element, previous_element ----------'
    print soup.find('a', id='link3').next_element
    print soup.find('a', id='link3').previous_element
    print soup.find('a', id='link3').previous_element.next_element

    # next_elements, previous_elements
    print u'---------- next_elements, previous_elements ----------'
    for e in soup.find('a', id='link3').next_elements:
        print repr(e)
    print '-' * 50
    for e in soup.find(id='link3').previous_elements:
        print repr(e)


def search_tree():
    soup = BeautifulSoup(html_doc, 'lxml')  # 创建BeautifulSoup对象，指定lxml解析器
    print soup.find_all('b')  # 传标签名
    print '-' * 50
    for t in soup.find_all(re.compile(r'^b')):  # 传正则表达式
        print t.name
    print '-' * 50
    for t in soup.find_all(['a', 'b']):  # 传入列表
        print t.name
    print '-' * 50
    for t in soup.find_all(True):  # 传入True
        print t.name
    print '-' * 50
    print soup.find_all(lambda t: t.has_attr('class') and not t.has_attr('id'))  # 传入函数
    print '-' * 50
    print soup.find_all(id='link2')  # 指定属性
    print soup.find_all(attrs={'id': 'link3'})
    print soup.find_all('a', class_='sister')
    print soup.find_all(string='Elsie')
    print soup.find_all(string=['Tillie', 'Elsie', 'Lacie'])
    print soup.find_all('a', limit=1)
    print soup.find_all('title')
    print soup.find_all('title', recursive=False)


def css_selector():
    soup = BeautifulSoup(html_doc, 'lxml')  # 创建BeautifulSoup对象，指定lxml解析器
    print soup.select('title')  # 标签
    print '-' * 50
    print soup.select('p:nth-of-type(3)')
    print '-' * 50
    print soup.select('body a')  # 级联标签
    print '-' * 50
    print soup.select('html head title')
    print '-' * 50
    print soup.select('head > title')  # 直接级联标签
    print '-' * 50
    print soup.select('p > a')
    print '-' * 50
    print soup.select('p > a:nth-of-type(2)')
    print '-' * 50
    print soup.select('p > #link1')
    print '-' * 50
    print soup.select('body > a')
    print '-' * 50
    print soup.select('#link1 ~ .sister')  # 相邻
    print '-' * 50
    print soup.select('#link1 + .sister')
    print '-' * 50
    print soup.select('.sister')  # 类名
    print '-' * 50
    print soup.select('[class~=sister]')
    print '-' * 50
    print soup.select('#link1')  # ID
    print '-' * 50
    print soup.select('a#link2')
    print '-' * 50
    print soup.select('#link1,#link2')  # 匹配任意一个
    print '-' * 50
    print soup.select('a[href]')  # 存在属性
    print '-' * 50
    print soup.select('a[href="http://example.com/elsie"]')  # 属性值
    print '-' * 50
    print soup.select('a[href^="http://example.com/"]')
    print '-' * 50
    print soup.select('a[href$="tillie"]')
    print '-' * 50
    print soup.select('a[href*=".com/el"]')
    print '-' * 50
    print soup.select_one(".sister")  # 返回第一个


def modify_tree():
    # 改名和属性
    soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'lxml')
    tag = soup.b
    print tag
    tag.name = 'blockquote'
    tag['class'] = 'verybold'
    tag['id'] = 1
    print tag
    del tag['class']
    del tag['id']
    print tag

    # 改string
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    tag = soup.a
    tag.string = 'New link text'
    print '-' * 50
    print tag

    # append()
    soup = BeautifulSoup('<a>Foo</a>', 'lxml')
    soup.a.append('Bar')
    print '-' * 50
    print soup
    print soup.a.contents

    # extend()
    soup = BeautifulSoup('<a>Soup</a>', 'lxml')
    soup.a.extend(['\'s', ' ', 'on'])
    print '-' * 50
    print soup
    print soup.a.contents

    # NavigableString
    soup = BeautifulSoup('<b></b>', 'lxml')
    tag = soup.b
    tag.append('Hello')
    new_string = NavigableString(' there')
    tag.append(new_string)
    print '_' * 50
    print tag
    print tag.contents

    # Comment
    new_comment = Comment('Nice to see you.')
    tag.append(new_comment)
    print '_' * 50
    print tag
    print tag.contents

    # new_tag()
    soup = BeautifulSoup('<b></b>', 'lxml')
    original_tag = soup.b
    new_tag = soup.new_tag('a', href='http://www.example.com')
    original_tag.append(new_tag)
    print '_' * 50
    print original_tag
    new_tag.string = "Link text."
    print original_tag

    # insert()
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    tag = soup.a
    tag.insert(1, "but did not endorse ")
    print '_' * 50
    print tag
    print tag.contents

    # insert_before()
    soup = BeautifulSoup('<b>stop</b>')
    tag = soup.new_tag('i')
    tag.string = 'Don\'t'
    soup.b.string.insert_before(tag)
    print '_' * 50
    print soup.b

    # insert_after()
    div = soup.new_tag('div')
    div.string = 'ever'
    soup.b.i.insert_after(' you ', div)
    print '_' * 50
    print soup.b
    print soup.b.contents

    # clear()
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    tag = soup.a
    print '_' * 50
    tag.clear()
    print tag

    # extract()
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    a_tag = soup.a
    i_tag = soup.i.extract()
    print '_' * 50
    print a_tag
    print i_tag
    print i_tag.parent
    my_string = i_tag.string.extract()
    print my_string
    print my_string.parent
    print i_tag

    # decompose()
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    a_tag = soup.a
    soup.i.decompose()
    print '_' * 50
    print a_tag

    # replace_with()
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    a_tag = soup.a
    new_tag = soup.new_tag('b')
    new_tag.string = 'example.net'
    a_tag.i.replace_with(new_tag)
    print '_' * 50
    print a_tag

    # wrap()
    soup = BeautifulSoup('<p>I wish I was bold.</p>', 'lxml')
    print '_' * 50
    print soup.p.string.wrap(soup.new_tag('b'))
    print soup.p.wrap(soup.new_tag('div'))

    # unwrap()
    markup = '<a href="http://example.com/">I linked to <i>example.com</i></a>'
    soup = BeautifulSoup(markup, 'lxml')
    a_tag = soup.a
    a_tag.i.unwrap()
    print '_' * 50
    print a_tag


if __name__ == '__main__':
    print 'simple_use()', '*' * 100
    simple_use()
    print 'four_kinds_objects()', '*' * 100
    four_kinds_objects()
    print 'navigating_tree()', '*' * 100
    navigating_tree()
    print 'search_tree()', '*' * 100
    search_tree()
    print 'css_selector()', '*' * 100
    css_selector()
    print 'modify_tree()', '*' * 100
    modify_tree()
```

```
输出为：

simple_use() ****************************************************************************************************
<title>The Dormouse's story</title>
title
The Dormouse's story
head
<p class="title"><b>The Dormouse's story</b></p>
['title']
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister" href="http://example.com/tillie" id="link3">
    Tillie
   </a>
   ;
and they lived at the bottom of a well.
  </p>
  <p class="story">
   ...
  </p>
 </body>
</html>
four_kinds_objects() ****************************************************************************************************
---------- Tag ----------
<class 'bs4.element.Tag'>
b
['boldest']
{'class': ['boldest']}
<b class="boldest" id="verybold">Extremely bold</b>
{'class': ['boldest'], 'id': 'verybold'}
None
[u'body', u'strikeout']
my id
---------- NavigableString ----------
Extremely bold
<class 'bs4.element.NavigableString'>
<b class="boldest">No longer bold</b>
---------- BeautifulSoup ----------
<class 'bs4.BeautifulSoup'>
[document]
---------- Comment ----------
Hey, buddy. Want to buy a used parser?
<class 'bs4.element.Comment'>
navigating_tree() ****************************************************************************************************
---------- 使用tag名 ----------
<head><title>The Dormouse's story</title></head>
<title>The Dormouse's story</title>
<b>The Dormouse's story</b>
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
---------- contents ----------
[<title>The Dormouse's story</title>]
<title>The Dormouse's story</title>
[u"The Dormouse's story"]
---------- children ----------
The Dormouse's story
---------- descendants ----------
<title>The Dormouse's story</title>
The Dormouse's story
---------- string ----------
The Dormouse's story
The Dormouse's story
None
---------- strings ----------
u"The Dormouse's story"
u'\n'
u'\n'
u"The Dormouse's story"
u'\n'
u'Once upon a time there were three little sisters; and their names were\n'
u'Elsie'
u',\n'
u'Lacie'
u' and\n'
u'Tillie'
u';\nand they lived at the bottom of a well.'
u'\n'
u'...'
u'\n'
---------- stripped_strings ----------
u"The Dormouse's story"
u"The Dormouse's story"
u'Once upon a time there were three little sisters; and their names were'
u'Elsie'
u','
u'Lacie'
u'and'
u'Tillie'
u';\nand they lived at the bottom of a well.'
u'...'
---------- parent ----------
<head><title>The Dormouse's story</title></head>
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
</body></html>
None
---------- parents ----------
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
p
body
html
[document]
---------- next_sibling, previous_sibling ----------
<c>text2</c>
<b>text1</b>
None
None
None
,

<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
---------- next_siblings, previous_siblings ----------
u',\n'
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
u' and\n'
<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
u';\nand they lived at the bottom of a well.'
u' and\n'
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
u',\n'
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
u'Once upon a time there were three little sisters; and their names were\n'
---------- next_element, previous_element ----------
Tillie
 and

<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
---------- next_elements, previous_elements ----------
u'Tillie'
u';\nand they lived at the bottom of a well.'
u'\n'
<p class="story">...</p>
u'...'
u'\n'
--------------------------------------------------
u' and\n'
u'Lacie'
<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
u',\n'
u'Elsie'
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
u'Once upon a time there were three little sisters; and their names were\n'
<p class="story">Once upon a time there were three little sisters; and their names were\n<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,\n<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and\n<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;\nand they lived at the bottom of a well.</p>
u'\n'
u"The Dormouse's story"
<b>The Dormouse's story</b>
<p class="title"><b>The Dormouse's story</b></p>
u'\n'
<body>\n<p class="title"><b>The Dormouse's story</b></p>\n<p class="story">Once upon a time there were three little sisters; and their names were\n<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,\n<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and\n<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;\nand they lived at the bottom of a well.</p>\n<p class="story">...</p>\n</body>
u'\n'
u"The Dormouse's story"
<title>The Dormouse's story</title>
<head><title>The Dormouse's story</title></head>
<html><head><title>The Dormouse's story</title></head>\n<body>\n<p class="title"><b>The Dormouse's story</b></p>\n<p class="story">Once upon a time there were three little sisters; and their names were\n<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,\n<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and\n<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;\nand they lived at the bottom of a well.</p>\n<p class="story">...</p>\n</body></html>
search_tree() ****************************************************************************************************
[<b>The Dormouse's story</b>]
--------------------------------------------------
body
b
--------------------------------------------------
b
a
a
a
--------------------------------------------------
html
head
title
body
p
b
p
a
a
a
p
--------------------------------------------------
[<p class="title"><b>The Dormouse's story</b></p>, <p class="story">Once upon a time there were three little sisters; and their names were\n<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>,\n<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and\n<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;\nand they lived at the bottom of a well.</p>, <p class="story">...</p>]
--------------------------------------------------
[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
[<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
[u'Elsie']
[u'Elsie', u'Lacie', u'Tillie']
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
[<title>The Dormouse's story</title>]
[]
css_selector() ****************************************************************************************************
[<title>The Dormouse's story</title>]
--------------------------------------------------
[<p class="story">...</p>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<title>The Dormouse's story</title>]
--------------------------------------------------
[<title>The Dormouse's story</title>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
--------------------------------------------------
[]
--------------------------------------------------
[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
--------------------------------------------------
[<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>]
--------------------------------------------------
<a class="sister" href="http://example.com/elsie" id="link1">Elsie</a>
modify_tree() ****************************************************************************************************
<b class="boldest">Extremely bold</b>
<blockquote class="verybold" id="1">Extremely bold</blockquote>
<blockquote>Extremely bold</blockquote>
--------------------------------------------------
<a href="http://example.com/">New link text</a>
--------------------------------------------------
<html><body><a>FooBar</a></body></html>
[u'Foo', u'Bar']
--------------------------------------------------
<html><body><a>Soup's on</a></body></html>
[u'Soup', u"'s", u' ', u'on']
__________________________________________________
<b>Hello there</b>
[u'Hello', u' there']
__________________________________________________
<b>Hello there<!--Nice to see you.--></b>
[u'Hello', u' there', u'Nice to see you.']
__________________________________________________
<b><a href="http://www.example.com"></a></b>
<b><a href="http://www.example.com">Link text.</a></b>
__________________________________________________
<a href="http://example.com/">I linked to but did not endorse <i>example.com</i></a>
[u'I linked to ', u'but did not endorse ', <i>example.com</i>]
/home/pennlai/MachineLearning/FasterRCNN/BeautifulSoup.py:312: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.

The code that caused this warning is on line 312 of the file /home/pennlai/MachineLearning/FasterRCNN/BeautifulSoup.py. To get rid of this warning, pass the additional argument 'features="lxml"' to the BeautifulSoup constructor.

  soup = BeautifulSoup('<b>stop</b>')
__________________________________________________
<b><i>Don't</i>stop</b>
__________________________________________________
<b><i>Don't</i> you <div>ever</div>stop</b>
[<i>Don't</i>, u' you ', <div>ever</div>, u'stop']
__________________________________________________
<a href="http://example.com/"></a>
__________________________________________________
<a href="http://example.com/">I linked to </a>
<i>example.com</i>
None
example.com
None
<i></i>
__________________________________________________
<a href="http://example.com/">I linked to </a>
__________________________________________________
<a href="http://example.com/">I linked to <b>example.net</b></a>
__________________________________________________
<b>I wish I was bold.</b>
<div><p><b>I wish I was bold.</b></p></div>
__________________________________________________
<a href="http://example.com/">I linked to example.com</a>
```
