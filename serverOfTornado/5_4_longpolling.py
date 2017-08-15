# 长轮询例子
# 由于在库存变化时所有的推送请求同时应答和关闭，使得在浏览器重新建立连接时服务器受到了新请求的猛烈冲击。
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4


#  购物车，放入购物车，移出购物车，刷新库存
class ShoppingCart(object):
    totalInventory = 10  # 库存
    callbacks = [] # list
    carts = {} # dict

    # 注册回调
    def register(self, callback):
        self.callbacks.append(callback)

    # 获取剩余库存，总库存减去购物车放置的商品
    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    # 通知回调刷新页面
    ## // 3. 长轮训 添加或者删除操作，触发所有回调执行
    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)
        self.callbacks = []

    # 移动到购物车
    def moveItemToCart(self, session):
        if session in self.carts:
            return
        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return
        del (self.carts[session])
        self.notifyCallbacks()


# 获取库存
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render("longpolling.html", session=session, count=count)


# 执行加减购物车动作
class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        # session 不存在
        if not session:
            self.set_status(400)
            return

        # 放购物车
        if action == 'add':
            self.set_status(200)
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.set_status(200)
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)


class StatusHandler(tornado.web.RequestHandler):
    ## // 2. 长轮训 服务器注册回调，一直不响应客户端
    @tornado.web.asynchronous
    def get(self):
        self.application.shoppingCart.register(self.on_message)

    def on_message(self, count):## 4. 长轮训 响应客户端
        self.write('{"inventoryCount": "%d"}' % count)
        self.finish()


class Application(tornado.web.Application):
    def __init__(self):
        self.shoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
