引用官网（https://docs.scrapy.org/en/latest/topics/architecture.html）的一张图：

![数据流](./Scrapy_Data_Flow.png)

Scrapy的数据流是由执行引擎控制的，具体流程如上图的红圈数字所示：

1.引擎（Engine）从爬虫程序（Spider）获取要抓取的初始请求（Request）。

2.Engine在调度器（Scheduler）里调度请求，并索要下一个要抓取的Request。

3.Scheduler返回下一个Request给Engine。

4.Engine通过下载器中间件（Downloader Middleware）把Requests发送给下载器（Downloader）。process_request()。

5.一旦下载完成，Downloader生成响应（Response），并通过Downloader Middleware发送回给Engine。process_response()。

6.Engine从Downloader接收到Response，然后通过爬虫中间件（Spider Middleware）把Response发送给Spider处理。process_spider_input()。

7.Spider处理Response，并通过Spider Middleware把抓取的条目（item）和新的要抓取的Request返回给Engine。process_spider_output()。

8.Engine把处理过的条目发送到条目管道（Item Pipeline），然后把处理过的Request发送给Scheduler并索要下一个可能要抓取的Request。

9.重复步骤1，直到Scheduler里不再有要处理的请求为止。

主要部件：
```
Scrapy Engine：爬虫引擎，负责控制数据在系统中所有部件之间的流动，当某些行为发生时，负责触发对应的事件。

Scheduler：调试器，从Engine接收请求，把请求放入队列，当Engine索要请求时，把请求出队给Engine。

Downloader：下载器，负责提取网页，并返回给Engine，然后由Engine发送给Spider。

Spider：爬虫程序，由用户自定义的类，用于解析Response，从中提取需要的条目和额外的请求。

Item Pipeline：条目管道，负责处理由Spider提取的条目。典型的任务包括条目清洗、验证和持久化（如保存到数据库）。

Downloader Middleware：下载器中间件，是位于Engine和Downloader之间的钩子，负责处理从Engine到Downloader的Request，以及从Downloader到Engine的Response。Downloader Middleware用于以下的场景：
1.在发送到Downloader之前要先处理请求，即在爬虫发送请到到网站之前。
2.在发送到Spider之前要改变接收到的Response。
3.要发送一个新的Request给Spider，而不是接收到的Response。
4.发送Response给Spider，但不提取网页。
5.悄悄丢弃一些请求。

Spider Middleware：爬虫中间件，是位于Engine和Spider之间的钩子，可以处理爬虫的输入（Response）和输出（Item，Request）。Spider Middleware用于以下场景：
1.Spider回调输出的后处理，包括改变、增加和移除Request或Item。
2.对start_requests的后处理。
3.处理异常。
4.对一些请求，根据Response的内容调用错误处理，而不是调用回调。
```

事件驱动网络（Event-Driven Networking）

Twisted是一个流行的Python事件驱动网络框架，Scrapy是基于此框架的，使用了非阻塞（异步）代码来实现并发。
