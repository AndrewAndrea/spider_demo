# -*- coding: utf-8 -*-

from scrapy import cmdline

# 将运行的log信息全部打印到all.log文件
cmdline.execute("scrapy crawl area".split())


