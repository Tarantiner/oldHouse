# -*- coding:utf-8 -*-
# Author: Tarantiner
# @Time :2019/3/16 14:31

import json
import requests
from concurrent.futures.thread import ThreadPoolExecutor


class ProxyHandler:
    """
    I wont't let you take the risk having your ip banned by web server, so I write the class to get valid proxies.
    before run it, you should prepare some proxies formatting like this: '112.175.32.88:8080', and put them in directory
    /oldHouse/oldHouse/service/tmp.txt, we'll use them in our functions.
    how to get proxies, I'll recommend a website 'https://ip.ihuan.me/ti.html', it save me much time crawling proxies,
    most important, it's free!
    """
    count = 0
    p_lis = []
    proxy_lis = []
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    }

    def get_proxy_lis(self):
        """
        tmp.txt, this file is used to store our proxies as said, and now I'll transform this strings to lis form.
        :return: proxies by lis form
        """
        with open('tmp.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                proxy = line.strip('\n')
                self.proxy_lis.append(proxy)

    def tes_proxy(self, proxy):
        """ get useful proxy
        in order to make the project more effective, I decide to test each proxy before it really begin to crawl urls.
        :param proxy: proxy to be tested
        :return: proxy if valid else None
        """
        test_url = 'https://bj.58.com/'
        headers = self.HEADERS
        proxies = {'https': 'https://%s' % proxy}
        try:
            res = requests.get(url=test_url, headers=headers, proxies=proxies, timeout=3)
            self.count += 1
            return proxy
        except:
            # print('invalid', proxy)
            return False

    def save_valid_proxy_lis(self, proxy):
        """
        after testing, we transform this strings to lis form again.
        :param proxy: valid proxy
        :return: valid proxies by lis form
        """
        p = proxy.result()
        if p:
            self.p_lis.append(p)

    def save_proxy_to_json(self):
        # we make proxies item to json form in order to deserialize them when needed
        json.dump(self.p_lis, open('proxy.json', 'w', encoding='utf-8'))

    def multi_test(self):
        # using thread pool to improve testing speed
        t = ThreadPoolExecutor(10)
        for proxy in self.proxy_lis:
            t.submit(self.tes_proxy, proxy).add_done_callback(self.save_valid_proxy_lis)
        t.shutdown()
        print(f'fetch{self.count}valid proxies.')

    def run(self):
        """
        * get proxy
        * test each of them
        * save them by json form
        """
        self.get_proxy_lis()
        self.multi_test()
        self.save_proxy_to_json()


if __name__ == '__main__':
    p = ProxyHandler()
    p.run()





