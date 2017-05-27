# datetime是Python处理日期和时间的标准库

# ===========================
# 1. 获取当前时间
from datetime import datetime

print("===================")
print("1. 获取当前时间")
now = datetime.now()
print(now)
# 2017-05-26 10:49:33.913311
print(type(now))
# <class 'datetime.datetime'>

# ===========================
# 2. 获取指定日期和时间
print("===================")
print("2. 获取指定日期和时间")
dt = datetime(2015, 4, 19, 12, 20)
print(dt)
# 2015-04-19 12:20:00

# ===========================
# 3. 获取指定日期和时间
print("===================")
print("3. 获取指定日期和时间")
dt = datetime(2015, 4, 19, 12, 20)
print(dt)
print(dt.timestamp())
print(datetime.fromtimestamp(dt.timestamp()))
# 2015-04-19 12:20:00

# ===========================
# 4. str -> datetime，datetime-> str
print("===================")
print("4. str -> datetime")
dt = datetime(2015, 4, 19, 12, 20)
cday = dt.strftime('%Y-%m-%d  %H:%M:%S')
print(cday)
print(datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S'))
# 2015-04-19 12:20:00

# ===========================
# 5. datetime加减
from datetime import timedelta
print("===================")
print("5. datetime加减")
now = datetime.now()
print(now)
print(now + timedelta(hours=10))
print(now + timedelta(days=10))
print(now + timedelta(seconds=-11))
# 2015-04-19 12:20:00