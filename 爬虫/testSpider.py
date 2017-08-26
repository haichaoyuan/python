# 啊哈哈 91 我来爬你了
# encoding=utf8
import requests
from bs4 import BeautifulSoup
import re, time
import os, json
import base64
# from Crypto.Cipher import AES
from pprint import pprint
import sqlite3
import codecs
import pymongo

Default_Header = {
    'Host': 'www.mmjpg.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

BASE_URL = 'https://book.douban.com/tag/%E7%BB%8F%E5%85%B8?start=%s&type=T'

_session = requests.session()
_session.headers.update(Default_Header)


# =====================================================
# ============================= step one
# ============================= 最热页面 -> 模拟下一页的分页 -> 获取歌单列表 找到所有属性为'class':'tit f-thide s-fc0'的<a>
# =====================================================

# =====================================================
# ============================= request -> html -> txt
# =====================================================
def html2Txt(page, filePath):
    print("===========step one getPage============")
    if page:
        pageUrl = r'http://www.mmjpg.com/home/%s' % (page)
    else:
        pageUrl = r'http://www.mmjpg.com/home/'
    print("url:%s" % pageUrl)
    response = _session.get(pageUrl)
    #  www.mmjpg.com 没有正确编码，自行定义编码
    response.encoding = 'utf-8'
    htmlContent =response.text
    # htmlContent.encode('latin1').decode('utf-8')
    # 此处存入数据库好了
    with codecs.open(filePath, 'wb', 'utf-8') as file:
        file.write(htmlContent)

# =====================================================
# ============================= 从本地文件解析
# =====================================================
def txt2ParserWithBeautifulSoup(filePath):
    with codecs.open(filePath, 'rb', 'utf-8') as file:
        fileContent = file.read()
        soup = BeautifulSoup(fileContent, "html.parser")
        soupList = soup.find('div', attrs={'class': 'pic'})
        imgList = soupList.find_all('img')
        return imgList
    pass


# =====================================================
# ============================= 解析存数据库
# =====================================================
def store2DB(soupList):
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('res/douban/meitu.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表: 91电影
    cursor.execute('create table if not exists meitu (id integer primary key autoincrement, '
                   'title text, url text)')
    for soupItem in soupList:
        # 先拿标题
        try:
            # <img src="http://img.mmjpg.com/small/2017/1086.jpg" width="220" height="330" alt="磨人的小妖精温心怡美臀让人垂涎欲滴" />
            src = soupItem['src']
            alt = soupItem['alt']
            print(src + ',' + alt)
            cursor.execute(
                "insert into meitu (title, url) values (\'%s\',\'%s\');"
                % (src.strip(), alt.strip()))
        except Exception as err:
            print(err)
        finally:
            pass
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()


# =============== load data from net
def html2Content(page, filePath):
    print("===========step one getPage============")
    pageUrl = r'http://www.mmjpg.com/home/%s' % (page * 20)
    print("url:%s" % pageUrl)
    htmlContent = _session.get(pageUrl).text
    return htmlContent

# =============download img
def downloadImg(imgList):
    for img in imgList:
        src = img['src']
        alt = img['alt']
        print("downlaod url:%s" % src)

        #  www.mmjpg.com 没有正确编码，自行定义编码
        # response.encoding = 'utf-8'
        try:
            response = _session.get(src, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载'+ src)
            continue
        htmlContent = response.content
        # htmlContent.encode('latin1').decode('utf-8')
        # 此处存入数据库好了
        names = src.split('/')
        if(len(names) > 1):
            name = names[len(names) -1]
        else:
            name = src
        with codecs.open('res/douban/'+ name , 'wb') as file:
            file.write(htmlContent)
        break


# the enter load
if __name__ == '__main__':
    # step 1:网络爬数据
    # for i in range(1,43):
    #     getPage(str(i*35))
    page = 1
    filePath = 'res/douban/page_%s.txt' % page
    # htmlContent = html2Txt(page, filePath)

    # step 2: 解析数据
    imgList = txt2ParserWithBeautifulSoup(filePath)
    # store2DB(imgList)
    # step 3: 下载图片
    downloadImg(imgList)
