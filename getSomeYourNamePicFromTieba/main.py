# 目的：
# 从百度贴吧下载几张君名的图片，https://tieba.baidu.com/p/4780093697
# 技术栈：
# 1.获取网页内容； 2. 正则获取查找所有图片路径，3.多线程下载图片，导出的本地图片文件夹

# encoding:utf-8
# !/usr/bin/env/python

import requests
import time
from pymongo import MongoClient  # mongo处理
from datetime import timedelta
import re
from bs4 import BeautifulSoup
from tornado import httpclient, gen, ioloop, queues

# 作者写自己
__author__ = 'hc'

concurrency = 10

# headers = {
#  # GET http://www.jobbole.com/ HTTP/1.1
#  "Host": "www.jobbole.com",
#  "Proxy-Connection": "keep-alive",
#  "Pragma": "no-cache",
#  "Cache-Control": "no-cache",
#  "Upgrade-Insecure-Requests": '1',
#  "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
#  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#  "Accept-Encoding": "gzip, deflate, sdch",
#  "Accept-Language": "zh-CN,zh;q=0.8",
# }

"""
获取知道页面中所有文章的URL
:param page_url:
:return:
"""


def get_posts_url_from_page(page_url):
    try:
        # response = yield httpclient.AsyncHTTPClient().fetch(page_url, headers = headers)
        response = yield httpclient.AsyncHTTPClient().fetch(page_url)
        soup = BeautifulSoup(response.body, 'html.parser')
        posts_tag = soup.find_all('div', class_='post floated-thumb')
        urls = []
        for index, archive in enumerate(posts_tag):
            print(index, archive)
    finally:
        pass


response = requests.get("https://tieba.baidu.com/p/4780093697")
print(response.content.decode('utf-8'))
