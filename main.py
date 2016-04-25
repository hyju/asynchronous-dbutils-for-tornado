# -*- coding:utf-8 -*-
"""
tornado中对mysql,mongo数据库的异步操作
"""

from tornado.options import define, options
# define("env", default='develop', help="", type=str)
define("port", default=8899, help="run on the given port", type=int)

options.parse_command_line()

from tornado.ioloop import IOLoop
from tornado.web import RequestHandler
from tornado import web, gen

from dbutils import MySQLDBUtils, MongodbUtils


mysql_conn_app_dict = dict(host='127.0.0.1', port=3306,
                               user='test',
                               pwd='test',
                               db='test', charset='utf8',
                               max_idle_connections=10,
                               max_open_connections=100,
                               max_recycle_sec=3)
mongo_conn_log_dict = dict(mongo_auth_url='mongodb://127.0.0.1/log')

# 项目中各个pool只需要实例化一次
mysql_pool = MySQLDBUtils(mysql_conn_app_dict)
mongo_pool = MongodbUtils(mongo_conn_log_dict)

# 32行到59行的代码可以分至各个模块中,对已经实例化的pool实例按需所用
class GetInfoHandler(RequestHandler):
    """
    Mysql demo
    """
    @gen.coroutine
    def post(self):
        news_id = int(self.get_argument('news_id', '0'))
        search_sql = (
            "SELECT title,pubtime FROM News WHERE newsid = {newsid} "
        )
        news_info = yield mysql_pool.get_one(search_sql.format(news_id=news_id))

        info_dict = dict()
        info_dict['title'] = news_info[0]
        info_dict['pubtime'] = news_info[1]
        self.write({"code": "0", "msg": u"ok", "info": info_dict})

class ZanHandler(RequestHandler):
    """
    mongo demo
    """
    @gen.coroutine
    def post(self):
        db_zan_collection = mongo_pool.get_collection('db',
                                                      'collection')
        yield db_zan_collection.insert({'key': 'value'})
        self.write({"code": "0", "msg": u"ok"})


URLS = [
    (r'/mongo_test', ZanHandler),                       # mongo demo
    (r'/mysql_test', GetInfoHandler),                       # mysql demo
]

APPLICATION_SETTINGS = dict(
    debug=False,
    app_setting=""
    )

app = web.Application(URLS, **APPLICATION_SETTINGS)

if __name__ == "__main__":
    app.listen(options.port, xheaders=True)
    IOLoop.current().start()
