爬虫的主要目标是从页面爬取非结构性的数据然后提取出结构性数据。Scrapy提供`Item`类可以实现这样的要求。`Item`对象是简单的容器，用于保存爬取到的数据。

1.`Item`类

```
class scrapy.item.Item([arg])：返回一个新条目对象，可以传入参数进行初始化。

唯一属性：
fields：包含所有声明字段（declared field）和填充字段（populated field）的字典。键为字段名，值为Field对象。
```

2.`Field`类

```
class scrapy.item.Field([arg])：内置dict类的别名，没有额外提供更多的方法或属性。
```

3.声明`Item`

`Item`使用简单的类定义语法和`Field`对象来声明。

```
import scrapy

class Product(scrapy.Item):  # 继承自scrapy.Item，即scrapy.item.Item
    name = scrapy.Field()  # Field对像，即scrapy.item.Field，填充字段（populated field）
    price = scrapy.Field()
    stock = scrapy.Field()
    tags = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)  # 指定序列化函数为str，声明字段（declared field）
```

4.`Field`字段

`Field`对象指定了每个字段的元数据（metadata）。每个字段可以指明任何类型的元数据，接受的值没有任何限制。

5.对`Item`的操作

```
class Product(scrapy.Item):  # 继承自scrapy.Item，即scrapy.item.Item
    name = scrapy.Field()  # Field对像，即scrapy.item.Field，填充字段（populated field）
    price = scrapy.Field()
    stock = scrapy.Field()
    tags = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)  # 指定序列化函数为str，声明字段（declared field）

'''
通过继承来扩展Item，如增加更多的字段，修改某些字段的元数据等
'''
class DiscountProduct(Product):
    discount_percent = scrapy.Field(serializer=str)
    discount_expiration_date = scrapy.Field()


'''
扩展字段的元数据，如通过使用原字段的元数据、添加新的值、或改变原来的值
'''
class SpecificProduct(Product):
    name = scrapy.Field(Product.fields['name'], serializer=str)  # 添加或覆盖name字段的serializer这个元数据


if __name__ == '__main__':
    product = Product(name='Desktop PC', price=1000)  # 创建Product item对象
    print '*' * 40, 'product', '*' * 40
    print product

    # 获取字段
    print '*' * 40, u'获取字段', '*' * 40
    print product['name']  # 获得字段
    print product.get('name')  # 使用get方法获得字段，可以避免出错
    # print product['tags']  # 报KeyError的错误
    print product.get('tags', u'未设置')  # 因为tags还没有设置，所以返回未设置
    print product.get('foo', u'未知字段')  # foo不是有效字段，所以返回未知字段

    # 判断字段是否可用
    print '*' * 40, u'判断字段是否可用', '*' * 40
    print 'name' in product  # 是否为填充字段，True
    print 'foo' in product  # False
    print 'last_updated' in product  # False
    print 'last_updated' in product.fields  # 是否为声明字段，True
    print 'name' in product.fields  # True
    print 'foo' in product.fields  # False

    # 设置字段
    print '*' * 40, u'设置字段', '*' * 40
    product['last_updated'] = u'今天'
    print product['last_updated']
    # product['foo'] = u'未知字段'  # 报KeyError的错误

    # 访问所有字段
    print '*' * 40, u'访问所有字段', '*' * 40
    print product.keys()  # 键的集合
    print product.items()  # 键值对

    # 复制
    print '*' * 40, u'复制', '*' * 40
    product['tags'] = [1, 2, 3]
    product2 = Product(product)  # 浅复制
    product2['tags'][0] = 4  # product对应的值也被修改
    print 'product = ', product
    print 'product2 = ', product2
    product3 = product.copy()  # 浅复制
    product3['tags'][1] = 5  # product，product2对应的值也被修改
    print 'product = ', product
    print 'product2 = ', product2
    print 'product3 = ', product3
    product4 = product.deepcopy()  # 深复制
    product4['tags'][2] = 6  # product对应的值不变
    print 'product = ', product
    print 'product4 = ', product4

    # Item与字典间转换
    print '*' * 40, u'Item与字典间转换', '*' * 40
    print dict(product)  # 从items创建字典
    print Product({'name': 'computer', 'price': 1000})  # 从字典创建Item
    # print Product({'name': 'computer', 'price': 1000, 'foo': 'unknown'})  # 报KeyError的错误

'''
输出为：

**************************************** product ****************************************
{'name': 'Desktop PC', 'price': 1000}
**************************************** 获取字段 ****************************************
Desktop PC
Desktop PC
未设置
未知字段
**************************************** 判断字段是否可用 ****************************************
True
False
False
True
True
False
**************************************** 设置字段 ****************************************
今天
**************************************** 访问所有字段 ****************************************
['price', 'last_updated', 'name']
[('price', 1000), ('last_updated', u'\u4eca\u5929'), ('name', 'Desktop PC')]
**************************************** 复制 ****************************************
product =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 2, 3]}
product2 =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 2, 3]}
product =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 5, 3]}
product2 =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 5, 3]}
product3 =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 5, 3]}
product =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 5, 3]}
product4 =  {'last_updated': u'\u4eca\u5929',
 'name': 'Desktop PC',
 'price': 1000,
 'tags': [4, 5, 6]}
**************************************** Item与字典间转换 ****************************************
{'price': 1000, 'last_updated': u'\u4eca\u5929', 'name': 'Desktop PC', 'tags': [4, 5, 3]}
{'name': 'computer', 'price': 1000}
'''
```

源码可于github下载：[https://github.com/gkimeeq/WebCrawler](https://github.com/gkimeeq/WebCrawler)。
