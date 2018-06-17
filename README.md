# jianshu_views_count
---

刷简书 阅读数 <https://www.jianshu.com/p/6f18ca5521a6>

## 端午节快乐。熬夜看世界杯，先刷到 10k 吧。

使用 `homebrow` 安装 `python` 安装库时不需要再输入 [sudo] 。

```sh
$ brew install python # python3
$ brew install python@2 # python2 我们这里用 python2
$ pip install virtualenv # 虚拟环境
$ pip install virtualenvwrapper
$ cat ~/.bashrc
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Code/python
source /usr/local/bin/virtualenvwrapper.sh
$ cat .bash_profile 
if [ "${BASH-no}" != "no" ]; then
    [ -r ~/.bashrc ] && . ~/.bashrc
fi
$ mkvirtualenv jianshu
(jianshu) $
$ deactivate # 退出虚拟环境
$ workon # 虚拟环境列表
$ workon jianshu # 进入 jianshu 虚拟环境  
```

## 识别网站所用技术

```
$ pip install builtwith
$ python
>>> import builtwith
>>> builtwith.parse('http://iosdevlog.com')
{u'blogs': [u'Jekyll'], u'cms': [u'Jekyll']}
```

<http://iosdevlog.com> 是用 `Jekyll` 搭建的。

## 寻找网站所有者

```
$ pip install python-whois
>>> import whois
>>> print(whois.whois('iosdevlog.com'))
{
  "updated_date": "2017-03-23 22:19:16", 
  "status": "ok https://icann.org/epp#ok", 
  "name": null, 
  "dnssec": "unsigned", 
  "city": "Hangzhou", 
  "expiration_date": "2018-10-01 20:13:15", 
  "zipcode": null, 
  "domain_name": [
    "IOSDEVLOG.COM", 
    "iosdevlog.com"
  ], 
  "country": null, 
  "whois_server": "grs-whois.hichina.com", 
  "state": "Zhejiang", 
  "registrar": "HiChina Zhicheng Technology Ltd.", 
  "referral_url": null, 
  "address": null, 
  "name_servers": [
    "F1G1NS1.DNSPOD.NET", 
    "F1G1NS2.DNSPOD.NET"
  ], 
  "org": null, 
  "creation_date": "2015-10-01 20:13:15", 
  "emails": "DomainAbuse@service.aliyun.com"
}
```

<http://iosdevlog.com> 当时是在万网注册的。

# 简易爬虫 `common.py`

```
# -*- coding: utf-8 -*-

import urllib2
import urlparse

def download(url, user_agent='iosdevlog', proxy=None, num_retries=2):
    """Download function with support for proxies"""
    print 'Downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, user_agent, proxy, num_retries-1)
    return html

if __name__ == '__main__':
    print(download('http://iosdevlog.com'))
```

## 网站地图爬虫 `sitemap.py`

```
# -*- coding: utf-8 -*-

import re
from common import download

def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        html = download(link)
        # scrape html here
        # ...

if __name__ == '__main__':
    crawl_sitemap('http://iosdevlog/sitemap.xml')
```

## 刷简书的浏览量 阅读数 `jianshu_views_count.py`

使用 `postman` 导出为 python - request ，当然也可以导出成其它语言代码。

![postman.png](https://upload-images.jianshu.io/upload_images/910914-134e258e005123cc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
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
```

## GitHub 源码

<https://github.com/iOSDevLog/jianshu_views_count>
