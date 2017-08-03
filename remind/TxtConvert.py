import codecs  # 用于读取文件
import re

# 文件读写，字符串判断存在字符串，截取
file2Read = codecs.open("res/dataForConvert", 'r', 'utf-8')
file2Write = codecs.open("res/dataForConvert2", 'w', 'utf-8')

try:
    txts = file2Read.readlines( )
    for seg in txts:
        seg = seg.replace('\r', '').replace('\n', '').replace('\t', '')
        if(seg):
            print(seg)
            indexValue = '---'
            findIndex = seg.find(indexValue)

            if(findIndex != -1):
                seg2 = seg[findIndex + 3:]
                if (seg2):
                    file2Write.write(seg2)
                    file2Write.write('\r\n')
finally:
    file2Read.close( )
    file2Write.close( )
