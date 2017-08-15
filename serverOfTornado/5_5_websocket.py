# WebSockets H5新提出的客户-服务器通讯协议
# 涉及到WebSocketHandler
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4
import sys

class ShoppingCart(object):
    totalInventory = 10  # 库存
    callbacks = [] # list
    carts = {} # dict

    # 注册回调
    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)

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
        self.render("longpolling2.html", session=session, count=count)


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


class StatusHandler(tornado.websocket.WebSocketHandler):
    def callback(self, count):
        self.write_message('{"inventoryCount": "%d"}' % count)

    def open(self):
        self.application.shoppingCart.register(self.callback)

    def on_close(self):
        self.application.shoppingCart.unregister(self.callback)

    def on_message(self, count):
        pass


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
