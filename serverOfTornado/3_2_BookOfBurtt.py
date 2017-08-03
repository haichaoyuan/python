# Burt需要一个书店，遍历在html，实际显示调用python的UI模块，模块再去呈现另个html
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index3_2.html',
                    title = "haichao's Books",
                    header_text = "Haha this is head line,ok  Welcome to my Books",
                    books=[
                        {
                            "title": "Programming Collective Intelligence",
                            "subtitle": "Building Smart Web 2.0 Applications",
                            "image": "https://img3.doubanio.com\/img\/celebrity\/large\/39105.jpg",
                            "author": "Toby Segaran",
                            "date_added": 1310248056,
                            "date_released": "August 2007",
                            "isbn": "978-0-596-52932-1",
                            "description": "<p>This fascinating book demonstrates how you "
                                           "can build web applications to mine the enormous amount of data created by people "
                                           "on the Internet. With the sophisticated algorithms in this book, you can write "
                                           "smart programs to access interesting datasets from other web sites, collect data "
                                           "from users of your own applications, and analyze and understand the data once "
                                           "you've found it.</p>"
                        },
                        {
                            "title": "Programming Collective Intelligence",
                            "subtitle": "Building Smart Web 2.0 Applications",
                            "image": "https://img1.doubanio.com\/img\/celebrity\/large\/1415801312.29.jpg",
                            "author": "Toby Segaran",
                            "date_added": 1310248056,
                            "date_released": "August 2007",
                            "isbn": "978-0-596-52932-1",
                            "description": "<p>This fascinating book demonstrates how you "
                                           "can build web applications to mine the enormous amount of data created by people "
                                           "on the Internet. With the sophisticated algorithms in this book, you can write "
                                           "smart programs to access interesting datasets from other web sites, collect data "
                                           "from users of your own applications, and analyze and understand the data once "
                                           "you've found it.</p>"
                        }
                        # {"title": "title3", "image": "https://img3.doubanio.com\/img\/celebrity\/large\/1401440361.14.jpg"},
                        # {"title": "title4",
                        #  "image": "https://img3.doubanio.com\/img\/celebrity\/large\/1370330521.5.jpg"},
  ])

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'

class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('book.html', book = book)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            debug = True
        )
        tornado.web.Application.__init__(self, handlers, **settings, ui_modules = [{'hello':HelloModule}, {'Book':BookModule}])

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()