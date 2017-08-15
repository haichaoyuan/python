import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print('hello world hc')
        self.write('hello world hc')
        self.write('<html><body><form action="/" method="post">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
    def post(self):
        self.set_header("Content-Type","text/plain")
        print('hello world hc')
        self.write("arg:"+ self.get_argument('message'))

class MainHandler2(tornado.web.RequestHandler):
    def get(self, story_id):
        print('hello world hc2')
        self.write('hello world hc2,id is '+ story_id)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/niubi/([0-9]+)", MainHandler2)
    ])

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()