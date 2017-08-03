# 导入一些模块
import tornado.ioloop
import tornado.web
import tornado.httpserver

# 监听命令行读取设置，比如port
from tornado.options import define,options
define("port", default= 8000, help = "run on the given port", type = int)

# 请求处理函数类，此处只定义get方法，故只处理get方法
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # RequestHandler.get_argument从查询字符串中读取参数greeting的值，要是没有，则取第二个参数作为默认
        greeting = self.get_argument('greeting', 'hello')
        # RequestHandler.write,写入HTTP响应中
        self.write(greeting+ ', friendly user!')
    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit,user! You caused a %d error."% status_code)


def make_app():
    # handlers是个元组，第一个元素用来匹配正则表达式，第二个是RequestHandler类
    return tornado.web.Application(handlers = [
        (r"/", IndexHandler)
    ])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 真正使Tornado运转起来的语句
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()