#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/3/6 11:22 
# @Author : zhao.jia
# @Site :  
# @File : demo_01.py 
# @Software: PyCharm

import requests
import tools
import execjs
import time
from lxml import etree


class FaceBook:
    def __init__(self):
        self.sess = requests.session()
        self.tabid = None
        self.generate_tabid()

    def generate_tabid(self):
        tabid = execjs.compile(open('_s_de.js', 'r', encoding='utf8').read()).call('o')
        self.tabid = tabid

    def generate_session(self):
        session = execjs.compile(open('_s_de.js', 'r', encoding='utf8').read()).call('o')
        a = execjs.compile(open('_s_de.js', 'r', encoding='utf8').read()).call('o')
        return session, a

    def get_page_id(self):
        url = "https://www.facebook.com/leomessi/"
        headers = """
            accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            accept-language: zh-CN,zh;q=0.9
            accept-encoding: gzip, deflate, br
            cache-control: max-age=0
            cookie: sb=iJ9gXuHDHH2fTW3VYna3vza8; datr=iJ9gXtM74wyDV-bxRR3aLnKr; fr=1ZkrhY0BFD4V5u2ST..BeYJ-I.e1.AAA.0.0.BeYcCL.AWV6qPcC; wd=1366x468
            referer: https://www.facebook.com/directory/pages/
            sec-fetch-dest: document
            sec-fetch-mode: navigate
            sec-fetch-site: same-origin
            sec-fetch-user: ?1
            upgrade-insecure-requests: 1
            user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36
        """
        # res = self.sess.get(url, headers=tools.headers_to_dict(headers), verify=False)
        # if res.status_code == 200:
        with open('facebook.html', 'r', encoding='utf8') as f:
            res_data = f.read()
        # client_revision就是__rev
        client_revision = res_data.split('client_revision":')[1].split(',', 1)[0].strip()
        hsi = res_data.split('hsi":')[1].split(',', 1)[0].strip()
        print(client_revision, hsi)
        res_html = etree.HTML(res_data)
        page_url = res_html.xpath('//a[@rel="ajaxify"]/@ajaxify')[0]
        page_url = f"https://www.facebook.com{page_url}"
        self.get_data(url=page_url, client_revision=client_revision, hsi=hsi)

    def get_data(self, url, client_revision, hsi):
        headers = """
            accept: */*
            accept-encoding: gzip, deflate, br
            accept-language: zh-CN,zh;q=0.9
            cookie: sb=iJ9gXuHDHH2fTW3VYna3vza8; datr=iJ9gXtM74wyDV-bxRR3aLnKr; _fbp=fb.1.1583466685447.274526643; locale=zh_CN; fr=1ZkrhY0BFD4V5u2ST..BeYJ-I.e1.AAA.0.0.BeYvy5.AWVFv6_P; wd=1366x150
            referer: https://www.facebook.com/leomessi/
            sec-fetch-dest: empty
            sec-fetch-mode: cors
            sec-fetch-site: same-origin
            user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
        """

        session, a = self.generate_session()
        # url = 'https://www.facebook.com/pages_reaction_units/more/?referrer&fb_dtsg_ag&__user=0&__a=1&__dyn=7AgNe5Gmawgrolg9odoyGzEy4QjFwn8S2Sq5UO5U4e1qzEjyQdxK5WAx-bxWUW16whoS2S4ogU9A3mcw8258e8hwj82oG7Elw86l0DwLwxw-KEdEnwho4a11zU4K1dx278-0CUrx62WUry8465o-cBKm1UwiE9E4aawDKi8wGwFyFE-1kwOwnolwBgK7o88vwlo2kwLwKG2q4U2IzUuxy5po5e1dw&__csr=&__req=b&__beoa=0&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001802011&__s=yjxmip%3Av22nxa%3Adsen9l&__hsi=6801018320680499016-0&__comet_req=0&__spin_r=1001802011&__spin_b=trunk&__spin_t=1583485473'
        from_data = {
            # "page_id": page_id,
            #             # "cursor": {"card_id": "videos", "has_next_page": True},  #  page_posts_card
            #             # "surface": "www_pages_home",
            #             # "unit_count": "8",
            #             # "referrer": "",
            "fb_dtsg_ag": "",
            "__user": "0",
            "__a": "1",
            "__dyn": "",
            "__csr": "",
            "__req": "b",  # 翻页时该值为b，进入用户首页时该值为2
            "__beoa": "0",
            "__pc": "PHASED:DEFAULT",   # 进入用户主页时可以获取到该参数
            "dpr": "1",
            "__rev": client_revision,   # 进入用户主页时可以获取到该参数
            "__s": f"{a}:{self.tabid}:{session}",
            "__hsi": hsi,  # 进入用户主页时可以获取到该参数
            "__comet_req": "0",
            "__spin_r": client_revision,   # 进入用户主页时可以获取到该参数
            "__spin_b": "trunk",
            "__spin_t": str(int(time.time())),  # 时间戳
        }
        res = self.sess.post(url=url, params=from_data, headers=tools.headers_to_dict(headers))
        print(res.text)

if __name__ == '__main__':
    FaceBook().get_page_id()





















































