# ==========================================================
# ============= 写错误文件
# ==========================================================
# ========= 保存到数据库 存入数据库 meiziMain（_id, title, time, popular人气, like喜欢,）
import codecs
import os
import sqlite3


def store2ErrorFile(self, title, content):  # 保存到sqlite
    print(title)
    now_time = sqlite3.datetime.datetime.now().date().__str__()
    with codecs.open(os.getcwd() + '/res/error_' + now_time + '.txt', 'a+', 'utf-8') as file:
        file.write('===================================================title=======================\r\n')
        file.write(title)
        file.write('\r\n')
        file.write('===================================================content======================\r\n')
        file.write(content)
        file.write('\r\n')
        file.write('================================================================================\r\n=')
        file.write('==============================================我是帅气分割线=====================\r\n')
        file.write('===============================================================================\r\n')