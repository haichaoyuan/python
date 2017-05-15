import xlrd
import xlwt
from os import path
import jieba  # 用来给文档内容分词
import numpy  # 词频统计时会调用numpy的统计函数
import codecs  # 用于读取文件
import pandas  # 用于基本数据处理以及导出excel

stopwords = {}

def generateStopWords(filename = ''):
    global stopwords
    stopwords = set([x.strip() for x in open(path.join(path.dirname(__file__), filename)).read().split('\n')])
    # f = open(filename, 'r', encoding='utf-8')
    # line = f.readline().strip()
    #
    # while line:
    #     stopwords.setdefault(line, 0)
    #     stopwords[line] = 1
    #     line = f.readline().strip()
    #
    # f.close()

def processChinese(text):
    seg_generator = jieba.cut(text) # 使用结巴分词
    seg_list = [i for i in seg_generator if i not in stopwords]
    seg_list = [i for i in seg_list if i != u' ']
    seg_str = r' '.join(seg_list)
    return seg_str

# 1. codecs自然语言编码模块，用于读取文件，区别去open,可忽略格式，utf-8,unicode
#  区别open方法，完成input文件(gbk, utf-8...)   ----decode----->   unicode  -------encode------> output文件(gbk, utf-8...)
file = codecs.open("res/周杰伦所有歌词.txt", 'r', 'utf-8')
content = file.read()
file.close()
segments = []
# 2. jieba分词模块，进行分词，返回迭代器
segs = jieba.cut(content)
for seg in segs:
    # 3. 此处应该加个文本的初步处理，去除空格,只挑选2个字
    if len(seg.strip()) > 1:
        print(seg)
        segments.append(seg)
# 4. pandas模块 列表 -> DataFrame
segmentDF = pandas.DataFrame({'segment': segments})
segmentDF.to_excel('res/周杰伦所有歌词-分词tmp.xls', sheet_name='sheet1')
df = segmentDF.groupby("segment")["segment"]
df = df.agg({"计数": numpy.size}).reset_index()
# df = df.sort_values(columns=['计数'], ascending=False)
df = df.sort_values(by=('计数'), ascending=False)
print(df.head(100))
# 5.xlwt模块， 转xls
df.to_excel('res/周杰伦所有歌词-分词.xls', sheet_name='sheet1')