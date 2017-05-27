# base64,把3字节的二进制编码未4字节的文本数据，长度增加33%，但是正文都可以显示
# 编码的二进制数据不是3的倍数，若剩余1个或2个字节，会末尾用\x00补齐,再在末尾怎讲1个或两个= 号，表示补了多谢字节

# =============================
# 1.base64编解码
print('=============================')
print('1.base64编解码')
import base64
mbase = base64.b64encode(b'hello world')
print(mbase)
morign = base64.b64decode(mbase)
print(morign)
# 正常Base64编码会出现+ 和 / ,但是不可使用url作为参数，所有有种url safe的base64编码，其实就是吧+ 和 /变成 - 和 _
print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))
urlsafe = base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
print(urlsafe)
print(base64.urlsafe_b64decode(urlsafe))

# =============================
# 2.摘要算法MD5和sha1
print('=============================')
print('2.MD5')
import hashlib
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())

# =============================
# 3.摘要算法sha1
print('=============================')
print('3.摘要算法sha1')
md5 = hashlib.sha1()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())

# =============================
# 4.xml解析，xml解析有两种，DOM和SAX,
# DOM会把整个XML读入内存中，解析为树，优点，可得到节点概况，节点数目，遍历任意树的节点，缺点占用内存大，解析慢
# SAX是流模式，边读边解析，占用内存小，解析快，缺点是需要我们自己处理事件，自己处理站到需要的节点
