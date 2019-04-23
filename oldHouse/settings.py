# -*- coding: utf-8 -*-

###################################################################################
# scrapy configurations
BOT_NAME = 'oldHouse'
SPIDER_MODULES = ['oldHouse.spiders']
NEWSPIDER_MODULE = 'oldHouse.spiders'
ROBOTSTXT_OBEY = False
RETRY_TIMES = 8
SCHEDULER_PERSIST = True
SCHEDULER_FLUSH_ON_START = False
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

###################################################################################
# to improve the performance settings
# DOWNLOAD_DELAY = 0.5
CONCURRENT_REQUESTS = 32
DOWNLOAD_TIMEOUT = 25

###################################################################################
# db configurations
MONGO_URL = 'localhost'
MONGO_DATABASE = 'old58Houser'
REDIS_URL = 'redis://root:chen123@192.168.1.11:6379'

###################################################################################
# widget whether test each proxy before crawling.
# if True, it cost much time when starting project, but more fluently when working,
# if False, it cost less time when starting project, but may less efficient when working.
# set True recommended
TEST_PROXY = True
TEST_URL = 'https://bj.58.com/ershoufang/'
PROXY_JSON_FILE = 'oldHouse/service/proxy.json'

###################################################################################
# log configurations
# LOG_FILE = "mySpider.log"
# LOG_LEVEL = "DEBUG"

###################################################################################
# pipeline
ITEM_PIPELINES = {
   'oldHouse.pipelines.MongoPipeline': 300,
}

###################################################################################
# middleware
DOWNLOADER_MIDDLEWARES = {
    'oldHouse.middlewares.OldhouseDownloaderMiddleware': 543,
    'oldHouse.middlewares.MyProxyMiddleWare': 542,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'oldHouse.middlewares.MyUserAgentMiddleWare': 541,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    # 'oldHouse.middlewares.MyRetryMiddleware': 551,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'oldHouse.middlewares.MyRedirectMiddleware': 601,
}




