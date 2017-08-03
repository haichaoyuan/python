# 一些mongo的一般用法
import pymongo

conn = pymongo.MongoClient("localhost", 27017)
db = conn.test
print(db.collection_names())
widgets = db.widgets

#1. 插入一个集合
# print(widgets.insert({"foo":"bar"}))
# print(db.collection_names())

#2. 再插入一个集合
# print(widgets.insert({"name":"flibnip", "description":"grade-A industrial flipnip", "quantity":3}))
#3. 查询，条件是个集合
# print(widgets.find_one({"name":"flibnip"}))

#4. 查询所有,
cursor = widgets.find()
for result in cursor:
    print(result)


# 5. 查询，更改，再保存
# flip = widgets.find_one({"name":"flibnip"})
# print(flip)
# flip["description"] = "new discripde";
# widgets.save(flip)


#6.移除
# widgets.remove({"name":"flibnip"})

# 7. 读取数据，删除id，序列化
flip = widgets.find_one({"foo":"bar"})
print(flip)
del flip["_id"]
import json
print(json.dumps(flip))

cursor = widgets.find()
for result in cursor:
    print(result)