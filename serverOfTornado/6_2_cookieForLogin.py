# 使用安全cookie实现简单登陆功能
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import base64,uuid
import os.path


from tornado.options import define, options
define("port", default= 8000, help= "run on the given port", type=int)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

#登陆页面 post请求，记录cookie
class LoginHandler(BaseHandler):
    def get(self):
        self.render('6_2_login.html')

    def post(self, *args, **kwargs):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect("/")

# authenticated装饰器,Tornado将确保这个方法的主体只有在合法的用户被发现时才会调用
# 1. 首先调用这个WelcomeHandler，由于被authenticated装饰，发现用户不合法(current_user为false),
# 服务器返回302，并跳转login_url
class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('6_2_index.html', user = self.current_user)

# 登出 清除cookir
class LogoutHandler(BaseHandler):
    def get(self):
        if(self.get_argument("logout", None)):
            self.clear_cookie("username")
            self.redirect("/")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    # 生成一个专属于我的安全码
    unique_code = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
    print("unique_code:%s" % unique_code)
    setting = {
        "template_path" :os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret":unique_code,
        "xsrf_cookies":True,#开启跨站攻击XSRF保护
        "login_url":"/login"
    }

    application = tornado.web.Application([
        (r'/', WelcomeHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
    ], **setting)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()