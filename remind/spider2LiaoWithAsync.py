# ================================================================================
# ===================================================== requests 进阶喽，增加async
# ================================================================================
# encoding:utf-8
# !/usr/bin/env/ python
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

headers = {
    # GET http://www.jobbole.com/ HTTP/1.1
    "Host": "www.jobbole.com",
    "Proxy-Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
}


@gen.coroutine()
def get_posts_url_from_page(page_url):
    """
    获取知道页面中所有文章的URL
    :param page_url:
    :return:
    """
    try:
        response = yield httpclient.AsyncHTTPClient().fetch(page_url, headers=headers)
        soup = BeautifulSoup(response.body, 'html.parser')
        posts_tag = soup.find_all('div', class_='post floated-thumb')
        urls = []
        for index, archive in enumerate(posts_tag):
            print(index, archive)

    finally:
        pass


response = requests.get("http://python.jobbole.com/87305/")
print(response.content.decode('utf-8'))
