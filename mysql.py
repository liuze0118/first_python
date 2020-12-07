from MysqlApi import MysqlApi


class Mysql(object):
    def __init__(self):
        self.api = MysqlApi()

    def insert(self, sql):
        res = self.api.insert(sql)
