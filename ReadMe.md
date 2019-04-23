

### 项目介绍
- 利用scrapy_redis分布式爬虫框架，爬取58同城北京站房产相关数据，在master主机存储requests队列和指纹，在各slave主机存储具体爬取数据

到mongodb上

### 开发环境
- python 3.6.4

### 配置开发环境
- python库：
    命令行下运行 pip install -r requirements.txt
- exe程序：

    版本管理软件: git

    数据库软件：mongodb, redis

    数据库可视化软件： robo3t(for mongodb)， RedisDesktopManager(for redis)

- settings配置：

    配置redis服务器地址>>>REDIS_URL = 'redis://name:password@ip:port'
- PS:

    确保scrapy, pip已在系统环境变量目录下

### 部署
- master主机启动redis服务和mongodb服务

- slave主机启动mongodb服务


### 启动项目
- cd oldHouse
- shell:python3 oldHouse/service/protester.py,生成代理文件
- shell:scrapy crawl old58House，开始爬虫程序


### 数据库查看
- 爬取前

    远程redis

![jupyter](./img/remote_redis_start.png)

    本地mongodb

![jupyter](./img/local_mongo_start.png)

    远程mongodb

![jupyter](./img/remote_mongo_start.png)

- 爬取后

    远程redis

![jupyter](./img/remote_redis_end.png)

    本地mongodb

![jupyter](./img/local_mongo_end.png)

    远程mongodb

![jupyter](./img/remote_mongo_end.png)


    

