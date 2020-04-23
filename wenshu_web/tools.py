#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/8/6 16:16 
# @Author : Andrew
# @Site :  
# @File : tools.py 
# @Software: PyCharm

import time


def headers_to_dict(headers):
    row_headear = headers.split('\n')
    row_dict = dict()
    for i in row_headear:
        if i == '':
            continue
        row = i.strip().split(':', 1)
        if len(row) == 0:
            continue
        if row[0] == '':
            continue
        row_dict[row[0].strip()] = row[1].strip()
    return row_dict


def cookie_to_dict(cookies):
    row_cookie = cookies.split(';')
    row_dict = dict()
    for i in row_cookie:
        if i == '':
            continue
        row = i.strip().split('=', 1)
        row_dict[row[0].strip()] = row[1].strip()
    return row_dict


def get_stamp():
    """
    获取毫秒级时间戳
    :return:
    """
    stamp_time = int((time.time()) * 1000)
    return stamp_time


def get_s_stamp():
    """
    获取秒级时间戳
    :return:
    """
    stamp_time = int((time.time()) * 1000)
    return stamp_time


def stamp_to_time(stamp_time):
    """
    时间戳转时间
    :return:
    """
    timeArray = time.localtime(stamp_time/1000)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def unix_time(dt):
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    timestamp = int(time.mktime(timeArray))
    return timestamp