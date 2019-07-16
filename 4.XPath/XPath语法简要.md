XPath是在XML文档中查找信息的语言，可对元素和属性进行遍历。

利用以下的XML内容。

```
<bookshop>
    <book>
        <name>Introduction to Algorithms</name>
        <author>Thomas H. Cormen, etc.</author>
        <price>68.00</price>
    </book>
    <book>
        <name>Deep Learning</name>
        <author>Ian Goodfellow, etc.</author>
        <price>610.00</price>
    </book>
</bookshop>
```

1.节点关系
```
父节点（parent）：上一级节点，只有一个。book的父节点是bookshop。
子节点（child）：下一级节点，可有一个，多个或零个。book的子节点有name，author，price。
兄弟同胞（sibling）：有相同父节点的节点。name，author，price的父节点都是book，它们是兄弟同胞关系。
先辈（ancestor）：节点的父节点，父节点的父节点，等等。name的先辈有book，bookshop。
后辈（descendant）：节点的子节点，子节点的子节点，等等。bookshop的后辈有book，name，author，price。
```

2.节点选取

| 表达式 | 说明 | 例子 | 例子的结果说明 |
| :-: | :- | :- | :- |
| nodename | 节点的所有子节点 | bookshop | bookshop元素的所有子节点 |
| / | 从根节点选取 | /bookshop<br>bookshop/book | 根元素bookshop，由正斜杠（/）开始的代表着绝对路径<br>选取bookshop的所有book子元素 |
| // | 从匹配选择的当前节点选择文档中的节点，不考虑位置 | //book<br>bookshop//book | 选取所有book的子元素，不管在文档中的什么位置<br>选择bookshop后代的所有book元素，不管位于bookshop下的什么位置 |
| . | 当前节点 |  |  |
| .. | 当前节点的父节点 |  |  |
| @ | 选取属性 | //@lang | 选取名为lang的所有属性 |
| * | 匹配任何元素节点 | /bookshop/\*<br>//\* | bookshop元素的所有子元素<br>文档中的所有元素 |
| @* | 匹配任何属性节点 | //name[@*] | 所有带有属性的name元素 |
| node() | 匹配任何类型的节点 |  |  |

3.节点索引

| 例子 | 例子的结果说明 |
| :- | :- |
| /bookshop/book[1] | bookshop的第一个book |
| /bookshop/book[last()] | bookshop的倒数第一个book |
| /bookshop/book[last()-1] | bookshop的倒数第二个book |
| /bookshop/book[position() < 3] | bookshop的前两个book |
| /bookshop/book[price > 100.00] | bookshop中的所有book，并且price的值大于100.00 |
| /bookshop/book[price > 100.00]/name | bookshop中的book的所有name，并且price的值大于100.00 |
| //name[@lang] | 所有name元素，并且这些元素有lang属性 |
| //name[@lang='eng'] | 所有name元素，并且lang属性的值为eng |
| //book/name \| //book/price | book的所有name和price |
| //name \| //price | 文档中的所有name和price |
| /bookshop/book/name \| //price | bookshop的book的所有name，以及文档中的所有price |

4.轴

| 轴名 | 说明 | 例子 | 例子的结果说明 |
| :-: | :- | :- | :- |
| ancestor | 当前节点的所有先辈（父、祖父等） | ancestor::book | 当前节点的所有 book 先辈 |
| ancestor-or-self | 当前节点的所有先辈（父、祖父等）以及当前节点本身 | ancestor-or-self::book | 当前节点的所有 book 先辈以及当前节点（如果此节点是 book 节点） |
| attribute | 当前节点的所有属性 | attribute::lang<br>attribute::* | 当前节点的 lang 属性<br>当前节点的所有属性 |
| child | 当前节点的所有子元素 | child::book<br>child::*<br>child::text()<br>child::node()<br>child::price | 当前节点的子元素的 book 节点<br>当前节点的所有子元素<br>当前节点的所有文本子节点<br>当前节点的所有子节点<br>当前节点的所有 price 孙节点 |
| descendant | 当前节点的所有后代元素（子、孙等） | descendant::book | 当前节点的所有 book 后代 |
| descendant-or-self | 当前节点的所有后代元素（子、孙等）以及当前节点本身 | descendant-or-self::book | 当前节点的所有 book 后辈以及当前节点（如果此节点是 book 节点） |
| following | 文档中当前节点的结束标签之后的所有节点 |  |  |
| namespace | 当前节点的所有命名空间节点 |  |  |
| parent | 当前节点的父节点 | parent::book | 当前节点的父元素的 book 节点 |
| preceding | 当前节点的开始标签之前的所有节点 |  |  |
| preceding-sibling | 当前节点之前的所有同级节点 |  |  |
| self | 当前节点 |  |  |

5.运算符

| 运算符 | 说明 | 例子 | 例子的结果说明 |
| :-: | :- | :- | :- |
| \| | 并集 | //book \| //name | 所有book和name节点 |
| + | 加 | 1+2 | 3 |
| - | 减 | 4-3 | 1 |
| * | 乘 | 2*3 | 6 |
| div | 除 | 4 div 2 | 2 |
| = | 等 | price=68.00 | price为68.00，返回真，否则返回假 |
| != | 不等 | price!=68.00 | price为68.00，返回假，否则返回真 |
| < | 小于 | price<68.00 | price小于68.00，返回真，否则返回假 |
| <= | 小于等于 | price<=68.00 | price小于等于68.00，返回真，否则返回假 |
| > | 大于 | price>68.00 | price大于68.00，返回真，否则返回假 |
| >= | 大于等于 | price>=68.00 | price大于等于68.00，返回真，否则返回假 |
| or | 或 | price=68.00 or price=610.00 | price为68.00或610.00，返回真，否则返回假 |
| and | 与 | price>68.00 and price < 610.00 | price为68.00与610.00之间，返回真，否则返回假 |
| mod | 除法的余数 | 5 mod 2 | 1 |
