1.简单爬取一个页面
```
import urllib
f = urllib.urlopen('http://www.qq.com')  # HTTP协议，也可以是FTP，FILE，HTTPS等
print f.read()  # 读取整个页面
```

2.通过构造Request请求对象
```
import urllib2
req = urllib2.Request('http://www.qq.com')  # 构造一个Request请求对象
f = urllib2.urlopen(req)  # 传入一个Request请求对象
print f.read().decode('gbk')  # 读取整个页面，read()返回的是字节对象，转为gbk编码显示中文
```

3.POST和GET数据传送
```
import urllib

# POST
data = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})  # 数据字典
print data  # eggs=2&bacon=0&spam=1
f = urllib.urlopen('http://www.musi-cal.com/cgi-bin/query', data)  # POST，如果data里有中文，要data.encode('utf-8')
print f.geturl()  # 获取url，http://www.musi-cal.com/cgi-bin/query
print f.read(100)  # 返回的是字节对象，读取前100个字节

# GET
f = urllib.urlopen('http://www.musi-cal.com/cgi-bin/query?%s' % data)  # GET，如果data里有中文，要data.encode('utf-8')
print f.geturl()  # 获取url，http://www.musi-cal.com/cgi-bin/query?eggs=2&bacon=0&spam=1
print f.read(100)  # 返回的是字节对象，读取前100个字节
```

4.设置Headers
```
import urllib2
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}  # 设置User-Agent
req = urllib2.Request(url='https://www.qq.com', headers=headers)  # 构造一个Request请求对象，并传入Headers
f = urllib2.urlopen(req)  # 传入一个Request请求对象
print f.read().decode('gbk')  # 读取整个页面，read()返回的是字节对象，转为gbk编码显示中文

req = urllib2.Request(url='https://www.qq.com')  # 构造一个Request请求对象
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0')  # 添加User-Agent到Headers
f = urllib2.urlopen(req)  # 传入一个Request请求对象
print f.read().decode('gbk')  # 读取整个页面，read()返回的是字节对象，转为gbk编码显示中文
```
Header的一些属性说明：

User-Agent：通过该值来判断是否为浏览器发出的请求。

Content-Type：使用REST接口时，服务器会检查此值来确定Body中的内容要怎样解析。

application/xml：在XML RPC调用时使用。

application/json：在JSON RPC调用时使用。

application/x-www-form-urlencoded：浏览器提交Web表单时使用。

5.代理（Proxy）设置
```
import urllib2
proxy_handler = urllib2.ProxyHandler({'http': 'http://www.example.com:3128/'})  # 代理处理器
proxy_auth_handler = urllib2.ProxyBasicAuthHandler()  # 代理验证处理器
proxy_auth_handler.add_password('realm', 'host', 'username', 'password')  # 添加用户名和密码
opener = urllib2.build_opener(proxy_handler, proxy_auth_handler)  # 建立一个opener，传入了代理处理器和代理验证处理器
f = opener.open('http://www.example.com/login.html')  # 用建立的opener直接打开网页，不需要调用urllib2.install_opener()
# 或者这样使用
# urllib2.install_opener(opener)  # 安装opener
# f = urllib2.urlopen('http://www.example.com/login.html')  # 调用urlopen()
print f.read()  # 获得页面内容
```

6.超时（timeout）设置
```
# 参考5中的代码
f = opener.open('http://www.example.com/login.html', timeout=5)  # 超时5秒则抛出URLError异常
```

7.异常处理（URLError，HTTPError）

URLError是IOError的子类，HTTPError是URLError的子类。URLError产生的原因有：网络无连接，连接不到服务器，服务器不存在，请求超时等。URLError异常有`reason`属性，说明了异常的原因。
```
import urllib2
req = urllib2.Request(url='http://www.baidu123456123456123456.com')  # 一个不存在的网页
try:
    f = urllib2.urlopen(req)  # 试图打开不存在的网页
    print f.read()
except urllib2.URLError as e:  # 抛出异常
    print e.reason  # [Errno 11001] getaddrinfo failed
else:
    print u'成功'
```

