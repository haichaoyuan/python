# 提供一个需要用户填写的HTML表单，然后处理表单结构
# HTML占位符展示
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # 2. 告知模板位置后，就可用用render方法读入模板文件
        self.render('index.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        # index.html用表单提交方式传递值到PoemPageHandler
        # 此处使用get_atgument方法获取值
        name = self.get_argument('name')
        age = self.get_argument('age')
        city = self.get_argument('city')
        love = self.get_argument('love')
        #3. 预先配置双大括号的Python的值，其中双大括号就是占位符
        self.render('poem.html', name = name, age = age, city = city, love = love, books=[
                "Learning Python",
                "Programming Collective Intelligence",
                "Restful Web Services"
            ])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 1. template_path参数告诉Tornado在哪里寻找模板文件，模板允许你嵌入Python代码片段到HTML文件
    app = tornado.web.Application(
        handlers = [(r'/', IndexHandler), (r'/poem', PoemPageHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates")
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()