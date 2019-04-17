# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import json
from scrapy import signals
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy import Request
from scrapy.downloadermiddlewares.redirect import BaseRedirectMiddleware
from six.moves.urllib.parse import urljoin
from w3lib.url import safe_url_string
from oldHouse.spiders.old58House import Old58houseSpider


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

    @staticmethod
    def get_proxy():
        return json.load(open('oldHouse/service/proxy.json', 'r', encoding='utf-8'))

    def process_request(self, request, spider):
        proxy_lis = self.get_proxy()
        request.meta['proxy'] = random.choice(proxy_lis)
        return None


class MyRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        if all([(response.status == 302), ('firewall' not in request.url), ('service' not in request.url)]):
            print('*' * 30, response.status, response.url, request.url)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider)
            # return Request(request.url, callback=Old58houseSpider.parse_detail, meta={'dont_redirect': True})
        return response


class MyRedirectMiddleware(BaseRedirectMiddleware):
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
        print('here is', location, response.status, response.url, request.url)

        redirected_url = urljoin(request.url, location)

        if response.status in (301, 307, 308) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)
        if 'Jump' in redirected_url:
            # 为防3类情况：fake_url -> jump_url -> jump_url -> jump_url放弃url
            # spider.logger.debug('#'*50 + '33333333333333')
            # print(redirected_url + '###\n' + request.url + '###\n' + response.status +response.url)
            new_request = request.replace(url=redirected_url, method='GET', body='', meta={'max_retry_times': 5})  # 每次遇到这个跳转url都会加一次retry就是无线retry了
        if 'Jump' not in redirected_url and 'firewall' not in redirected_url:
            # 为防4类情况：fake_url -> jump_url -> real_url - > firewal，当拿到真的url，不允许重定向到firewall
            # spider.logger.debug('#' * 50 + '44444444444444')
            # print(redirected_url + '###\n' + request.url + '###\n' + response.status + response.url)
            new_request = request.replace(url=redirected_url, method='GET', body='', meta={'dont_redirect': True, 'max_retry_times': 7})
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
