1.安装
```
pip install lxml
```
在Linux CentOS-6.10下可以这样安装：

```
yum install python-lxml
```

2.简单导入
```
import xml.etree.ElementTree as etree  # Python 2.7.16
```

3._ElementInterface类
```
http://effbot.org/zone/pythondoc-elementtree-ElementTree.htm#elementtree.ElementTree._ElementInterface-class

_ElementInterface(tag, attrib)：内部元素类，用于定义元素接口。不能直接创建此类的实例，要用Element类和SubElement类代替。
参数：
tag：元素名称。
attrib：元素的属性字典。

方法与属性：
__delitem__(index)：删除给定的子元素。
__delslice__(start, stop)：删除从start到stop的子元素，不包含stop。
__getitem__(index)：返回给定的子元素。
__getslice__(start, stop)：返回从start到stop的子元素列表，不包含stop。
__len__()：子元素个数。
__setitem__(index, element)：设置子元素。
__setslice__(start, stop, elements)：设置从start到stop的子元素，不包含stop。
append(element)：在元素末尾添加一个子元素。
clear()：清除元素，包括把所有的子元素、属性、tail、text都删除或设置为None。
find(path)：传入名称或路径，返回找到的第一个子元素，没有找到就返回None。
findall(path)：传入名称或路径，返回找到的所有子元素的列表。
findtext(path, default=None)：传入名称或路径，返回找到的第一个子元素的字符串，没有找到就返回default给定的值。
get(key, default=None)：获取属性值，如果不存在，返回default值。
getchildren()：返回所有子元素列表。
getiterator(tag=None)：返回列表或迭代器，包含了tag指定的元素及其所有子元素，按文档的顺序。如果文档在迭代过程中被修改了，结果是未定义的。
insert(index, element)：在指定位置插入元素。
items()：返回属性的元组，(string, string)。
keys()：所有属性名列表。
makeelement(tag, attrib)：创建一个新的元素，与当前元素有相同的类型。
remove(element)：删除子元素，此子元素是通过对比id来匹配。
set(key, value)：设置元素属性。
attrib：属性字典，如果可以的话，用get，set，keys，items来访问属性。
tail：在标签结束后，下一个兄弟元素之前的字符串。
text：第一个子元素前的字符串。
```

4.Element工厂
```
http://effbot.org/zone/pythondoc-elementtree-ElementTree.htm#elementtree.ElementTree.Element-function

Element(tag, attrib={}, **extra)：返回一个元素对象。
参数：
tag：元素名
attrib：属性字典
extra：额外的属性

元素的方法与属性参考_ElementInterface类。
```

5.ElementTree类
```
http://effbot.org/zone/pythondoc-elementtree-ElementTree.htm#elementtree.ElementTree.ElementTree-class

ElementTree(element=None, file=None)：用于包装文档为文档树。
参数：
element：根元素。
file：文件名或文件对象，文件的内容用于初始化文档树。

方法和属性：
_setroot(element)：设置根元素。
find(path)：传入名称或路径，返回找到的第一个顶层元素，没有找到就返回None。类似于getroot().find(path)。
findall(path)：传入名称或路径，返回找到的所有顶层元素的列表。类似于getroot().findall(path)。
findtext(path, default=None)：传入名称或路径，返回找到的第一个顶层元素的字符串，没有找到就返回default给定的值。类似于getroot().findtext(path)。
getiterator(tag=None)：根元素的迭代器，迭代整个文档树。
getroot()：获取根元素。
parse(source, parser=None)：导入XML文件。
write(file, encoding=”us-ascii”)：保存文档树为XML文件。
```

6.SubElement工厂
```
SubElement(parent, tag, attrib={}, **extra)：创建子元素。
参数：
parent：父元素
tag：元素名
attrib：属性字典
extra：额外的属性

元素的方法与属性参考_ElementInterface类。
```

7.一些函数
```
dump(elem)：输出到sys.stdout。用于debug。
fromstring(text)：解析XML的字符串，返回元素对象。
iselement(element)：是否为元素。
parse(source, parser=None)：解析XML文档为文档树。
tostring(element, encoding=None)：返回元素的XML字符串。
XML(text)：同fromstring(text)。
```

