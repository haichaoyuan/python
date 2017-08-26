# 一个推特计步器
# 增加异步操作
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time
import random

from tornado.options import define,options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    #1. 增加异步注解
    @tornado.web.asynchronous
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        response = client.fetch("https://api.douban.com/v2/movie/in_theaters", callback=self.on_response)


    def on_response(self, response):
        body = json.loads(response.body)
        now = datetime.datetime.utcnow()
        seconds_diff = random.randint(100, 1000)
        time.sleep(5)
        self.write("""
               <div style="text-align: center">
                   <div style="font-size: 72px">%s</div>
                   <div style="font-size: 144px">%.02f</div>
                   <div style="font-size: 24px">tweets per second</div>
                   <div style="font-size: 24px">%s</div>
               </div>""" % ('abcd', seconds_diff, body))
        # 异步回调完成后的finish操作
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()