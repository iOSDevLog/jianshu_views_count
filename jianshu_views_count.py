
# -*- coding: utf-8 -*-
# iOSDevLog

import requests
import re
from common import download # 调用前面写的下载函数

# 阅读数
def crawl_views_count(jianshu_url):
    jianshu = download(jianshu_url)
    views_count = re.search(r'views_count":(\d+),', jianshu).group(1)
    print("views_count = " + views_count)

# uuid
def crawl_uuid(jianshu_url):
    jianshu = download(jianshu_url)
    uuid = re.search(r'uuid":"([a-z0-9\-]+?)"}', jianshu).group(1)

    return uuid

if __name__ == '__main__':
    jianshu_url = 'https://www.jianshu.com/p/6f18ca5521a6'
    max_count = 1000 # 刷阅读最大次数

    uuid = crawl_uuid(jianshu_url)
    print("uuid = " + uuid)
    mark_viewed_url = jianshu_url.replace("/p/", "/notes/") + '/mark_viewed.json'
    print("mark_viewed_url = " + mark_viewed_url)
    payload = "uuid=" + uuid
    print("payload = " + payload)

    headers = {
        'Origin': "https://www.jianshu.com",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.1 Safari/605.1.15",
        'Referer': jianshu_url,
        'Content-Type': "text/plain",
        'Cache-Control': "no-cache"
    }

    for _ in range(0, max_count):
        requests.request("POST", mark_viewed_url, data=payload, headers=headers)
        crawl_views_count(jianshu_url) # 检查阅读是否变更
