# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
###################################################################################
# scrapy configurations
BOT_NAME = 'oldHouse'
SPIDER_MODULES = ['oldHouse.spiders']
NEWSPIDER_MODULE = 'oldHouse.spiders'
# SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# SCHEDULER_PERSIST = True
# SCHEDULER_FLUSH_ON_START = False
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY=1
# CONCURRENT_REQUESTS = 32
# CONCURRENT_REQUESTS_PER_IP = 2
RETRY_TIMES = 5
ITEM_PIPELINES = {
   'oldHouse.pipelines.MongoPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'oldHouse.middlewares.OldhouseDownloaderMiddleware': 543,
    'oldHouse.middlewares.MyProxyMiddleWare': 542,
    'oldHouse.middlewares.MyUserAgentMiddleWare': 541,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'oldHouse.middlewares.MyRedirectMiddleware': 601,
    'oldHouse.middlewares.MyRetryMiddleware': 551,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
}

# LOG_FILE = "mySpider.log"
# LOG_LEVEL = "DEBUG"


###################################################################################
# db configurations
# REDIS_URL = 'redis://name:password@ip:port'
MONGO_URI = 'localhost'
MONGO_DATABASE = 'old58House'

###################################################################################
# widget whether test each proxy before crawling.
# if True, it cost much time when starting project, but more fluently when working,
# if False, it cost less time when starting project, but may less efficient when working.
# set True recommended
TEST_PROXY = True



