# 爬取妹子图  www.mmjpg.com
# 流程更简单
# 1. 爬取  www.mmjpg.com/%d 暂定
# 2. 获取 <div class="clearfloat"><script type="text/javascript">var picinfo = [2015,123,37];</script></div>
# 3. 存入数据库 meiziMain（_id, title, time, popular人气, like喜欢,）
#       meiziImg（_id, meiziId, url, status）
# 4. 多线程 多进程下载喽
import codecs
import os
import sqlite3
import threading

import requests
from bs4 import BeautifulSoup

from spider2MeiziForMmjpg import Constants
from spider2MeiziForMmjpg.Utils import store2ErrorFile


class SpiderMeiziForMmjpg():
    def spiderMainByThreads(self):  # 多线程取数据
        # 1 - 151
        threads = []
        maxSize = Constants.MAX_SIZE
        CUR_PAGE = 1000
        NEXT_GOAL_PAGE = Constants.MAX_SIZE
        i = CUR_PAGE

        while (i <= NEXT_GOAL_PAGE):
            if len(threads) == 0:  # 线程处理完，再起线程
                print('[spider]线程处理完，再起线程')
                for v in range(Constants.THREAD_NUM - len(threads)):
                    if i > maxSize:
                        continue
                    url = Constants.HOST + str(i)
                    i = i + 1
                    thread = threading.Thread(target=self.startSpider(url=url))  ##创建线程
                    # thread.setDaemon(True)  ##设置守护线程
                    thread.start()  ##启动线程+
                    threads.append(thread)  ##添加进线程队列
            sqlite3.time.sleep(Constants.SLEEP_TIME)
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
            print('[spider]后台线程走一走(dong:%d, rest:%d)' % (len(threads), Constants.THREAD_NUM - len(threads)))



    def startSpider(self, url):
        '''
         开启爬虫
        :return:
        '''
        if not url:
            return
        print("===========url start============")
        print("url:%s" % url)
        htmlContent = self.getMainPage(url)
        if not htmlContent:
            return
        title, time, popularNum, likeNum, clearfloat = self.parseHtmlForMain(htmlContent)
        if len(title) <= 0:
            store2ErrorFile('【错误】URL解析', url)
            return
        lastId = self.store2DBForMain(title, time, popularNum, likeNum)
        self.store2DBForDetail(lastId, clearfloat)
        print("===========finish============")

    # ==========================================================
    # ============= 爬取网页
    # ==========================================================
    # ========= 获取主界面网页数据
    def getMainPage(self, url):
        '''
        获取网页数据
        :param url: 路径
        :return:  网页数据
        '''
        htmlContent = ''
        try:
            response = requests.get(url, headers=Constants.Default_Header)
            #  www.mmjpg.com 没有正确编码，自行定义编码
            response.encoding = 'utf-8'
            htmlContent = response.text
        except requests.exceptions.ConnectionError:
            store2ErrorFile('【错误】URL访问' , url)
        return htmlContent

    # ========= 解析网页数据
    def parseHtmlForMain(self, htmlContent):  # 解析html
        soup = BeautifulSoup(htmlContent, "html.parser")
        try:
            # 1 ，获取title
            article = soup.find('div', attrs={'class': 'article'})
            title = article.find('h2').string
            infos = article.find('div', attrs={'class': 'info'}).findAll('i')
            # 2 ，获取time
            time = infos[0].string
            if len(time) > 0:
                time = time[4:]
            popularNum = infos[3].string
            if len(popularNum) > 0:
                popularNum = popularNum[3:-1]
            likeNum = infos[4].string
            if len(likeNum) > 0:
                likeNum = likeNum[3:-1]
            # 3. endIndex
            clearfloat = soup.find('div', attrs={'class': 'clearfloat'}).find('script').string
            # if len(clearfloat) > 0:
            #     clearfloat = clearfloat[1:-1]
            clearfloatLeftIndex = clearfloat.index('[')
            clearfloatRightIndex = clearfloat.index(']')
            clearfloat = clearfloat[clearfloatLeftIndex+1 :clearfloatRightIndex ]
        except requests.exceptions.ConnectionError:
            store2ErrorFile('【错误】parseHtmlForMain', htmlContent)
            title = ''
        return title, time, popularNum, likeNum, clearfloat


    # ==========================================================
    # ============= 数据操作
    # ==========================================================
    # ========= 保存到数据库 存入数据库 meiziMain（_id, title, time, popular人气, like喜欢,）
    def store2DBForMain(self, title, time, popularNum, likeNum):  # 保存到sqlite
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists meitiMain (id integer primary key autoincrement, '
                            'title text, time datetime, popularNum int, likeNum int)')
        try:
            self.cursor.execute(
                "insert into meitiMain (title, time, popularNum, likeNum) values (\'%s\',\'%s\', \'%s\',\'%s\');"
                % (title.strip(), time.strip(), popularNum, likeNum))
        except Exception as err:
            store2ErrorFile("插入数据出错",err.__str__())
        finally:
            pass
        # 关闭Cursor:
        self.cursor.close()
        id = self.cursor.lastrowid
        # 提交事务:
        self.conn.commit()

        # 关闭Connection:
        self.conn.close()
        return id

    # ========= 将startIndex直到endIndex的多个index与url拼接，存入数据库
    def store2DBForDetail(self, maiId, picinfo):  # 保存到sqlite
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists meitiDetail (id integer primary key autoincrement, '
                            'mainId int, url text, status int)')

        picinfos = picinfo.split(',')
        if len(picinfos) != 3:
            store2ErrorFile("len(picinfos) != 3", 'maiId:'+ maiId+ '...'+ picinfos)
            return

        try:
            for i in range( 1,  int(picinfos[2])):
                newUrl = Constants.DB_IMAGE + picinfos[0] + '/' + picinfos[1] + '/' + str(i) + '.jpg'
                self.cursor.execute(
                    "insert into meitiDetail (mainId, url, status) values (%d,\'%s\',0);"
                    % (maiId, newUrl.strip()))
        except Exception as err:
            store2ErrorFile("插入数据出错", err.__str__())
        finally:
            pass
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()