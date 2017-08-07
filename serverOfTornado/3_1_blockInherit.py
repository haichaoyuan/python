# 块继承，块占位
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index3_1.html')

class PoemPageHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name')
        age = self.get_argument('age')
        city = self.get_argument('city')
        love = self.get_argument('love')
        self.render('poem3_1.html', name = name, age = age, city = city, love = love, books=[
                "Learning Python",
                "Programming Collective Intelligence",
                "Restful Web Services"
            ])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [(r'/', IndexHandler), (r'/poem', PoemPageHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()