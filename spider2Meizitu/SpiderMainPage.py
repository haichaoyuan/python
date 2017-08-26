# ==================================================
# ============================ 爬取主界面
# ===================================================
import sqlite3
import threading
import time

from bs4 import BeautifulSoup

import spider2Meizitu.Constants as Constants
from spider2Meizitu.SpiderBase import SpiderBasePage

CUR_PAGE = 0  # 当前页
NEXT_GOAL_PAGE = 1  # 下个目标页

class SpiderMainPage(SpiderBasePage):
    def __init__(self) -> None:
        super().__init__()

    # ==================================================
    # ============================  多线程爬取主界面 逻辑
    # ===================================================
    def spiderMainByThreads(self):  # 多线程取数据
        # 1 - 151
        threads = []
        maxSize = Constants.MAX_SIZE
        i = CUR_PAGE
        # while(i <= 151):
        while (i <= NEXT_GOAL_PAGE):
            if len(threads) == 0:  # 线程处理完，再起线程
                print('[spider]线程处理完，再起线程')
                for v in range(Constants.THREAD_NUM):
                    url = 'http://www.mzitu.com/page/%d/' % i
                    i = i + 1
                    if i > maxSize:
                        continue
                    thread = threading.Thread(target=self.spiderMainPageIml(url=url))  ##创建线程
                    # thread.setDaemon(True)  ##设置守护线程
                    thread.start()  ##启动线程+
                    threads.append(thread)  ##添加进线程队列
            time.sleep(Constants.SLEEP_TIME)
            for thread in threads:
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            print('[spider]后台线程走一走(dong:%d, rest:%d)' % (len(threads), Constants.THREAD_NUM - len(threads)))

    def spiderMainPageIml(self, url):  # 爬主界面流程
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
        liList = self.parseHtmlForMain(htmlContent)

        if len(liList) <= 0:
            return
        self.store2DBForMain(liList, url)
        print("===========finish============")

    # ==================================================
    # ============================  多线程爬取主界面 逻辑 end
    # ===================================================


    # ========= 解析网页数据
    def parseHtmlForMain(self, htmlContent):  # 解析html
        soup = BeautifulSoup(htmlContent, "html.parser")
        soupList = soup.find('ul', attrs={'id': 'pins'})
        liList = soupList.find_all('li')
        return liList

    # ========= 保存到数据库
    def store2DBForMain(self, imgList, baseUrl):  # 保存到sqlite
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists meitiMain (id integer primary key autoincrement, '
                            'title text, url text, time datetime, num text, status int)')
        title = ''
        for soupItem in imgList:
            # 先拿标题
            try:
                # <img src="http://img.mmjpg.com/small/2017/1086.jpg" width="220" height="330" alt="磨人的小妖精温心怡美臀让人垂涎欲滴" />
                spans = soupItem.findAll('span')
                url = spans[0].find('a')["href"]
                title = spans[0].find('a').string
                time = spans[1].string
                numStr = spans[2].string
                print(url + ',' + title + ',' + time + ',' + numStr)
                self.cursor.execute(
                    "insert into meitiMain (title, url, time, num, status) values (\'%s\',\'%s\', \'%s\',\'%s\', 0);"
                    % (title.strip(), url.strip(), time.strip(), numStr.strip()))
            except Exception as err:
                self.saveDbFailure(url=baseUrl, title=title)
                print(err)
            finally:
                pass
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()

        # 关闭Connection:
        self.conn.close()
