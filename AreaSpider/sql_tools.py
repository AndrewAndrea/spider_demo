# -*- coding: utf-8 -*-
import pymysql


class ConnectMysql(object):
    """
    存储数据
    """

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',
            db='dragonfly_inn',
            user='root',
            passwd='12345678',
            # charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def insert_data(self, data):
        # SQL 插入语句
        sql = "INSERT INTO area(pid, district, level) \
               VALUES (%s,%s,%s)"
        # 区别与单条插入数据，VALUES ('%s', '%s',  %s,  '%s', %s) 里面不用引号

        # val = (('li', 'si', 16, 'F', 1000),
        #        ('Bruse', 'Jerry', 30, 'F', 3000),
        #        ('Lee', 'Tomcat', 40, 'M', 4000),
        #        ('zhang', 'san', 18, 'M', 1500))
        try:
            # 执行sql语句
            self.cursor.execute(sql, data)
            new_id = self.cursor.lastrowid
            # 提交到数据库执行
            self.connect.commit()
            return new_id
        except:
            # 如果发生错误则回滚
            self.connect.rollback()


