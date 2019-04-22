# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import json
from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin
from scrapy import signals
from scrapy import Request
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError


class OldhouseSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MyUserAgentMiddleWare(UserAgentMiddleware):
    # provide user-agent for each request

    @staticmethod
    def get_ua():
        return json.load(open('oldHouse/service/UserAgent.json', 'r', encoding='utf-8'))

    def process_request(self, request, spider):
        # fetch a random user-agent from existing user-agent list
        ua_lis = self.get_ua()
        ua = random.choice(ua_lis)
        request.headers.update({'User-Agent': ua, 'Referer': 'https://bj.58.com/ershoufang/'})
        return None


class MyProxyMiddleWare(object):

    def process_request(self, request, spider):
        proxy_lis = spider._proxy_lis
        request.meta['proxy'] = 'https://' + random.choice(proxy_lis)
        return None


class MyRetryMiddleware(RetryMiddleware):

    EXCEPTIONS_TO_DEL_PROXY = (TimeoutError, ConnectionRefusedError, ConnectError, ConnectionLost, TCPTimedOutError)

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            if isinstance(exception, self.EXCEPTIONS_TO_DEL_PROXY):
                ip_port = request.meta.get("proxy").replace("https://", '')
                try:
                    spider._proxy_lis.remove(ip_port)
                except ValueError:
                    spider.logger.debug(f'proxy{ip_port}: proxy had already been removed')
            return self._retry(request, exception, spider)


class MyRedirectMiddleware(RedirectMiddleware):
    """
    Handle redirection of requests based on response status
    and meta-refresh html tag.
    """

    def process_response(self, request, response, spider):
        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        allowed_status = (301, 302, 303, 307, 308)

        if 'Location' not in response.headers or response.status not in allowed_status:
            return response

        location = safe_url_string(response.headers['location'])

        redirected_url = urljoin(request.url, location)

        if response.status in (301, 307, 308) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        if 'firewall' in redirected_url:
            # to avoid case1、case2：real_url -> firewall
            return Request(request.url, callback=spider.parse_detail, meta=request.meta, dont_filter=True)

        if 'Jump' in redirected_url:
            # to avoid case3：fake_url -> jump_url -> jump_url -> jump_url放弃url
            new_request = request.replace(url=redirected_url, method='GET', body='', meta=request.meta)  # 每次遇到这个跳转url都会加一次retry就是无线retry了

        else:
            new_request = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(new_request, request, spider, response.status)


class OldhouseDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
