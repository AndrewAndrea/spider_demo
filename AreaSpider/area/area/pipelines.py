# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class AreaPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host='127.0.0.1',
            db='name',
            user='root',
            passwd='12345678',
            # charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # SQL 插入语句
        sql = "INSERT INTO area(district_id, pid, district, level) \
               VALUES (%s,%s,%s, %s)"
        try:
            # 执行sql语句

            self.cursor.execute(sql, (item['district_id'], item['parent_id'], item['district_name'], item['level']))
            self.connect.commit()

        except Exception as e:
            # 如果发生错误则回滚
            self.connect.rollback()

        return item

