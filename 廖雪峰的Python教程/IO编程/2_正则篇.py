# ====================================================
# =====================正则
# 一. \d匹配一个数字，\w匹配一个字母或者数字
# 1.1. '00\d'匹配'007'
# 1.2. '\d\d\d' 匹配 '010'
# 1.3. '\w\w\d' 匹配 'pw3'
# 二. .匹配任意字符
# 2.1 'py.' 匹配 'pyc'、'py0'、'py!'、
# 三. 匹配变长字符
#  * 表示任意个字符(包括0个)，+ 表示至少一个字符，？表示0个或1个字符，
# {n}表示n个字符， {n,m }表示n-m个字符
# 3.1 \d{3}\s+\d{3,8} 表示3个数字+ 至少一个空格+ 3到8个数字

import re

r = re.match(r'^\d{3}\-\d{3,8}$', '010@123456')
print(r)

# ====================================================
# =====================切分字符串
print('=======切分字符串========')
print('a b;c'.split(' '))
print(re.split(r'[\s\;]','a b;c'))

# ====================================================
# =====================分组
print('=======分组========')
re_compile = re.compile(r'^(\d{3}-(\d{3,8}))$')
group = re_compile.match('010-123456')
print(group.groups())