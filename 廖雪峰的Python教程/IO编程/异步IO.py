# ========================================================
# ================== yield send实现协程
# ========================================================
# 消费者
def consumer():
    r = ''
    while True:
        # 2. 通过yield拿到数据，处理，并把数据返回
        n = yield r
        if not n :
            return
        print('[CONSUMER] Consuming %s...'% n)
        r = '200 OK'

# 生产者
def produce(c):
    # 1. 启动生成器
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s ...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    # 关闭启动器
    c.close

# 协程例子
def fun1_coroutine_demo():
    c = consumer()
    produce(c)


# ========================================================
# ================== asincio使用
# ========================================================
import asyncio
import threading
# 把generator标记为coroutine类型
@asyncio.coroutine
def coroutine_demo():
    print("hello coroutine!(%s)"% threading.current_thread())
    # 异步调用asyncio.sleep(1)
    r = yield from asyncio.sleep(1)
    print('hello again!(%s)' % threading.current_thread())

def fun2_coroutine():
    # 获取EventLoop
    loop = asyncio.get_event_loop()
    # 执行coroutine
    tasks = [coroutine_demo(), coroutine_demo()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


# ========================================================
# ================== asincio异步网络链接
# ========================================================
@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0 \r\n Host: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s'% (host, line.decode('utf-8').rstrip()))
    writer.close()

def fun3_network():
    loop = asyncio.get_event_loop()
    tasks = [wget(host) for host in ['www.sina.com', 'www.qq.com', 'www.163.com']]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()



# ========================================================
# ================== aiohttp异步网络链接
# ========================================================
import asyncio
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    return web.Response(body=b'<h1>Index</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s!</h1>' % request.match_info['name']
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    app.router.add_route('GET', '/hello/{name}', hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print('Server started at http://127.0.0.1:8000...')
    return srv

def fun4_aiohttp():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


# fun1_coroutine_demo()
# fun2_coroutine()
# fun3_network()
fun4_aiohttp()