# 啊哈哈 妹子图我来爬你了
# encoding=utf8
import codecs
import multiprocessing
import os
import random
import sqlite3
import threading
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://book.douban.com/tag/%E7%BB%8F%E5%85%B8?start=%s&type=T'
## 配置一些USER_AGENT, HEADER头进行模拟客户端抓取数据
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
Default_Header = {
    # 'Host': 'www.mmjpg.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': random.choice(UserAgent_List),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}
# 抓取数据
MAX_SIZE = 151 #最大页数
CUR_PAGE = 50 #当前页
NEXT_GOAL_PAGE = 60 #下个目标页

class SpiderMeizitu:
    def __init__(self) -> None:
        super().__init__()
        self._session = requests.session()
        self.SLEEP_TIME = 5
        self.PAGE_SIZE = 5
        self.values = []

    def getPageForMain(self, url):# 获取网页数据
        '''
        获取网页数据
        :param url: 
        :return: 
        '''
        print("======================================")
        print("===========step one getPage============")
        print("======================================")
        print("url:%s" % url)
        htmlContent = ''
        try:
            # response = requests.get("http://mm.howkuai.com/wp-content/uploads/2012a/03/09/01.jpg", headers=Default_Header)
            response = requests.get(url, headers=Default_Header)
            # _session.headers.update(Default_Header)
            # response = _session.get(url)
            #  www.mmjpg.com 没有正确编码，自行定义编码
            response.encoding = 'utf-8'
            htmlContent = response.text
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载' + url)
            self.saveDbFailure(url=url)
        return htmlContent

    def getPageForDetail(self, url):# 获取网页数据
        print("======================================")
        print("===========step one getPage============")
        print("======================================")
        print("url:%s" % url)
        htmlContent = ''
        try:
            # response = requests.get("http://mm.howkuai.com/wp-content/uploads/2012a/03/09/01.jpg", headers=Default_Header)
            response = requests.get(url, headers=Default_Header)
            # _session.headers.update(Default_Header)
            # response = _session.get(url)
            #  www.mmjpg.com 没有正确编码，自行定义编码
            response.encoding = 'gbk'
            htmlContent = response.text
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载' + url)
        return htmlContent

    def spiderByThread(self):# 多线程取数据
        # 1 - 151
        threads = []
        maxSize = MAX_SIZE
        i = CUR_PAGE
        # while(i <= 151):
        while(i <= NEXT_GOAL_PAGE):
            if len(threads) == 0: # 线程处理完，再起线程
                print('[spider]线程处理完，再起线程')
                for v in range( self.PAGE_SIZE):
                    url = 'http://www.mzitu.com/page/%d/'% i
                    i = i+ 1
                    if i > maxSize:
                        continue
                    thread = threading.Thread(target= self.spiderMainPage(url= url))  ##创建线程
                    # thread.setDaemon(True)  ##设置守护线程
                    thread.start()  ##启动线程+
                    threads.append(thread)  ##添加进线程队列
            time.sleep(self.SLEEP_TIME)
            for thread in threads:
                if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                    threads.remove(thread)
            print('[spider]后台线程走一走(dong:%d, rest:%d)'%(len(threads), self.PAGE_SIZE-len(threads)) )

    def spiderMainPage(self, url):# 爬主界面
        if not url:
            return
        htmlContent = self.getPageForMain(url)
        if not htmlContent:
            return
        liList = self.parseHtmlForMain(htmlContent)

        if len(liList) <= 0:
            return
        self.store2DBForMain(liList)
        print("===========finish============")

    def spider(self, url):# 主入口
        if not url:
            return
        htmlContent = self.getPage(url)
        if not htmlContent:
            return
        imgList = self.parseHtml(htmlContent)

        if len(imgList) <= 0:
            return
        self.store2DB(imgList)
        print("===========finish============")


    def downloadImgsByThread(self):#下载图片
        # crawl_queue = MogoQueue('meinvxiezhenji', 'crawl_queue')  ##这个是我们获取URL的队列
        ##img_queue = MogoQueue('meinvxiezhenji', 'img_queue')
        self.values = self.fetDataFromDb()
        threads = []
        while len(self.values) > 0:
            if threads or self.values:
                for thread in threads:
                    if not thread.is_alive():  ##is_alive是判断是否为空,不是空则在队列中删掉
                        threads.remove(thread)
                if len(threads) == 0: # 线程处理完，再起线程
                    print('线程处理完，再起线程')
                    for v in range( self.PAGE_SIZE):
                    # while len(threads) < max_threads :  ##线程池中的线程少于max_threads 或者 crawl_qeue时
                        thread = threading.Thread(target= self.downloadImgsIml)  ##创建线程
                        # thread.setDaemon(True)  ##设置守护线程
                        thread.start()  ##启动线程+
                        threads.append(thread)  ##添加进线程队列
                time.sleep(self.SLEEP_TIME)
                print('后台线程走一走')
                if len(self.values) <= 0:
                    self.values = self.fetDataFromDb()

    def downloadImgsIml(self):  # 下载图片
        if(len(self.values) <= 0):
            return
        start_time = time.clock()
        v = self.values.pop()
        no = v[0]
        src = v[1]
        title = v[2]
        print("downlaod image:%s（%d）" % (src , len(self.values)))
        response = ''
        try:
            # Default_Header['User-Agent'] = UserAgent_List[random.choice]random.choice(UserAgent_List),
            response = requests.get(src, headers=Default_Header)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载' + src)
            self.changetMeituState(self.STATUS_FAILURE, no)
            return
        htmlContent = response.content
        # 此处存入数据库好了
        names = src.split('/')
        if len(names) > 1:
            name = names[len(names) - 1]
        else:
            name = src
        file_path = 'res'
        file_path = self.mkdir(file_path, title)
        file_path = os.path.join(file_path, name)

        with codecs.open(os.getcwd() + '/'+ file_path, 'wb') as file:
            file.write(htmlContent)
        end_time = time.clock()
        total_time = float(end_time - start_time)
        self.changetMeituState(self.STATUS_SUCCESS, no)
        print("downlaod image:%s（%d）finish，总用时 : %f s" % (src, len(self.values), total_time))

    def mutiProcessDownloadImgs(self):# 入口2 多进程下载
        # values = self.fetDataFromDb()
        process = []
        num_cpus = multiprocessing.cpu_count()
        print('cpu_num:%d'% num_cpus)
        # num_cpus = 1
        for i in range(2):
            if i == 0:
                # 1 - 151
                # http://www.mzitu.com/page/151/
                url = 'http://www.meizitu.com/a/214.html'
                p = multiprocessing.Process(target= self.spiderByThread())
            else:
                p = multiprocessing.Process(target=self.downloadImgsByThread)
            p.start()# 启动进程
            process.append(p)
        for p in process:
            p.join()  ##等待进程队列里面的进程结束

    def fetDataFromDb(self):# 数据库查询db
        # 连接到SQLite数据库
        # 数据库文件是test.db
        # 如果文件不存在，会自动在当前目录创建:
        conn = sqlite3.connect('res/douban/meizitu.db')
        # 创建一个Cursor:
        cursor = conn.cursor()
        cursor.execute('select * from meitu where state != %d limit %d '% (self.STATUS_SUCCESS,  self.PAGE_SIZE))
        # 获得查询结果集:
        values = cursor.fetchall()
        print(values)
        # 关闭Cursor:
        cursor.close()
        # 关闭Connection:
        conn.close()
        return values


    def downloadImgs(self, imgList):# 下载图片
        print("===========step three download all image============")
        for img in imgList:
            src = img['src']
            title = img['title']
            print("downlaod image:%s" % src)
            try:
                # Default_Header['User-Agent'] = UserAgent_List[random.choice]random.choice(UserAgent_List),
                response = requests.get(src, headers=Default_Header)
            except requests.exceptions.ConnectionError:
                print('【错误】当前图片无法下载' + src)
                continue
            htmlContent = response.content
            # 此处存入数据库好了
            names = src.split('/')
            if (len(names) > 1):
                name = names[len(names) - 1]
            else:
                name = src
            tmpPath = 'res/' + title + '/' + name
            self.mkdir('res/', title)
            with codecs.open(tmpPath, 'ab') as file:
                file.write(htmlContent)

    def parseHtml(self, htmlContent):# 解析html
        print("===========step two BeautifulSoup Page============")
        soup = BeautifulSoup(htmlContent, "html.parser")
        soupList = soup.find('div', attrs={'class': 'postContent'})
        imgList = soupList.find_all('img')
        return imgList

    def parseHtmlForMain(self, htmlContent):# 解析html
        print("===========step two BeautifulSoup Page============")
        soup = BeautifulSoup(htmlContent, "html.parser")
        soupList = soup.find('ul', attrs={'id': 'pins'})
        liList = soupList.find_all('li')
        return liList

    def mkdir(self, file_path, img_title):  ## 创建文件夹
        file_path = file_path.strip()
        img_title = img_title.strip()
        path = os.path.join(file_path, img_title)
        if not os.path.exists(path):
            print(u'创建文件夹', path)
            os.makedirs(path)
        # os.chdir(path)
        return path

    def save2mongodb(self, imgList):#保存到数据库
        pass

    STATUS_FAILURE = 1
    STATUS_SUCCESS = 2
    def changetMeituState(self, status, id):
        self.conn = sqlite3.connect('res/douban/meizitu.db')
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        self.cursor.execute('update meitu set state = %d where id = %d'%(status, id))
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def saveDbFailure(self, url):#保存失败的url
        self.conn = sqlite3.connect('res/douban/meizitu.db')
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        # 执行一条SQL语句，创建user表: 91电影
        self.cursor.execute('create table if not exists meituFailure (id integer primary key autoincrement, '
                            'title text, url text, state int)')
        self.cursor.execute(
            "insert into meituFailure (title, url, state) values ('title',\'%s\', 0);"
            % (url.strip()))
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()
    def store2DB(self, imgList): #保存到sqlite
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        self.conn = sqlite3.connect('res/douban/meizitu.db')
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        # 执行一条SQL语句，创建user表: 91电影
        self.cursor.execute('create table if not exists meitu (id integer primary key autoincrement, '
                       'title text, url text, state int)')
        for soupItem in imgList:
            # 先拿标题
            try:
                # <img src="http://img.mmjpg.com/small/2017/1086.jpg" width="220" height="330" alt="磨人的小妖精温心怡美臀让人垂涎欲滴" />
                src = soupItem['src']
                alt = soupItem['title']
                print(src + ',' + alt)
                self.cursor.execute(
                    "insert into meitu (title, url, state) values (\'%s\',\'%s\', 0);"
                    % (src.strip(), alt.strip()))
            except Exception as err:
                print(err)
            finally:
                pass
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def store2DBForMain(self, imgList): #保存到sqlite
        # 连接到SQLite数据库
        # 如果文件不存在，会自动在当前目录创建:
        self.conn = sqlite3.connect('res/douban/meizitu.db')
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        # 执行一条SQL语句，创建user表: 91电影
        self.cursor.execute('create table if not exists meituUrl (id integer primary key autoincrement, '
                       'title text, url text, time datetime, num text)')
        for soupItem in imgList:
            # 先拿标题
            try:
                # <img src="http://img.mmjpg.com/small/2017/1086.jpg" width="220" height="330" alt="磨人的小妖精温心怡美臀让人垂涎欲滴" />
                spans = soupItem.findAll('span')
                url = spans[0].find('a')["href"]
                title = spans[0].find('a').string
                time = spans[1].string
                numStr = spans[2].string
                print(url + ',' + title+','+time +','+numStr)
                self.cursor.execute(
                    "insert into meituUrl (title, url, time, num) values (\'%s\',\'%s\', \'%s\',\'%s\');"
                    % (title.strip(), url.strip(), time.strip(), numStr.strip()))
            except Exception as err:
                print(err)
            finally:
                pass
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()

        # 关闭Connection:
        self.conn.close()

# the enter load
if __name__ == '__main__':
    page = 1
    spiderMeizitu = SpiderMeizitu()
    spiderMeizitu.mutiProcessDownloadImgs()
    # spiderMeizitu.downloadImgsIml()
    # html2Txt(page, url)