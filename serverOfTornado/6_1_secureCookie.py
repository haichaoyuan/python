# 使用安全cookie
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import base64,uuid


from tornado.options import define, options
define("port", default= 8000, help= "run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        cookie = self.get_secure_cookie("count")
        count = int(cookie) + 1 if cookie else 1

        countString = "1 time" if count == 1 else "%d times" % count

        self.set_secure_cookie("count", str(count))
        self.write(
            '<html><head><title>Cookie Counter</title></head>'
            '<body><h1>you;ve viewed this page %s times.</h1>' % countString+
            '<body><h1>您已经查看了该页面 %s 次。</h1>' % countString +
            '</body></html>'
        )

if __name__ == "__main__":
    tornado.options.parse_command_line()
    # 生成一个专属于我的安全码
    unique_code = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    print("unique_code:%s" % unique_code)
    setting = {
        "cookie_secret":unique_code
    }

    application = tornado.web.Application([
        (r'/', MainHandler)
    ], **setting)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()