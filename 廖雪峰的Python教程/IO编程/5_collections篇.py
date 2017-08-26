# collections是python内建的一个集合模块

# =============================
# 1. nametuple带名字的元组
from collections import namedtuple
#定义点
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x)
print(p.y)
# 定义园
Circle = namedtuple('Circle', ['x', 'y', 'z'])

# =============================
# 2. deque,双向链表，解决list访问快速，插入和删除慢速的问题，高效实现插入和删除
# 适合作为栈和队列
print('=============================')
print('2. deque,双向链表')
from collections import deque
q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)
print(q.pop()) #删除数据
print(q)
print(q.popleft())
print(q)

# =============================
# 3. defaultdict, dict中当key不存在，就好抛出KeyError,若想存在key不存在情况，可选用defaultdict
print('=============================')
print('3. defaultdict')
from collections import defaultdict
dd = defaultdict(lambda :'N/A')
# key 存在
dd['key1'] = 'abcd'
print(dd['key1'])
# 可以不存在，返回默认
print(dd['key2'])


# =============================
# 4. orderedDict,带插入顺序的dict
print('=============================')
print('4. orderedDict')
from collections import OrderedDict
d = dict([('a', 1),  ('c', 3), ('b', 2)])
d['d'] = 5
print(d)
od = OrderedDict()
od['z'] = 1
od['y'] = 2
od['x'] = 3
print(list(od.keys()))
 # =============================
# 5. counter,简单计数器
print('=============================')
print('5. counter,简单计数器')
from collections import Counter
c = Counter()
for ch in 'programing':
    c[ch] += 1
print(c)