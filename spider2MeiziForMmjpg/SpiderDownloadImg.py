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

from spider2MeiziForMmjpg import Constants
from spider2MeiziForMmjpg.Utils import store2ErrorFile


class SpiderDownloadImg():
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
                    if len(self.data) <= 0:
                        continue
                    url = self.data.pop()
                    thread = threading.Thread(target=self.spiderDownloadImgIml(id = url[0], imgUrl=url[1], title =url[2]))  ##创建线程
                    # thread.setDaemon(True)  ##设置守护线程
                    thread.start()  ##启动线程+
                    threads.append(thread)  ##添加进线程队列
            time.sleep(Constants.SLEEP_TIME)
            for thread in threads:#10/10
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            for thread in threads:#5/10
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            for thread in threads:#3/10
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            for thread in threads:#1/10
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            print('[DetailSpider]后台线程走一走(dong:%d, rest:%d)' % (len(threads), Constants.THREAD_NUM - len(threads)))
            if len(self.data) <= 0:
                self.data = self.fetDetailDataFromDb()

    def spiderDownloadImgIml(self, id, imgUrl, title):  # 下载图片
        start_time = time.clock()
        print("[DownloadImg]downlaod image:%s" % imgUrl)
        try:
            # Default_Header['User-Agent'] = UserAgent_List[random.choice]random.choice(UserAgent_List),
            response = requests.get(imgUrl, headers=Constants.getDefaultHeaderForDownload(imgUrl))
        except requests.exceptions.ConnectionError:
            store2ErrorFile('【错误】当前图片无法下载' , imgUrl)
            self.changeDetailState(id, Constants.STATUS_FAILURE)
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
        self.changeDetailState(id, Constants.STATUS_SUCCESS)
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

    # ==========================================================
    # ============= db
    # ==========================================================
    def fetDetailDataFromDb(self):  # 数据库查询db
        conn = sqlite3.connect(Constants.DB_PATH)
        # 创建一个Cursor:
        cursor = conn.cursor()
        cursor.execute(
            'select meitiDetail.id, meitiDetail.url, meitiMain.title from meitiDetail, meitiMain where meitiMain.id = meitiDetail.mainId and meitiDetail.status == %d limit %d ' % (Constants.STATUS_INITIAL, Constants.PAGE_SIZE))
        # 获得查询结果集:
        values = cursor.fetchall()
        print("===========step zero fetch from db size: %d============" % len(values))
        print(values)
        # 关闭Cursor:
        cursor.close()
        # 关闭Connection:
        conn.close()
        return values

    # ==================================================
    # ============================ 详情库
    # ===================================================
    # ========= 更新详情库数据状态
    def changeDetailState(self, id, status):
        self.conn = sqlite3.connect(Constants.DB_PATH)
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        self.cursor.execute('update meitiDetail set status = %s where id = \'%s\'' % (status, id))
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()
