from io import StringIO
from shutil import copyfile
# 拷贝文件tmp.html成tmp2.ht
copyfile('./tmp.html', './tmp2.ht')

import os

d = dict(name = 'bobo', age = 20)
print(d)
d['name'] = 'ok'
print(d)

import pickle
f = open('dump.txt', 'wb')
pickle.dump(d, f)
f.close()

f = open('dump.txt', 'rb')
d = pickle.load(f)
f.close()
print(d)