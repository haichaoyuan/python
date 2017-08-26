# ==================================================
# ============================ 爬取主界面
# ===================================================
import sqlite3
import threading
import time

import requests
from bs4 import BeautifulSoup

import spider2Meizitu.Constants as Constants


class SpiderBasePage():
    def __init__(self) -> None:
        super().__init__()

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
            print('【错误】当前图片无法下载' + url)
            self.saveDbFailure(url=url)
        return htmlContent

    # ==================================================
    # ============================ failure表
    # ===================================================
    # ========= 保存主界面错误数据
    def saveDbFailure(self, url, title = 'title', type = 0):  # 保存失败的url
        # connect -> cursor -> create table -> insert record -> close cursor -> close conn
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cursor = self.conn.cursor()
        # title 标题，url 路径，type 类型：暂定（0：主界面抓取失败，1：详细页面抓取失败，2：下载图片失败）
        self.cursor.execute('create table if not exists meitiFailure (id integer primary key autoincrement, '
                            'title text, url text, type int, state int)')
        self.cursor.execute(
            "insert into meituFailure (title, url, state, type) values (\'%s\',\'%s\', 0, 0, %d);"
            % (title.strip(), url.strip(), type))
        # 关闭Cursor:
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    # ==================================================
    # ============================ 主库
    # ===================================================
    # ========= 更新主库数据状态
    def changeMainState(self, url, status):
        self.conn = sqlite3.connect(Constants.DB_PATH)
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        self.cursor.execute('update meitiMain set status = %s where url = \'%s\'' % (status, url))
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    # ==================================================
    # ============================ 详情库
    # ===================================================
    # ========= 更新详情库数据状态
    def changeDetailState(self, url, status):
        self.conn = sqlite3.connect(Constants.DB_PATH)
        # 创建一个Cursor:
        self.cursor = self.conn.cursor()
        self.cursor.execute('update meitiDetail set status = %s where url = \'%s\'' % (status, url))
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def fetDetailDataFromDb(self):  # 数据库查询db
        conn = sqlite3.connect(Constants.DB_PATH)
        # 创建一个Cursor:
        cursor = conn.cursor()
        cursor.execute(
            'select url from meitiDetail where status == %d limit %d ' % (Constants.STATUS_INITIAL, Constants.PAGE_SIZE))
        # 获得查询结果集:
        values = cursor.fetchall()
        print("===========step zero fetch from db============")
        print(values)
        # 关闭Cursor:
        cursor.close()
        # 关闭Connection:
        conn.close()
        return values