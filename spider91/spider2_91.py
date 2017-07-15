# 啊哈哈 91 我来爬你了
#encoding=utf8
import requests
from bs4 import BeautifulSoup
import re,time
import os,json
import base64
# from Crypto.Cipher import AES
from pprint import pprint
import sqlite3
import codecs

Default_Header = {
    'Host': '93.91p12.space',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

BASE_URL = 'http://93.91p12.space/index.php'

_session = requests.session()
_session.headers.update(Default_Header)

# =====================================================
# ============================= step one
# ============================= 最热页面 -> 模拟下一页的分页 -> 获取歌单列表 找到所有属性为'class':'tit f-thide s-fc0'的<a>
# =====================================================

#=====================================================
#============================= request -> html -> txt
#=====================================================
def html2Txt(page, filePath):
    print("===========step one getPage============")
    pageUrl = "http://93.91p12.space/video.php?page=%s&category=rf"%page
    print("url:%s" % pageUrl)
    htmlContent = _session.get(pageUrl).text
    # 此处存入数据库好了
    with codecs.open(filePath, 'wb', 'utf-8') as file:
        file.write(htmlContent)

    # soup = BeautifulSoup(htmlContent, "html.parser")
    # songList = soup.findAll('div', attrs={'class': 'listchannel'})
    # store2DB(songList)
    # for i in songList:
    #     print(i['href'])
        # getPlayList(i['href'])

#=====================================================
#============================= 从本地文件解析
#=====================================================
def txt2ParserWithBeautifulSoup(filePath):
    with codecs.open(filePath, 'rb', 'utf-8') as file:
        fileContent = file.read()
        soup = BeautifulSoup(fileContent, "html.parser")
        soupList = soup.findAll('div', attrs={'class': 'listchannel'})
        store2DB(soupList)
    pass

#=====================================================
#============================= 解析存数据库
#=====================================================
def store2DB(soupList):
    # 连接到SQLite数据库
    # 数据库文件是test.db
    # 如果文件不存在，会自动在当前目录创建:
    conn = sqlite3.connect('res/91p20/nineOneFilm.db')
    # 创建一个Cursor:
    cursor = conn.cursor()
    # 执行一条SQL语句，创建user表: 91电影
    cursor.execute('create table if not exists nineOneFilm (id integer primary key autoincrement, '
                   'videoHref text, videoTitle text, videoSrc text, videoTime varchar(100), videoAuthor varchar(100),'
                   'videoAuthorHref text)')
    cursor.execute('create table if not exists error (id integer primary key autoincrement, '
                   'context text, time datetime)')
    for soupItem in soupList:
        #先拿标题
        try:
            firstDivAs = soupItem.find_all('a')
            firstDivImgs = soupItem.find_all('img', width = 120)
            # 1. 拿到href
            videoHref = firstDivAs[0]['href']
            # 2. 拿到title
            videoTitle = firstDivImgs[0]['title']
            # 3. 拿到src
            videoSrc = firstDivImgs[0]['src']
            #3.拿时长
            spans = soupItem.find_all('span')
            timespan = spans[1]
            videoTime = timespan.next_sibling
            videoTime = videoTime.replace('\n', '')
            #4.作者
            videoAuthor = firstDivAs[2].string
            videoAuthorHref = firstDivAs[2]['href']
            print(videoHref + ',' + videoTitle + ',' + videoSrc +','+ videoTime + ',' +
                  videoAuthor+ ','+videoAuthorHref)
            cursor.execute("insert into nineOneFilm (videoHref, videoTitle , videoSrc , videoTime ,videoAuthor, videoAuthorHref) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');"
                           % (videoHref.strip(), videoTitle.strip() , videoSrc.strip() , videoTime.strip() , videoAuthor.strip(), videoAuthorHref.strip()))
        except Exception as err:
            cursor.execute("insert into error (context, time) values (\'%s\', datetime('now'))"
                           % (soupItem.prettify()))
            print(err)
        finally:
            pass
    # 关闭Cursor:
    cursor.close()
    # 提交事务:
    conn.commit()
    # 关闭Connection:
    conn.close()

if __name__=='__main__':
    # for i in range(1,43):
    #     getPage(str(i*35))
    page = 0
    filePath = 'res/91p20/page_%s.txt' % page
    # html2Txt(page, filePath)

    txt2ParserWithBeautifulSoup(filePath)
    # store2DB(0)
