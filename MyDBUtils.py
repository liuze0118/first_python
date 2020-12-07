# -*- coding: UTF-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB
import DB_config as Config
import MySQLdb

'''
@功能：PT数据库连接池
'''


def getPTConnection():
    return PTConnectionPool()


def __exit__(self, type, value, trace):
    self.cursor.close()
    self.conn.close()
    print("PT连接池释放con和cursor")

    # 重连接池中取出一个连接


class PTConnectionPool(object):
    __pool = None

    def __enter__(self):
        self.conn = self.__getConn()
        self.cursor = self.conn.cursor()
        print("PT数据库创建con和cursor")
        return self

    def __getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=MySQLdb, mincached=Config.DB_MIN_CACHED, maxcached=Config.DB_MAX_CACHED,
                                   maxshared=Config.DB_MAX_SHARED, maxconnections=Config.DB_MAX_CONNECYIONS,
                                   blocking=Config.DB_BLOCKING, maxusage=Config.DB_MAX_USAGE,
                                   setsession=Config.DB_SET_SESSION,
                                   host=Config.DB_TEST_HOST, port=Config.DB_TEST_PORT,
                                   user=Config.DB_TEST_USER, passwd=Config.DB_TEST_PASSWORD,
                                   db=Config.DB_TEST_DBNAME, use_unicode=False, charset=Config.DB_CHARSET);
        return self.__pool.connection()

    def getConn(self):
        conn = self.__getConn()
        cursor = conn.cursor()
        return cursor, conn
