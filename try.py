import json
import requests
import time
from concurrent.futures.thread import ThreadPoolExecutor


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}

def tes_proxy(p):
    test_url = 'https://bj.58.com/'
    headers = HEADERS
    proxy = {'https': 'https://%s' % p}
    try:
        res = requests.get(url=test_url, headers=headers, proxies=proxy, timeout=3)
        print('valid', proxy, res.status_code)
        return p
    except:
        # print('invalid', proxy)
        return False

f = open('1.txt', 'r', encoding='utf-8')
lis = []
for line in f.readlines():
    new = line.strip('\n')
    lis.append(new)
f.close()

p_lis = []


def save_data(proxy):
    p = proxy.result()
    if p:
        print(p)
        p_lis.append(p)


# proxies = json.load(open('proxy.json', 'r', encoding='utf-8'))
t = ThreadPoolExecutor(10)
for i in lis:
    t.submit(tes_proxy, i).add_done_callback(save_data)
t.shutdown()
json.dump(p_lis, open('proxy.json', 'w', encoding='utf-8'))


