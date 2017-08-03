# handlers的第一个参数是复杂正则
import textwrap
import tornado.ioloop
import tornado.web
import tornado.httpserver

# 监听命令行读取设置，比如port
from tornado.options import define,options
define("port", default= 8000, help = "run on the given port", type = int)

# 请求处理函数类，此处只定义get方法，故只处理get方法
class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        # RequestHandler.get_argument从查询字符串中读取参数greeting的值，要是没有，则取第二个参数作为默认
        greeting = self.get_argument('greeting', 'hello')
        # input[::-1] -1代表步数，意思反序
        self.write(greeting+ ', friendly user!'+ input[::-1])

class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        # wrap匹配路径/wrap的post请求
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))

def make_app():
    # handlers是个元组，第一个元素用来匹配正则表达式，第二个是RequestHandler类
    # 此处实例化了两个RequestHandler类对象，第一个正则表示匹配任何reverse开头，任意字符串结尾的路径
    return tornado.web.Application(handlers = [
        (r"/reverse/(\w+)", ReverseHandler),
        (r"/wrap", WrapHandler)
    ])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 真正使Tornado运转起来的语句
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()