默认的情况下，Scrapy项目的默认结构如下：
```
scrapy.cfg
myproject/
    __init__.py
    items.py
    middlewares.py
    pipelines.py
    settings.py
    spiders/
        __init__.py
        spider1.py
        spider2.py
        ...
```

1.scrapy.cfg

Scrapy的项目配置文件。配置参数是以ini文件的风格来定义，即`key=value`的格式 。这里的scrapy.cfg是位于项目根目录。Scrapy也会查找系统和用户的scrapy.cfg。

系统级的配置文件位于`/etc/scrapy.cfg`或`c:\scrapy\scrapy.cfg`。

用户级的配置文件位于`~/.config/scrapy.cfg ($XDG_CONFIG_HOME)`或`~/.scrapy.cfg ($HOME)`。

项目根目录的scrapy.cfg的参数配置具有最高优先权，其次是用户级的配置，系统级的配置优先级最低。

Scarpy也会通过一些环境变量来配置，目前包括有：`SCRAPY_SETTINGS_MODULE `，`SCRAPY_PROJECT`，`SCRAPY_PYTHON_SHELL`。

2.myproject

项目文件夹，以项目名来命名。

3.items.py

包含数据容器模型的代码。提供了类似于字典的API、声明可用字段的简单语法。这种简单的容器用于保存爬得的数据。

4.middlewares.py

包含下载器中间件和爬虫中间件模型的代码。

下载器中间件是位于Engine和Downloader之间的钩子，负责处理从Engine到Downloader的Request，以及从Downloader到Engine的Response。

爬虫中间件是位于Engine和Spider之间的钩子，可以处理爬虫的输入（Response）和输出（Item，Request）。

5.pipelines.py

管道组件的代码。每个管道组件是一个实现了简单方法的类，接收item并执行一些行为，也决定此item是否继续通过后续的管理组件或者被丢弃也不再处理。

6.settings.py

提供定制组件的方法，可以控制包括核心（core），插件（extension），管道及spider组件。

7.spiders

此文件夹用于存放各个爬虫程序。

8.spider1.py

爬虫程序的代码。
