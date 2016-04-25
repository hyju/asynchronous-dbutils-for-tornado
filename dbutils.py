# -*- coding: utf-8 -*- #
"""
数据库操作公用方法
"""


from tornado import gen
from tornado_mysql import pools
from tornado_mysql.cursors import DictCursor
from motor import MotorClient


class MySQLDBUtils(object):
    """
    MYSQL数据库操作类
    """

    def __init__(self, db_conn_dict):
        """
        数据库连接
        :param db_conn_dict:数据库连接参数
        :return:
        """
        self.pool = MySQLDBUtils.create_pool(db_conn_dict)
        self.pool_dict = MySQLDBUtils.create_pool(db_conn_dict, cursor_class="DictCursor")

    @gen.coroutine
    def get_all(self, query, param=None, cursor='list'):
        """
        执行查询，并取出所有结果集
        :param query:  查询语句
        :param param:  参数列表 条件列表值（元组/列表）
        :param cursor:  指定cursor的返回类型
        :return: ((column_1, column_2), (column_1, column_2))
        """
        if cursor == 'dict':
            if param:
                cursor = yield self.pool_dict.execute(query, param)
            else:
                cursor = yield self.pool_dict.execute(query)
        elif cursor == 'list':
            if param:
                cursor = yield self.pool.execute(query, param)
            else:
                cursor = yield self.pool.execute(query)
        res = cursor.fetchall()
        raise gen.Return(res)

    @gen.coroutine
    def get_one(self, query, param=None, cursor=''):
        """
        执行查询，并取出第一条
        :param query:  查询语句
        :param param:  参数列表 条件列表值（元组/列表）
        :param cursor:
        :return: (column_1, column_2, column_3)
        """
        if cursor == 'dict':
            if param:
                cursor = yield self.pool_dict.execute(query, param)
            else:
                cursor = yield self.pool_dict.execute(query)
        else:
            if param:
                cursor = yield self.pool.execute(query, param)
            else:
                cursor = yield self.pool.execute(query)
        res = cursor.fetchone()
        raise gen.Return(res)

    @gen.coroutine
    def get_many(self, query, param=None, num=20, cursor='list'):
        """
        执行查询，并取出num条结果
        :param query:  查询语句
        :param param: 可选参数，条件列表值（元组/列表）
        :param num: 指定条数
        :param cursor:
        :return: ((column_1, column_2), (column_1, column_2))
        """
        if cursor == 'dict':
            if param:
                cursor = yield self.pool_dict.execute(query, param)
            else:
                cursor = yield self.pool_dict.execute(query)
        elif cursor == 'list':
            if param:
                cursor = yield self.pool.execute(query, param)
            else:
                cursor = yield self.pool.execute(query)
        res = cursor.fetchmany(num)
        raise gen.Return(res)

    @gen.coroutine
    def insert_one(self, query, param=None):
        """
        向数据表插入一条记录
        :param query:  SQL语句
        :param param: 参数
        :return:
        """
        if param:
            res = yield self.pool.execute(query, param)
        else:
            res = yield self.pool.execute(query)
        raise gen.Return(res)

    @gen.coroutine
    def insert_many(self, query, param=None):
        """
        向数据表插入多条记录
        :param query: SQL语句
        :param param: 参数
        :return:
        """
        if param:
            res = yield self.pool.executemany(query, param)
        else:
            res = yield self.pool.executemany(query)

        raise gen.Return(res)

    @gen.coroutine
    def delete(self, query, param=None):
        """
        删除数据表记录
        :param query:  SQL语句
        :param param: 参数
        :return:
        """
        if param:
            res = yield self.pool.execute(query, param)
        else:
            res = yield self.pool.execute(query)
        raise gen.Return(res)

    @gen.coroutine
    def update(self, query, param=None):
        """
        更新数据表记录
        :param query: SQL语句
        :param param: 参数
        :return:
        """
        if param:
            res = yield self.pool.execute(query, param)
        else:
            res = yield self.pool.execute(query)
        raise gen.Return(res)

    @gen.coroutine
    def get_data_from_db(self, query, param=None, search_type='all', num=10, cursor='list'):
        """
        获取数据表的数据
        :param query: 查询语句
        :param param: 参数
        :param search_type: one:查询单条 all:查询全部 many:查询指定条数
        :param num: 指定条数
        :param cursor:
        :return:
            one: (column_1, column_2, column_3)
            all: ((column_1, column_2), (column_1, column_2))
            many: ((column_1, column_2), (column_1, column_2))
        """
        if cursor == 'dict':
            if param:
                cursor = yield self.pool_dict.execute(query, param)
            else:
                cursor = yield self.pool_dict.execute(query)
        elif cursor == 'list':
            if param:
                cursor = yield self.pool.execute(query, param)
            else:
                cursor = yield self.pool.execute(query)
        if search_type == 'one':
            res = cursor.fetchone()
        elif search_type == 'all':
            res = cursor.fetchall()
        else:
            res = cursor.fetchmany(num)
        raise gen.Return(res)

    @gen.coroutine
    def operate_db(self, query, param=None):
        """
        操作数据表的数据
        :param query: SQL语句
        :param param: 参数
        :return:
        """
        if param:
            res = yield self.pool.execute(query, param)
        else:
            res = yield self.pool.execute(query)
        raise gen.Return(res)

    @staticmethod
    def create_pool(para, cursor_class=''):
        """
        生成数据库连接池
        :param para: 数据库配置参数
        :param cursor_class:
        :return:
        """
        if cursor_class == "DictCursor":
            return pools.Pool(dict(host=para['host'],
                                   port=3306,
                                   user=para['user'],
                                   passwd=para['pwd'],
                                   db=para['db'],
                                   charset=para['charset'],
                                   cursorclass=DictCursor
                                   ),
                              max_idle_connections=10,
                              max_open_connections=100,
                              max_recycle_sec=3)
        else:
            return pools.Pool(dict(host=para['host'],
                                   port=3306,
                                   user=para['user'],
                                   passwd=para['pwd'],
                                   db=para['db'],
                                   charset=para['charset']
                                   ),
                              max_idle_connections=10,
                              max_open_connections=100,
                              max_recycle_sec=3)


class MongodbUtils(object):
    """
    mongodb操作类
    """

    def __init__(self, db_conn_dict):
        """
        数据库连接
        :param db_conn_dict:数据库连接参数
        :return:
        """
        self.client = MongodbUtils.create_pool(db_conn_dict)

    def get_collection(self, db_name, collection_name):
        """
         获取指定数据库中的collection
        :param db_name:
        :param collection_name:
        :return:
        """
        db = self.client[db_name]
        return db[collection_name]

    @staticmethod
    def create_pool(para):
        """
        生成数据库连接池
        :param para: 数据库配置参数
        :param cursor_class:
        :return:
        """
        client = MotorClient(para['mongo_auth_url'])
        return client
