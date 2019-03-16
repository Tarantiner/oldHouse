# -*- coding: utf-8 -*-

###################################################################################
# scrapy configurations
BOT_NAME = 'oldHouse'
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
SCHEDULER_PERSIST = True
SCHEDULER_FLUSH_ON_START = False
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_IP = 3
REDIRECT_ENABLED = False
ITEM_PIPELINES = {
   'oldHouse.pipelines.MongoPipeline': 300,
}
DOWNLOADER_MIDDLEWARES = {
    'oldHouse.middlewares.OldhouseDownloaderMiddleware': 543,
    'oldHouse.middlewares.MyProxyMiddleWare': 542,
    'oldHouse.middlewares.MyUserAgentMiddleWare': 541,
}


###################################################################################
# db configurations
REDIS_URL = 'redis://root:chen123@192.168.199.128:6379'
SPIDER_MODULES = ['oldHouse.spiders']
NEWSPIDER_MODULE = 'oldHouse.spiders'
MONGO_URI = 'localhost'
MONGO_DATABASE = 'old58House'



