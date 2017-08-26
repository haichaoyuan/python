# ==================================================
# ============================ 爬取详情界面，就是二级页面
# ===================================================
import sqlite3
import threading

import requests
import time
from bs4 import BeautifulSoup
from spider2Meizitu.SpiderBase import SpiderBasePage

import spider2Meizitu.Constants as Constants


class SpiderDetailPage(SpiderBasePage):
    def __init__(self) -> None:
        super().__init__()

    # ==================================================
    # ============================  多线程爬取详情界面 逻辑
    # ===================================================
    def spiderDetailByThreads(self):  # 多线程取数据
        threads = []
        self.data = self.fetMainDataFromDb()
        # while(i <= 151):
        while len(self.data) > 0:
            if len(threads) == 0:  # 线程处理完，再起线程
                print('[DetailSpider]线程处理完，再起线程')
                for v in range(Constants.THREAD_NUM):
                    url = self.data.pop()
                    if len(url[0]) <= 0:
                        continue
                    thread = threading.Thread(target=self.spiderDetailPageIml(url=url[0]))  ##创建线程
                    # thread.setDaemon(True)  ##设置守护线程
                    thread.start()  ##启动线程+
                    threads.append(thread)  ##添加进线程队列
            time.sleep(Constants.SLEEP_TIME)
            for thread in threads:
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            print('[DetailSpider]后台线程走一走(dong:%d, rest:%d)' % (len(threads), Constants.THREAD_NUM - len(threads)))
            if len(self.data) <= 0:
                self.data = self.fetMainDataFromDb()

    def spiderDetailPageIml(self, url):  # 爬主界面流程
        if not url:
            return
        print("======================================")
        print("===========step one getPage============")
        print("======================================")
        print("url:%s" % url)
        htmlContent = self.getMainPage(url)
        if not htmlContent:
            return
        print("===========step two BeautifulSoup Page============")
        liList = self.parseHtmlForDetail(htmlContent)

        if len(liList) <= 0:
            return
        result = self.store2DBForDetail(liList, url)
        if result:
            self.changeMainState(url, Constants.STATUS_SUCCESS)
        else:
            self.changeMainState(url, Constants.STATUS_FAILURE)
        print("===========finish============")

    # ==================================================
    # ============================  多线程爬取详情界面 逻辑 end
    # ===================================================

    def fetMainDataFromDb(self):  # 数据库查询db
        conn = sqlite3.connect(Constants.DB_PATH)
        # 创建一个Cursor:
        cursor = conn.cursor()
        cursor.execute(
            'select url from meitiMain where status == %d limit %d ' % (Constants.STATUS_INITIAL, Constants.PAGE_SIZE))
        # 获得查询结果集:
        values = cursor.fetchall()
        print("===========step zero fetch from db============")
        print(values)
        # 关闭Cursor:
        cursor.close()
        # 关闭Connection:
        conn.close()
        return values

    # ========= 获取主界面网页数据

    # ========= 解析网页数据
    def parseHtmlForDetail(self, htmlContent):  # 解析html
        soup = BeautifulSoup(htmlContent, "html.parser")
        # soupList = soup.find('div', attrs={'class': 'maincontent'})
        soupList = soup.find('div', attrs={'class': 'main-image'})
        imgList = soupList.find_all('img')
        return imgList

    # ========= 保存到数据库
    def store2DBForDetail(self, imgList, baseUrl):  # 保存到sqlite
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists meitiDetail (id integer primary key autoincrement, '
                            'parentUrl text, url text, time datetime, num text, status int)')
        title = ''
        result = True
        try:
            for soupItem in imgList:
                # 先拿标题
                # <img src="http://img.mmjpg.com/small/2017/1086.jpg" width="220" height="330" alt="磨人的小妖精温心怡美臀让人垂涎欲滴" />
                # spans = soupItem.findAll('span')
                # url = spans[0].find('a')["href"]
                # title = spans[0].find('a').string
                # time = spans[1].string
                # numStr = spans[2].string
                time = ''
                numStr = ''
                url = soupItem['src']
                title = soupItem['alt']
                print(url + ',' + title + ',' + time + ',' + numStr)
                self.cursor.execute(
                    "insert into meitiDetail (parentUrl, url, time, num, status) values (\'%s\',\'%s\', \'%s\',\'%s\', 0);"
                    % (baseUrl.strip(), url.strip(), time.strip(), numStr.strip()))
        except Exception as err:
            print(err)
            result = False
        finally:
            # 关闭Cursor:
            self.cursor.close()
            # 提交事务:
            self.conn.commit()
            # 关闭Connection:
            self.conn.close()
            return result