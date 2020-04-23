# -*- coding: utf-8 -*-
import json
import os
import random
import uuid
import traceback
import execjs
import requests
import time
import arrow
import datetime

from des3_demo2 import prpcrypt
import tools
from sql_tools import WenShuPipeline
from my_log_test import MyLogger

logger = MyLogger(name="wenshu_spider", level="INFO").add_log_file()


logger.catch(reraise=True)
class Wenshu:

    def __init__(self):
        self.session = requests.session()
        self.page_num = 12
        self.cprqstart = "2006-05-24"
        self.cprqend = "2006-06-12"
        self.add_days = 20
        self.doc_id_list = []
        self.code_cookies = None

    def set_id(self):
        id = time.strftime("%Y%m%d%H%M%S",  time.localtime())
        return id

    def get_token(self):
        js = """ function random(size){
                	var str = "",
                	arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
                	for(var i=0; i<size; i++){
                		str += arr[Math.round(Math.random() * (arr.length-1))];
                	}
                	return str;
                }
        """
        ctx = execjs.compile(js)
        result = ctx.call("random", "24")
        return result

    def get_cipher_3_test(self):
        with open("cipher.js", 'r', encoding='utf-8') as f:
            js = f.read()
        ctx = execjs.compile(js)
        salt = self.get_token()
        iv = ctx.call("cipher")
        result_d = prpcrypt(key=salt, IV=iv).encrypt(str(int(time.time() * 1000)))

        # result_d = DesObj.encryption(str(int(time.time() * 1000)))
        str_en_to = salt + iv + str(result_d)
        resutlt = ctx.call('return_result', str_en_to)

        return resutlt

    def set_devid(self):
        devid = str(uuid.uuid4()).replace('-', '')
        return devid

    def request_data(self):
        # while True:
        #     print(q.empty())
        #     if not q.empty():
        #         item = q.get()
        #         url = item[0]
        #         cookie = item[1]
        retry = 1
        while True:
            url, cookie = self.get_url_cookie()
            if url and cookie:
                from_data = {
                    'pageNum': self.page_num,
                    'sortFields': "s50:desc",
                    'ciphertext': self.get_cipher_3_test(),
                    'pageId': self.set_devid(),
                    'pageSize': 20,
                    's8': '02',
                    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
                    '__RequestVerificationToken': self.get_token(),
                    'queryCondition': json.dumps([{"key": "cprq", "value": f"{self.cprqstart} TO {self.cprqend}"}])
                }
                logger.info(f'-------改变后的查询条件{from_data}')
                headers = """
                    Accept: application/json, text/javascript, */*; q=0.01
                    Accept-Encoding: gzip, deflate
                    Accept-Language: zh-CN,zh;q=0.9
                    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
                    Host: wenshu.court.gov.cn
                    Origin: http://wenshu.court.gov.cn
                    Proxy-Connection: keep-alive
                    Referer: http://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html
                    User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
                    X-Requested-With: XMLHttpRequest
                """
                try:
                    res = self.session.post(url, headers=tools.headers_to_dict(headers), data=from_data,
                                            cookies=cookie, timeout=(5, 30))
                except Exception as e:
                    print('请求出现列表异常。。。异常原因：')
                    print(traceback.format_exc())
                    time.sleep(60)
                    continue
                print("请求列表的响应状态码：", res.status_code)
                if res.status_code == 200:
                    try:
                        r_json = res.json()
                    except:
                        logger.error(traceback.format_exc())
                        if 'waf_captcha' in res.text:
                            check_result = self.input_check_image
                            if check_result:
                                continue
                        continue
                    # data = r_json.get('data')
                    secretKey = r_json.get('secretKey')
                    content = r_json.get('result')
                    # if
                    with open("cipher.js", 'r', encoding='utf-8') as f:
                        js = f.read()
                    ctx = execjs.compile(js)
                    iv = ctx.call("cipher")
                    result_d = prpcrypt(key=secretKey, IV=iv).decrypt(content)
                    result_dict = json.loads(result_d)
                    query_result = result_dict.get('queryResult')
                    query_result_list = query_result.get('resultList')
                    resultCount = query_result.get('resultCount')
                    if int(resultCount) > 600 and self.add_days == 1:
                        logger.info(f'----需要增加新的条件，爬虫暂停，当前查询条件{from_data}-{self.add_days}')
                        return False
                    if resultCount:
                        for query_result in query_result_list:
                            docid = query_result.get('rowkey')
                            print(docid)
                            title = query_result.get('1')
                            fayuan = query_result.get('2')
                            jianjie = query_result.get('26')
                            anhao = query_result.get('7')
                            # 发布日期
                            uploaddate = query_result.get('31')
                            wenshu_dict = {
                                'docid': docid,
                                'title': title,
                                'fayuan': fayuan,
                                'jianjie': jianjie,
                                'anhao': anhao,
                                'uploaddate': uploaddate
                            }

                            result = self.get_wenshu_detail(docid, wenshu_dict, iv)
                            if result:
                                pass
                            else:
                                return

                        self.page_num += 1
                        print(f'翻页到------{self.page_num}')
                        if len(query_result_list) < 20:
                            end_time = arrow.get(self.cprqend)
                            self.cprqend = end_time.shift(days=+self.add_days).format('YYYY-MM-DD')
                            self.cprqstart = end_time.shift(days=+1).format('YYYY-MM-DD')
                            self.page_num = 1
                            logger.error(f'-------当前查询数量小于60 ，改变查询条件{from_data}')
                        if int(resultCount) > 600:
                            self.add_days -= 10
                            if self.add_days < 1:
                                self.add_days = 1
                            end_time = arrow.get(self.cprqend)
                            self.cprqend = end_time.shift(days=-self.add_days).format('YYYY-MM-DD')
                            # self.cprqstart = end_time.shift(days=+1).format('YYYY-MM-DD')
                            logger.error(f'-------当前查询结果大于600 ，改变查询条件{from_data}')
                            self.page_num = 1
                            continue

                        # self.request_data()
                    if resultCount == 0:
                        logger.info(f'-------当前查询数量为0 ，改变查询条件{from_data}')
                        end_time = arrow.get(self.cprqend)
                        self.cprqend = end_time.shift(days=+self.add_days).format('YYYY-MM-DD')
                        self.cprqstart = end_time.shift(days=+1).format('YYYY-MM-DD')

                elif res.status_code in [502, 500, 504]:
                    time.sleep(60)
                    print('响应状态码502，暂停一分钟后继续抓取。。。')
                elif res.status_code == 400:
                    print('响应的状态码为400：跳过')
                    continue
                else:
                    print(f'{res.status_code}, 请求参数{from_data}, 响应内容{res.text}')
                    logger.error(f'请求列表--{res.status_code}, 请求参数{from_data}, 响应内容{res.text}')
                    return False
                time.sleep(1)
            else:
                print('没有数据。。。')
                time.sleep(1)

    def get_wenshu_detail(self, docid, wenshu_dict, iv):
        headers = f"""
            Accept: application/json, text/javascript, */*; q=0.01
            Accept-Encoding: gzip, deflate
            Accept-Language: zh-CN,zh;q=0.9
            Content-Type: application/x-www-form-urlencoded; charset=UTF-8
            Host: wenshu.court.gov.cn
            Origin: http://wenshu.court.gov.cn
            Proxy-Connection: keep-alive
            Pragma: no-cache
            Referer: http://wenshu.court.gov.cn/website/wenshu/181029CR4M5A62CH/index.html?docId={docid}
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
            X-Requested-With: XMLHttpRequest
        """
        retry = 1
        while True:
            url, cookie = self.get_url_cookie()

            if url and cookie:
                from_data = {
                    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch',
                    'ciphertext': self.get_cipher_3_test(),
                    'docId': docid,
                    '__RequestVerificationToken': self.get_token()
                }
                try:
                    res = self.session.post(url=url, data=from_data, cookies=cookie, headers=tools.headers_to_dict(headers))
                except Exception as e:
                    print('detail请求出现详情异常。。。异常原因：')
                    print(traceback.format_exc())
                    time.sleep(60)
                    continue
                if res.status_code == 200:
                    try:
                        r_json = res.json()
                    except Exception as e:
                        logger.error(traceback.format_exc())
                        if 'waf_captcha' in res.text:
                            check_result = self.input_check_image
                            if check_result:
                                continue
                        continue
                    secretKey = r_json.get('secretKey')
                    content = r_json.get('result')
                    if content:
                        with open("cipher.js", 'r', encoding='utf-8') as f:
                            js = f.read()
                        ctx = execjs.compile(js)
                        iv = ctx.call("cipher")
                        result_d = prpcrypt(key=secretKey, IV=iv).decrypt(content)
                        docinfo = json.loads(result_d)
                        # 查看次数
                        self.parse_detail(docinfo, wenshu_dict)
                        return True
                    else:
                        print('返回的内容为空，直接跳过')
                        logger.error(f'响应的数据{res.json()} -- 返回的内容为空，直接跳过')
                elif res.status_code in [502, 500, 504]:
                    time.sleep(60)
                    print('响应状态码502，暂停一分钟后继续抓取。。。')
                elif res.status_code == 400:
                    print('响应的状态码为400：跳过')
                    continue
                else:
                    print(f'{res.status_code}, 请求参数{from_data}, 响应内容{res.text}')
                    logger.error(f'请求详细信息--{res.status_code}, 请求参数{from_data}, 响应内容{res.text}')
                    return False

            else:
                print('当前没有数据等待')
                time.sleep(1)

    def parse_detail(self, docinfo, wenshu_dict):
        wenshu_dict['view_count'] = docinfo.get('viewCount')
        # 标题
        wenshu_dict['s1'] = docinfo.get('s1')
        # 法院
        wenshu_dict['s2'] = docinfo.get('s2')
        wenshu_dict['s3'] = docinfo.get('s3')
        wenshu_dict['s4'] = docinfo.get('s4')
        wenshu_dict['s5'] = docinfo.get('s5')
        wenshu_dict['s6'] = docinfo.get('s6')
        wenshu_dict['s7'] = docinfo.get('s7')
        wenshu_dict['s8'] = docinfo.get('s8')
        wenshu_dict['s9'] = docinfo.get('s9')
        wenshu_dict['s31'] = docinfo.get('s31')
        wenshu_dict['s41'] = docinfo.get('s41')
        wenshu_dict['s43'] = docinfo.get('s43')
        wenshu_dict['s22'] = docinfo.get('s22')
        wenshu_dict['s23'] = docinfo.get('s23')
        wenshu_dict['s25'] = docinfo.get('s25')
        wenshu_dict['s26'] = docinfo.get('s26')
        wenshu_dict['s27'] = docinfo.get('s27')
        wenshu_dict['s28'] = docinfo.get('s28')
        wenshu_dict['s17'] = docinfo.get('s17')
        wenshu_dict['s45'] = docinfo.get('s45')
        wenshu_dict['s11'] = docinfo.get('s11')
        wenshu_dict['wenshuAy'] = docinfo.get('wenshuAy')
        wenshu_dict['47'] = docinfo.get('s47')
        wenshu_dict['relWenshu'] = docinfo.get('relWenshu')
        wenshu_dict['globalNet'] = docinfo.get('globalNet')
        # s17 = docinfo.get('s17')
        # 文书详情
        wenshu_dict['qwContent'] = docinfo.get('qwContent')
        # wenshu_dict['wenshu_type'] = self.return_wenshu_type()
        WenShuPipeline().process_item(wenshu_dict)

    def get_url_cookie(self):
        try:
            res = self.session.get('http://*/get')
            if res.text and res.status_code != 503:
                if res.json().get('code') == 200:
                    url = res.json().get('url')
                    cookie = res.json().get('cookie')
                    return url, json.loads(cookie)
            return None, None
        except Exception as e:
            print(traceback.format_exc())
            return None, None

    def input_check_image(self):
        url = 'http://wenshu.court.gov.cn/waf_captcha/'
        headers = """
            Accept: image/webp,image/apng,image/*,*/*;q=0.8
            Accept-Encoding: gzip, deflate
            Accept-Language: zh-CN,zh;q=0.9
            Cache-Control: no-cache
            Connection: keep-alive
            Host: wenshu.court.gov.cn
            Pragma: no-cache
            Referer: http://wenshu.court.gov.cn/waf_verify.htm
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36
        """
        while True:
            request_url, cookie = self.get_url_cookie()
            if url and cookie:
                res = self.session.get(url=url, headers=tools.headers_to_dict(headers), cookies=cookie)
                if res.status_code == 200:
                    with open('input.png', 'wb') as f:
                        f.write(res.content)
                    logger.error('验证码以保存为input.png, 请输入验证码')
                    self.code_cookies = res.cookies.get_dict()
                    code = input('请输入验证码：')

                    code_url = f'http://wenshu.court.gov.cn/waf_verify.htm?captcha={code}'
                    self.code_cookies.update(cookie)
                    check_res = self.session.get(url=code_url, headers=tools.headers_to_dict(headers), cookies=self.code_cookies)
                    if check_res.status_code == 302:
                        self.code_cookies.update(check_res.cookies.get_dict())
                        return True





if __name__ == '__main__':

    Wenshu().request_data()
