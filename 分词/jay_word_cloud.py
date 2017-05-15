# coding: utf-8
# =================================================
# ===============生成杰伦兄歌词的词云
# =================================================
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import pandas as pd
import jieba

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# 1. 获取当前路径
dir = path.dirname(__file__)

# 3. 设置背景图片
# back_coloring = imread(path.join(dir, 'res/alice_color.png'))
back_coloring = imread(path.join(dir, 'res/jay2.png'))

# 解决中文字符显示问题
wordcloud = WordCloud(font_path='res/font/simhei.ttf', # 设置字体
                      background_color='white',#背景颜色
                      max_words= 2000, #词云最大的词数
                      max_font_size=40, #字体最大知
                      random_state=42,
                      mask= back_coloring# 设置背景图片
                      )


#2. 读取文件内容
# text = open(path.join(dir, 'res/周杰伦所有歌词.txt'), encoding= 'utf-8').read()
# text = processChinese(text)
# 1. 直接将字符串生成字云
# wordcloud.generate(text)
# 2. txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
def readFreqContentFromExcel():
    array = dict()
    ts = pd.read_excel('res/周杰伦所有歌词-分词.xls', 'sheet1', index_col=None, na_values=['NA'])
    for index,row in ts.head(2000).iterrows():
        array[row[0]] = row[1];
        print("获取行索引", index,'序号获取数据',row[0],'_',row[1])
    return array

txt_freq = readFreqContentFromExcel()
print(txt_freq)
# txt_freq = wordcloud.process_text(text)
result = wordcloud.generate_from_frequencies(txt_freq)

image_colors = ImageColorGenerator(back_coloring)
# image = wordcloud.to_image()
# image.show()

# 以下代码显示图片
# plt.imshow(wordcloud)
# plt.axis("off")

# 绘制词云
# 绘制背景图片为颜色的图片
plt.figure()
plt.imshow(wordcloud.recolor(color_func=image_colors))
plt.axis("off")
plt.show()


# 保存图片
wordcloud.to_file(path.join(dir, "res/jay_word_cloud.png"))

