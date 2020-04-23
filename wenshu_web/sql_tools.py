# -*- coding: utf-8 -*-

import pymongo
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError
import traceback


class WenShuPipeline(object):

    def __init__(self):
        self.connection = pymongo.MongoClient('*', port, connect=False)
        # self.connection.admin.authenticate('andrew', 'wjzj1217@')
        db = self.connection['wenshu']
        db.authenticate('username', 'password')
        self.collection1 = db['wenshu']
        self.collection1.create_index([("docid", DESCENDING)], unique=True)

    def process_item(self, item):

        # item = dict(item)
        try:
            self.collection1.insert_one(item)
            print('----数据插入成功！---')
        except DuplicateKeyError as e:

            print(f'该条数据已插入，直接跳过')
            print('---------------------------')
        except Exception as e:
            print('出现其他异常！')
            print(traceback.format_exc())
            print(item)



