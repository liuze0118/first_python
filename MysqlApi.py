from MyDBUtils import getPTConnection


class MysqlApi(object):
    mysql = None

    def __init__(self):
        # self.connect()
        self.db = getPTConnection()
        print("初始化Mysql-Api")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'inst'):
            cls.inst = super(MysqlApi, cls).__new__(cls, *args, **kwargs)
        return cls.inst

    # 查询所有
    def selectall(self, sql='', param=()):
        # 判断是否连接,并设置重连机制
        # self.connected()
        try:
            cursor, conn = self.execute(sql, param)
            res = cursor.fetchall()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print('selectall except   ', e.args)
            self.close(cursor, conn)
            return None

    # 查询一条
    def selectone(self, sql='', param=()):
        """

        :rtype: object
        """
        # self.connected()
        try:
            # cur = self.db.cursor()
            cursor, conn = self.execute(sql, param)
            res = cursor.fetchone()
            self.close(cursor, conn)
            return res
        except Exception as e:
            print('selectone except   ', e.args)
            self.close(cursor, conn)
            return None

    # 增加
    def insert(self, sql='', param=()):
        # self.connected()
        try:
            # self.db.getconn().execute(sql, param)
            cursor, conn = self.execute(sql, param)
            print('============')
            # _id=self.db.conn.insert_id()
            _id = cursor.lastrowid
            print('_id   ', _id)
            conn.commit()
            self.close(cursor, conn)
            # 防止表中没有id返回0
            if _id == 0:
                return True
            return _id
        except Exception as e:
            print('insert except   ', e.args)
            conn.rollback()
            self.close(cursor, conn)
            # self.conn.rollback()
            return 0

    # 增加多行
    def insertmany(self, sql='', param=()):
        # self.connected()
        cursor, conn = getConn()
        try:
            cursor.executemany(sql, param)
            # self.execute(sql,param)
            conn.commit()
            self.close(cursor, conn)
            return True
        except Exception as e:
            print('insert many except   ', e.args)
            conn.rollback()
            self.close(cursor, conn)
            # self.conn.rollback()
            return False

    # 删除
    def delete(self, sql='', param=()):
        # self.connected()
        try:
            # cur = self.conn.cursor()
            # self.db.getconn().execute(sql, param)
            cursor, conn = self.execute(sql, param)
            # self.db.conn.commit()
            self.close(cursor, conn)
            return True
        except Exception as e:
            print('delete except   ', e.args)
            conn.rollback()
            self.close(cursor, conn)
            # self.conn.rollback()
            return False

    # 更新
    def update(self, sql='', param=()):
        # self.connected()
        try:
            # cur = self.conn.cursor()
            # self.db.getconn().execute(sql, param)
            cursor, conn = self.execute(sql, param)
            # self.db.conn.commit()
            self.close(cursor, conn)
            return True
        except Exception as e:
            print('update except   ', e.args)
            conn.rollback()
            self.close(cursor, conn)
            # self.conn.rollback()
            return False

    @classmethod
    def getInstance(self):
        if MysqlApi.mysql is None:
            MysqlApi.mysql = MysqlApi()
        return MysqlApi.mysql

    # 执行命令
    def execute(self, sql='', param=(), autoclose=False):
        cursor, conn = self.db.getConn()
        try:
            if param:
                cursor.execute(sql, param)
            else:
                cursor.execute(sql)
            conn.commit()
            if autoclose:
                self.close(cursor, conn)
        except Exception as e:
            pass
        return cursor, conn

    # 执行多条命令
    '[{"sql":"xxx","param":"xx"}....]'

    def executemany(self, list=[]):
        cursor, conn = self.db.getconn()
        try:
            for order in list:
                sql = order['sql']
                param = order['param']
                if param:
                    cursor.execute(sql, param)
                else:
                    cursor.execute(sql)
            conn.commit()
            self.close(cursor, conn)
            return True
        except Exception as e:
            print('execute failed========', e.args)
            conn.rollback()
            self.close(cursor, conn)
            return False

    # def connect(self):
    #     self.conn = MySQLdb.connect(user='root', db='asterisk', passwd='kalamodo', host='192.168.88.6')

    def close(self, cursor, conn):
        cursor.close()
        conn.close()
        print("PT连接池释放con和cursor")