```
import urllib2
req = urllib2.Request(url='https://www.douyu.com/Json.html')  # 一个不存在的网页
try:
    f = urllib2.urlopen(req)  # 试图打开不存在的网页
    print f.read()
except urllib2.HTTPError as e:
    print e.reason  # Not Found
    print e.code  # 404
except urllib2.URLError as e:  # 抛出异常
    print e.reason
else:
    print u'成功'
```
HTTPError异常除了继承了`reason`属性，还有`code`属性，是异常对应的状态码。HTTP状态码有：
```
100：客户端继续发送请求的剩余部分，如请求已完成，忽略。
101：发送完此响应的最后空行，服务器切换到Upgrade消息头中定义的协议。
102：处理被继续执行。
200：请求成功。
201：请求完成。
202：请求被接受，处理尚未完成。
204：服务器已实现请求，但没有返回信息。
300：存在多个可用的被请求资源。
301：请求到的资源会分配一个永久的URL，将来通过此URL来访问。
302：请求到的资源在一个不同的URL临时保存。
304：请求的资源未更新。
400：非法请求。
401：未授权。
403：禁止。
404：找不到。
500：服务器内部错误。
501：服务器无法识别。
502：错误网关。
503：服务出错。
```

8.Cookie的使用（cookielib.CookieJar，cookielib.FileCookieJar，cookielib.MozillaCookieJar，cookielib.LWPCookieJar）

cookielib.MozillaCookieJar和cookielib.LWPCookieJar是cookielib.FileCookieJar的子类，cookielib.FileCookieJar是cookielib.CookieJar的子类。
```
# cookie保存在变量中
import urllib2
import cookielib

cj = cookielib.CookieJar()  # CookieJar对象，cookie会保存在这个变量中
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))  # 传入cookie处理器来构建opener
f = opener.open('http://www.baidu.com')  # 打开页面
for item in cj:  # 历遍cookie中的键值对
    print u'键：' + item.name
    print u'值：' + item.value
```

```
# cookie保存到文件
import urllib2
import cookielib

filename = 'cookie.txt'
cj = cookielib.MozillaCookieJar(filename)  # MozillaCookieJar对象，cookie会保存在文件中
processor = urllib2.HTTPCookieProcessor(cj)  # cookie处理器
opener = urllib2.build_opener(processor)   # 传入cookie处理器来构建opener
f = opener.open('http://www.baidu.com')  # 打开页面
cj.save(ignore_discard=True, ignore_expires=True)  # 保存，cookie被丢弃也保存，cookie到期也保存
```

```
# 读取cookie
import urllib2
import cookielib

cj = cookielib.MozillaCookieJar()  # MozillaCookieJar对象
cj.load('cookie.txt', ignore_discard=True, ignore_expires=True)  # 读取cookie文件
processor = urllib2.HTTPCookieProcessor(cj)  # cookie处理器
req = urllib2.Request('http://www.baidu.com')  # 建立请求
opener = urllib2.build_opener(processor)   # 传入cookie处理器来构建opener
f = opener.open(req)  # 打开页面
print f.read()  # 读取页面内容
```

```
# 模拟登陆的过程
import urllib
import urllib2
import cookielib

filename = 'cookie.txt'
cj = cookielib.MozillaCookieJar(filename)  # MozillaCookieJar对象，cookie会保存在文件中
processor = urllib2.HTTPCookieProcessor(cj)  # cookie处理器
opener = urllib2.build_opener(processor)   # 传入cookie处理器来构建opener
data = {}  # 数据字典
data['username'] = 'xxxxxxx'  # 用记名
data['password'] = '1111111'  # 密码
post = urllib.urlencode(data)  # 生成用于传递的数据字符串
url = 'http://www.xxxx.com/login'  # 登陆页面
req = urllib2.Request(url=url, data=post)  # 建立请求，传入登陆需要的数据，如用户名密码之类
f = opener.open(req)  # 打开页面
cj.save(ignore_discard=True, ignore_expires=True)  # 保存，cookie被丢弃也保存，cookie到期也保存
other_url = 'http://www.xxxx.com/other'  # 需要登陆才能访问的页面
f = opener.open(other_url)  # 访问需要登陆才能访问的页面
print f.read()  # 读取页面内容
```
