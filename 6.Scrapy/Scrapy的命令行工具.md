1.Scrapy项目的默认结构

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

`scrapy.cfg`所在有目录为项目的根目录。此文件包含了配置文件的说明。

```
[settings]
default = myproject1.settings
project1 = myproject1.settings
project2 = myproject2.settings
```

默认情况下会使用`default`这个配置。可以使用`SCRAPY_PROJECT`环境变量来指定不同的项目。

```
export SCRAPY_PROJECT=project2
scrapy settings --get BOT_NAME
```

2.scrapy工具的使用

直接运行获得帮助说明：

```
scrapy
```

创建项目：

```
scrapy startproject myproject [project_dir]
```

控制项目：

```
scrapy genspider mydomain mydomain.com  # 创建一个新的Spider
```

可用的工具命令：

```
scrapy -h  # 查看所有可用命令
scrapy <command> -h  # 查看对应命令的帮助

全局命令：
startproject：scrapy startproject <project_name> [project_dir]  # 创建项目
genspider：scrapy genspider [-t template] <name> <domain>  # 创建新的Spider
settings：scrapy settings [options]  # 获取配置
runspider：scrapy runspider <spider_file.py>  # 运行Python文件里的Spider，不需要创建项目
shell：scrapy shell [url]  # 启动Scrapy交互终端，可用于调试
fetch：scrapy fetch <url>  # 使用Scrapy下载器下载给定的URL，并将获取的内容送到标准输出
view：scrapy view <url>  # 浏览器中打开URL
version：scrapy version [-v]  # 打印版本

项目命令：
crawl：scrapy crawl <spider>  # 使用spider进行爬取
check：scrapy check [-l] <spider>  # 运行contract检查
list：scrapy list  # 列出当前项目可用的所有spider
edit：scrapy edit <spider>  # 使用EDITOR环境变量中设定的编辑器编辑spider
parse：scrapy parse <url> [options]  # 获取给定的URL并使用spider分析处理
bench：scrapy bench  # 运行benchmark测试
```
