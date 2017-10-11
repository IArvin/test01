# -*-coding: utf-8-*-
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from tornado.web import asynchronous
import torndb
from tornado.gen import coroutine
from utils.threadpool import ThreadPool
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import textwrap
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

threadpool = ThreadPool(50)

def config_log():
    level = logging.INFO
    fmt = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    log = logging.getLogger('')
    fileTimeHandler = TimedRotatingFileHandler('MVengine.log', "D", 1, 3)
    fileTimeHandler.suffix = "%Y%m%d.log"
    fileTimeHandler.setFormatter(logging.Formatter(fmt))
    logging.basicConfig(level=level, format=fmt)
    log.addHandler(fileTimeHandler)


class defaultsetting():
    def __init__(self):
        self.sql_conn = torndb.Connection("policy.tripto.cn:3306", "test", user="zanhao", password="zanhao1212")


class baseHandler(tornado.web.RequestHandler):
    @asynchronous
    def get(self):
        threadpool.add_task(self.dojob, self.request.body)

    @asynchronous
    def post(self):
        threadpool.add_task(self.dojob, self.request.body)

    def dojob(self, request_body):
        try:
            self.callback(request_body)
        except Exception, e:
            logging.exception(e)
        finally:
            self.finish()
            return

    def callback(self, request_body):
        if request_body == '':
            db = defaultsetting()
            self.add_header('Access-Control-Allow-Origin', '*')
            select_sql = "SELECT * FROM `mv_msg` LIMIT 0, 1;"
            result = db.sql_conn.query(select_sql)
            logging.info(result)
            self.write({'data': 'success'})


if __name__ == '__main__':
    config_log()
    db = defaultsetting()
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/homepage", baseHandler),
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()