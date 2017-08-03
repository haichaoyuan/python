# 模板替代的升级版本
# 1. 一个页面post方式提交表单
# 2. 读取页面传递到的数据，进行处理，解析另一个页面并传入值
# 3. 页面HTML占位符展示和内嵌python代码显示
import os.path
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type = int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # 2. 告知模板位置后，就可用用render方法读入模板文件
        self.render('index2.html')

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        # 分行
        for line in text.split('\r\n'):
            # 分句子
            for word in  [x for x in line.split(' ') if len(x) > 0]:
                # 此处为dict的key是否存在的操作
                if word[0] not in mapped :
                    mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        self.render('poem3_1.html', source_map = source_map, change_lines = change_lines, choice = random.choice)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 1. template_path参数告诉Tornado在哪里寻找模板文件，模板允许你嵌入Python代码片段到HTML文件
    app = tornado.web.Application(
        handlers = [(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
        template_path = os.path.join(os.path.dirname(__file__), "templates"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        # 调用了一个便利的测试模式：tornado.autoreload模块，此时，一旦主要的Python文件被修改，Tornado将会尝试重启服务器，并且在模板改变时会进行刷新。
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()