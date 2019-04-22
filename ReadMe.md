

### 项目介绍
- 利用scrapy爬虫框架，爬取58同城北京站房产相关数据，将数据存储到本机mongodb上

### 开发环境
- python 3.6.4

### 配置开发环境
- python库：
    命令行下运行 pip install -r requirements.txt
- 应用程序：

    数据库软件：mongodb

    数据库可视化软件： robo3t(for mongodb)

- PS:

    确保scrapy, pip已在系统环境变量目录下

### 部署
- 本地主机启动mongodb服务

### 启动项目
- ！！！本项目需要手动生成代理列表，务必在启动前运行oldHouse/service/protester/protester.py文件
- 在项目目录下，在命令行输入：scrapy crawl old58House，程序启动

