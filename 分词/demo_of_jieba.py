#encoding = utf-8
# jieba的例子，更多例子可以参照https://github.com/fxsjy/jieba
import jieba

# 全模式
text = "我来到北京清华大学"
seg_list = jieba.cut(text, cut_all= True)
print(u"[全模式]","/".join(seg_list))

# 精确模式
seg_list = jieba.cut(text, cut_all=False)
print(u"[精确模式]: ", "/ ".join(seg_list))

# 默认是精确模式
seg_list = jieba.cut(text)
print(u"[默认模式]: ", "/ ".join(seg_list))

# 新词识别 “杭研”并没有在词典中,但是也被Viterbi算法识别出来了
seg_list = jieba.cut("他来到了网易杭研大厦")
print(u"[新词识别]: ", "/ ".join(seg_list))

# 搜索引擎模式,粒度比较细
seg_list = jieba.cut_for_search(text)
print(u"[搜索引擎模式]: ", "/ ".join(seg_list))