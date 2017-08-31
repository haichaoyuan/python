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

from spider2Meizitu.SpiderMainPage import SpiderMainPage
from spider2Meizitu.SpiderDetailPage import SpiderDetailPage
from spider2Meizitu.SpiderDownloadImg import SpiderDownloadImg


class SpiderMeizitu:
    def __init__(self) -> None:
        super().__init__()
        self.spiderMainPage = SpiderMainPage()
        self.spiderDetailPage = SpiderDetailPage()
        self.spiderDownloadImg = SpiderDownloadImg()

    # ==================================================
    # ============================ 多进程，多线程，一个进程启多线程爬主界面
    # ============================ 一个进程启多线程爬主界面
    # ============================ 另个进程启多线程爬详情界面
    # ============================ 另个进程启多线程下载图片
    # ===================================================
    def mutiProcess2Spider(self):  # 入口2 多进程下载
        process = []
        num_cpus = multiprocessing.cpu_count()
        print('cpu_num:%d' % num_cpus)
        # num_cpus = 1
        for i in range(3):
            if i == 0:
                continue
                p = multiprocessing.Process(target=self.spiderMainPage.spiderMainByThreads)
            elif i == 1:
                p = multiprocessing.Process(target=self.spiderDetailPage.spiderDetailByThreads())
            else:
                p = multiprocessing.Process(target=self.spiderDownloadImg.downloadImgsByThreads())
            p.start()  # 启动进程
            process.append(p)
        for p in process:
            p.join()  ##等待进程队列里面的进程结束
# the enter load
if __name__ == '__main__':
    page = 1
    spiderMeizitu = SpiderMeizitu()
    spiderMeizitu.mutiProcess2Spider()

    # spiderMeizitu.downloadImgsIml()
    # html2Txt(page, url)
