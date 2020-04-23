#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/5/28 10:54 
# @Author : zhao.jia
# @Site :  
# @File : tools.py 
# @Software: PyCharm

import time


def headers_to_dict(headers):
    row_headear = headers.split('\n')
    row_dict = dict()
    # headers_list = []
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
    cookie_list = []
    row_cookie = cookies.split(';')
    for i in row_cookie:
        if i == '':
            continue
        row = i.strip().split('=', 1)

        row_dict = {row[0].strip(), row[1].strip()}
        cookie_list.append(row_dict)
    print(dict(cookie_list))


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
    timeArray = time.localtime(stamp_time)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    return otherStyleTime