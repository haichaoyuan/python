# ==================================================
# ============================  下载图片
# ===================================================
import codecs
import os
import sqlite3
import time
import threading
import requests
from bs4 import BeautifulSoup

import spider2Meizitu.Constants as Constants
from spider2Meizitu.SpiderBase import SpiderBasePage


class SpiderDownloadImg(SpiderBasePage):
    # ==================================================
    # ============================  多线程爬取图片 逻辑
    # ===================================================
    def downloadImgsByThreads(self):
        threads = []
        self.data = self.fetDetailDataFromDb()
        # while(i <= 151):
        while len(self.data) > 0:
            if len(threads) == 0:  # 线程处理完，再起线程
                print('[DetailSpider]线程处理完，再起线程')
                for v in range(Constants.THREAD_NUM):
                    url = self.data.pop()
                    if len(url[0]) <= 0:
                        continue
                    thread = threading.Thread(target=self.spiderDownloadImgIml(imgUrl=url[0], title ='abc'))  ##创建线程
                    # thread.setDaemon(True)  ##设置守护线程
                    thread.start()  ##启动线程+
                    threads.append(thread)  ##添加进线程队列
            time.sleep(Constants.SLEEP_TIME)
            for thread in threads:
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            print('[DetailSpider]后台线程走一走(dong:%d, rest:%d)' % (len(threads), Constants.THREAD_NUM - len(threads)))
            if len(self.data) <= 0:
                self.data = self.fetDetailDataFromDb()

    def spiderDownloadImgIml(self, imgUrl, title):  # 下载图片
        start_time = time.clock()
        print("[DownloadImg]downlaod image:%s" % imgUrl)
        try:
            # Default_Header['User-Agent'] = UserAgent_List[random.choice]random.choice(UserAgent_List),
            response = requests.get(imgUrl, headers=Constants.getDefaultHeaderForDownload())
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载' + imgUrl)
            self.changeDetailState(imgUrl, Constants.STATUS_FAILURE)
            return
        htmlContent = response.content
        # 此处存入数据库好了
        names = imgUrl.split('/')
        if (len(names) > 1):
            name = names[len(names) - 1]
        else:
            name = imgUrl
        tmpPath = 'res/' + title + '/' + name
        self.mkdir('res/', title)
        with codecs.open(tmpPath, 'ab') as file:
            file.write(htmlContent)
        end_time = time.clock()
        total_time = float(end_time - start_time)
        self.changeDetailState(imgUrl, Constants.STATUS_SUCCESS)
        print("downlaod image:%s 。finish，总用时 : %f s" % (imgUrl, total_time))
    # ==================================================
    # ============================  多线程爬取详情界面 逻辑end
    # ===================================================

    def mkdir(self, file_path, img_title):  ## 创建文件夹
        file_path = file_path.strip()
        img_title = img_title.strip()
        path = os.path.join(file_path, img_title)
        if not os.path.exists(path):
            print(u'创建文件夹', path)
            os.makedirs(path)
        # os.chdir(path)
        return path
