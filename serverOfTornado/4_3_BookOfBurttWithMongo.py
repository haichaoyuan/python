# Burt需要一个书店，遍历在html，实际显示调用python的UI模块，模块再去呈现另个html
# 增加mongo的书籍存储
import os.path

import pymongo
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class initDict():
    def __init__(self):
        conn = pymongo.MongoClient("localhost", 27017)
        wordsData = conn.words
        words = wordsData.books
        words.insert({
            "title": "我的前半生",
            "author": "亦舒",
            "image": "https://img1.doubanio.com/mpic/s2720819.jpg",
            "description": "一个三十几岁的美丽女人子君，在家做全职家庭主妇。却被一个平凡女人夺走丈夫，一段婚姻的失败，让女主角不得不坚强，变得更美丽，有了事业，最终遇见一个更值得爱的男"
        })
        words.insert({
            "title": "百年孤独",
            "author": "[哥伦比亚] 加西亚·马尔克斯",
            "image": "https://img3.doubanio.com/mpic/s6384944.jpg",
            "description": "《百年孤独》是魔幻现实主义文学的代表作，描写了布恩迪亚家族七代人的传奇故事，以及加勒比海沿岸小镇马孔多的百年兴衰，反映了拉丁美洲一个世纪以来风云变幻的历史。"
        })
        words.insert({
            "title": "追风筝的人",
            "author": "[美] 卡勒德·胡赛尼 ",
            "image": "https://img3.doubanio.com/mpic/s1727290.jpg",
            "description": "12岁的阿富汗富家少爷阿米尔与仆人哈桑情同手足。然而，在一场风筝比赛后，发生了一件悲惨不堪的事，阿米尔为自己的懦弱感到自责和痛苦，逼走了哈桑，不久，自己也跟"
        })
        cursor = words.find()
        for result in cursor:
            print(result)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.table
        books = coll.find()
        self.render('index4_3.html',
                    title="haichao's Books",
                    header_text="Haha this is head line,ok  Welcome to my Books",
                    books=books
                    )

class RecommendHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.table
        books = coll.find().sort({"_id":1})
        self.render("recommended.html",
                    page_title = "haichao's Books | Recommend Reading",
                    header_text = "Recommended Reading",
                    books = books)

class AddRecommendHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("addNewBook.html")
    def post(self):
        mapped = dict()
        title = self.get_argument("title", "title")
        mapped["title"] = title
        author = self.get_argument("author", "author")
        mapped["author"] = author
        image = self.get_argument("image", "image")
        mapped["image"] = image
        description = self.get_argument("description", "description")
        mapped["description"] = description
        coll = self.application.table
        coll.save(mapped)
        self.redirect('/')

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string('book2.html', book=book)

    def css_files(self):
        return "/static/css/recommended.css"
    def javascript_files(self):
        return "/static/js/recommended.js"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/recommended", RecommendHandler),
            (r"/addNewBook.html", AddRecommendHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules=[{'hello': HelloModule}, {'Book': BookModule}],
            debug=True
        )
        conn = pymongo.MongoClient("localhost", 27017)
        self.db = conn["words"]
        self.table = self.db ["books"]
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    # initDict = initDict()
    # initDict.__init__()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
