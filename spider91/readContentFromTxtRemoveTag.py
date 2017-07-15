## 去除标签

import re
html='<a href="http://www.jb51.net">脚本之家</a>,Python学习！'
file = open('res/codeHtml')
print("读文件")
file = 'res/codeHtml'
with open(file, 'r') as f:
    # print(f.read())
    html = f.read()
## 使 . 匹配包括换行在内的所有字符
print("去除标签")
dr = re.compile(r'<[^>]+>',re.S)
## re.sub用于替换字符串中的匹配项
dd = dr.sub('',html)
print("写文件")
file2 = 'res/codeHtml2'
with open(file2, 'w') as file:
    file.write(dd)