8.简单的使用演示
```
#!/usr/bin/env python
# coding=utf-8

import xml.etree.ElementTree as etree
from io import BytesIO


# https://lxml.de/tutorial.html

def test_element():
    html = etree.Element('html')  # 创建一个元素
    body = etree.Element('body')
    html.append(body)  # 添加一个子元素
    div1 = etree.SubElement(body, 'div')
    div2 = etree.SubElement(body, 'div')
    div1.set('class', 'head')
    div1.text = 'hello world!'
    div2.text = u'你好！'
    print etree.tostring(html,
                         encoding='utf-8')  # <html><body><div class="head">hello world!</div><div>你好！</div></body></html>

    child = html[0]
    print child.tag  # body
    print len(child)  # 2
    for c in body:
        print c.text  # hello world! 你好！
    p = etree.Element('p')
    body.insert(0, p)
    print len(body)  # 3
    start = body[:1]
    end = body[-1:]
    print start[0].tag  # p
    print end[0].tag  # div
    print etree.iselement(body)  # True

    print div1.get('class')  # head
    print div2.get('class')  # None
    div1.set('style', 'border: 1px solid red;')
    print div1.keys()  # ['style', 'class']
    for k, v in div1.items():
        print '%s = %s' % (k, v)  # style = border: 1px solid red; class = head
    print div1.attrib  # {'style': 'border: 1px solid red;', 'class': 'head'}

    p.text = u'一段文字'
    p.tail = u'结尾'
    print etree.tostring(html,
                         encoding='utf-8')  # <html><body><p>一段文字</p>结尾<div class="head" style="border: 1px solid red;">hello world!</div><div>你好！</div></body></html>

    for e in html.iter():
        print '%s - %s' % (e.tag, e.text)  # html - None body - None p - 一段文字 div - hello world! div - 你好！
    for e in html.iter('div'):
        print '%s - %s' % (e.tag, e.text)  # div - hello world! div - 你好！

    s = etree.tostring(html, encoding='utf-8')
    another_html = etree.XML(s)
    print etree.tostring(another_html,
                         encoding='utf-8')  # <html><body><p>一段文字</p>结尾<div class="head" style="border: 1px solid red;">hello world!</div><div>你好！</div></body></html>
    print etree.tostring(another_html, encoding='utf-8', method='text')  # 一段文字结尾hello world!你好！


def test_element_tree():
    xml = '''<?xml version="1.0"?>
    <bookshop>
        <book>
            <name>C</name>
            <author>unknown</author>
        </book>
        <book>
            <name>Algorithm</name>
            <author>GG</author>
        </book>
    </bookshop>
    '''
    tr = etree.ElementTree(xml)
    print type(tr.getroot())  # <type 'str'>
    print tr.getroot()


def test_from_string_file():
    xml = '''<?xml version="1.0"?>
    <bookshop>
        <book>
            <name>C</name>
            <author>unknown</author>
        </book>
        <book>
            <name>Algorithm</name>
            <author>GG</author>
        </book>
    </bookshop>
    '''
    e1 = etree.fromstring(xml)
    print etree.tostring(e1, encoding='utf-8')
    e2 = etree.XML(xml)
    print etree.tostring(e2, encoding='utf-8')
    tr = etree.parse(BytesIO(xml))
    print etree.tostring(tr.getroot(), encoding='utf-8')


if __name__ == '__main__':
    print 'test_element()', '*' * 100
    test_element()
    print 'test_element_tree()', '*' * 100
    test_element_tree()
    print 'test_from_string_file()', '*' * 100
    test_from_string_file()


'''
输出为：

test_element() ****************************************************************************************************
<html><body><div class="head">hello world!</div><div>你好！</div></body></html>
body
2
hello world!
你好！
3
p
div
True
head
None
['style', 'class']
style = border: 1px solid red;
class = head
{'style': 'border: 1px solid red;', 'class': 'head'}
<html><body><p>一段文字</p>结尾<div class="head" style="border: 1px solid red;">hello world!</div><div>你好！</div></body></html>
html - None
body - None
p - 一段文字
div - hello world!
div - 你好！
div - hello world!
div - 你好！
<html><body><p>一段文字</p>结尾<div class="head" style="border: 1px solid red;">hello world!</div><div>你好！</div></body></html>
一段文字结尾hello world!你好！
test_element_tree() ****************************************************************************************************
<type 'str'>
<?xml version="1.0"?>
    <bookshop>
        <book>
            <name>C</name>
            <author>unknown</author>
        </book>
        <book>
            <name>Algorithm</name>
            <author>GG</author>
        </book>
    </bookshop>
    
test_from_string_file() ****************************************************************************************************
<bookshop>
        <book>
            <name>C</name>
            <author>unknown</author>
        </book>
        <book>
            <name>Algorithm</name>
            <author>GG</author>
        </book>
    </bookshop>
<bookshop>
        <book>
            <name>C</name>
            <author>unknown</author>
        </book>
        <book>
            <name>Algorithm</name>
            <author>GG</author>
        </book>
    </bookshop>
<bookshop>
        <book>
            <name>C</name>
            <author>unknown</author>
        </book>
        <book>
            <name>Algorithm</name>
            <author>GG</author>
        </book>
    </bookshop>
'''
```
