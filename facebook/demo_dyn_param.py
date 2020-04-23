#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/6 16:25 
# @Author : zhao.jia
# @Site :  
# @File : demo_dyn_param.py 
# @Software: PyCharm

import execjs

content = execjs.compile(open('_dyn_de.js', 'r', encoding='utf8').read()).call('toCompressedString')
# localstory中的session
session_en = execjs.compile(open('_s_de.js', 'r', encoding='utf8').read()).call('o')
# print(content)
print(session_en)