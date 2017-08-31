# 爬取这个 www.mmjpg.com 这个妹子网站
# 1. 爬取所有妹子 格式是 http://www.mmjpg.com/mm/%d
# 2. 爬取单个妹子所有图片路径
# 3. 下载图片

# 啊哈哈 妹子图我来爬你了
# encoding=utf8
import codecs
import multiprocessing
import os
import sqlite3
import threading
import time

import requests
from bs4 import BeautifulSoup

from spider2MeiziForMmjpg.SpiderDownloadImg import SpiderDownloadImg
from spider2MeiziForMmjpg.SpiderMeiziForMmjpg import SpiderMeiziForMmjpg


# the enter load
if __name__ == '__main__':
    # spiderMeizitu = SpiderMeiziForMmjpg()
    # spiderMeizitu.spiderMainByThreads()
    spiderMeizitu = SpiderDownloadImg()
    spiderMeizitu.downloadImgsByThreads()
    # error 156
    # spiderMeizitu.store2ErrorFile('title', 'content')
