#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/1 11:16 
# @Author : Andrew
# @Site :  
# @File : my_log_test.py 
# @Software: PyCharm
import os

from loguru import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logger.remove()


class MyLogger:

    def __init__(self, name, level, re_days="1 days"):
        self.name = name
        self.level = level
        self.re_days = re_days

    def add_log_file(self):
        logger.start(os.path.join(log_dir, self.name + '_{time:YYYY-MM-DD}.log'),
                     format="【{time:YYYY-MM-DD HH:mm:ss} | {level} | 】{message}", encoding='utf8',
                     backtrace=True, diagnose=True, rotation="00:00", level=self.level, retention=self.re_days,
                     filter=lambda record: record["extra"].get("name") == self.name)
        tp_logger = logger.bind(name=self.name)
        return tp_logger
