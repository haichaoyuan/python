# 一个简单词典
# 如： http://localhost:8000/?word=lemon
# back： definition:柠檬
import pymongo
import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type = int)

class initDict():
    def __init__(self):
        conn = pymongo.MongoClient("localhost", 27017)
        wordsData = conn.words
        words = wordsData.words
        words.insert({"word": "apple", "definition": "苹果"})
        words.insert({"word": "banana", "definition": "香蕉"})
        words.insert({"word": "peach", "definition": "桃子"})
        words.insert({"word": "lemon", "definition": "柠檬"})
        words.insert({"word": "avocado", "definition": "南美梨"})
        words.insert({"word": "grape", "definition": "葡萄"})
        words.insert({"word": "plum", "definition": "李子"})

        cursor = words.find()
        for result in cursor:
            print(result)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        word = self.get_argument('word', 'apple')

        conn = pymongo.MongoClient("localhost", 27017)
        wordsData = conn.words
        words = wordsData.words
        document = words.find_one({"word":word})
        if document:
            self.write("definition:" + document["definition"])
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [(r'/', IndexHandler)],
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()