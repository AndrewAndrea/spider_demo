# -*- coding: utf-8 -*-
import random

import requests
import time
import uuid
import base64
import json
import tools
import execjs
import pyDes

import arrow
from des_3 import TripleDesUtils
from des3_demo2 import prpcrypt
from sql_tools import WenShuPipeline
from my_log_test import MyLogger


logger = MyLogger(name="wenshu_spider", level="INFO").add_log_file()


logger.catch(reraise=True)
class WenShu:

    def __init__(self):

        self.session = requests.session()
        self.base_url = 'http://wenshuapp.court.gov.cn/appinterface/rest.q4w'
        headers = """
                    User-Agent:Dalvik/2.1.0 (Linux; U; Android 5.1.1; vivo x5m Build/LMY49I)
                    Host:wenshuapp.court.gov.cn
                    Accept-Encoding:gzip
                    Content-Type:application/x-www-form-urlencoded
                    Connection:keep-alive
                """
        self.session.headers = tools.headers_to_dict(headers)
        
        self.page_num = 1
        self.cprqStart = "2002-01-02"
        self.cprqend = "2002-06-01"
        # 文书类型
        self.s6 = "01"
        # 案由
        self.s11 = 1
        # 法院层级  4为基层
        self.s4 = 1
        # 审判程序
        self.s8 = '02'
        self.s33 = '北京市'
        self.queryCondition = [
            {"key": "cprqEnd", "value": self.cprqend},
            {"key": "cprqStart", "value": self.cprqStart}
        ]
        # self.result_flag = 1  # 等于1时，条件为初始条件，条件改变一次增加1
        # 关键字
        self.key_word = None
        # 案由
        self.causes = None
        # 地域及法院
        self.case_province = None
        # 法院层级
        self.court_hierarchy = None
        # 裁判年份
        self.referee_year = None
        # 审判程序
        self.trial_procedure = None
        # 时间间隔暂定为180天，如果所有添加增加完毕，查询出来的结果还是多余1000，增缩小时间间隔
        self.time_days = 180
        """
        [
                    {"key": "s45", "value": "合同"},
                    {"key": "s11", "value": "1"},
                    {"key": "s4", "value": "2"},
                    {"key": "cprqEnd", "value": "2008-04-14"},
                    {"key": "cprqStart", "value": "1996-01-01"}
                ]
        """

    def set_id(self):
        id = time.strftime("%Y%m%d%H%M%S",  time.localtime())
        return id

    def set_devid(self):
        devid = str(uuid.uuid4()).replace('-', '')
        return devid

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

    # 获取__RequestVerificationToken参数
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

    def get_count_data(self):
        """
        yyyyMMddHHmmss
        :return:
        """
        from_data = {
            'id': self.set_id(),
            'command': 'wsCountSearch',
            'params': {
                'app': 'cpws',
                'devtype': '1',
                'devid': self.set_devid(),
            }
        }

        request = {
            "request": str(base64.b64encode(json.dumps(from_data).encode("utf-8")), 'utf8')  # 将字符为unicode编码转换为utf-8编码
        }

        res = self.session.post(url=self.base_url, data=request)
        print(res.json())
        if res.status_code == 200:
            r_json = res.json()
            # 今日新增
            WsCountVo = r_json.get('data').get('WsCountVo')
            # 访问总量
            sum_visitor_count = WsCountVo.get('WZ_Z_zfwl')
            # 行政带T的是今天的
            xingzheng_t = WsCountVo.get('WS_T_txzaj')

            WS_T_tqtaj = WsCountVo.get('WS_T_tqtaj')
            # 民事今日新增
            WS_T_tmsaj = WsCountVo.get('WS_T_tmsaj')
            # 赔偿
            WS_C_pcaj = WsCountVo.get('WS_C_pcaj')
            # 赔偿今日新增
            WS_T_pcaj = WsCountVo.get('WS_T_pcaj')
            # 行政
            WS_C_xzaj = WsCountVo.get('WS_C_xzaj')
            # 文书总量
            WS_C_aj = WsCountVo.get('WS_C_aj')
            # 执行今日新增
            WS_T_tzxaj = WsCountVo.get('WS_T_tzxaj')
            curDate = WsCountVo.get('curDate')
            # 刑事
            WS_C_xsaj = WsCountVo.get('WS_C_xsaj')
            # 今日新增
            WS_T_taj = WsCountVo.get('WS_T_taj')
            # 民事
            WS_C_msaj = WsCountVo.get('WS_C_msaj')

            WS_C_qtaj = WsCountVo.get('WS_C_qtaj')
            # 刑事今日新增
            WS_T_txsaj = WsCountVo.get('WS_T_txsaj')
            # 执行
            WS_C_zxaj = WsCountVo.get('WS_C_zxaj')

    def get_wenshu_list(self):
        from_data = self.return_from_data
        logger.info(f'-------------------本次查询条件{from_data}--------------------------')
        request = {
            "request": str(base64.b64encode(json.dumps(from_data).encode("utf-8")), 'utf8')  # 将字符为unicode编码转换为utf-8编码
        }
        res = self.session.post(url=self.base_url, data=request)
        r_json = res.json()
        data = r_json.get('data')
        secretKey = data.get('secretKey')
        content = data.get('content')
        with open("cipher.js", 'r', encoding='utf-8') as f:
            js = f.read()
        ctx = execjs.compile(js)
        iv = ctx.call("cipher")
        result_d = prpcrypt(key=secretKey, IV=iv).decrypt(content)
        self.parse_data_list(result_d) == "0":

    def parse_data_list(self, result_d):
        result_dict = json.loads(result_d)
        query_result = result_dict.get('queryResult')
        query_result_list = query_result.get('resultList')
        resultCount = query_result.get('resultCount')
        print(resultCount, '总数量')
        logger.info(f'-------------------查询结果，总共查询到{resultCount}条--------------------------')
        if resultCount:
            logger.info(f'-------------------查询结果得到的列表长度{len(query_result_list)}--------------------------')
            for query_result in query_result_list:
                docid = query_result.get('rowkey')
                print(docid)
                title = query_result.get('1')
                fayuan = query_result.get('2')
                jianjie = query_result.get('26')
                anhao = query_result.get('7')
                # 发布日期
                uploaddate = query_result.get('31')
                self.get_wenshu_detail(docid)
            if len(query_result_list) < 50:
                return "0"
        else:
            logger.info(f'-------------------{result_dict}查询出来的列表数量显示为0，停止查询。。。--------------------------')

            return "0"

    def get_wenshu_detail(self, docid):
        from_data = {
            'id': self.set_id(),
            'command': 'docInfoSearch',
            'params': {
                'ciphertext': self.get_cipher_3_test(),
                'devtype': "1",
                'devid': self.set_devid(),
                'docId': docid,
            }
        }
        request = {
            "request": str(base64.b64encode(json.dumps(from_data).encode("utf-8")), 'utf8')  # 将字符为unicode编码转换为utf-8编码
        }
        res = self.session.post(url=self.base_url, data=request)
        if res.status_code == 200:
            r_json = res.json()
            data = r_json.get('data')
            secretKey = data.get('secretKey')
            content = data.get('content')
            if content:
                with open("cipher.js", 'r', encoding='utf-8') as f:
                    js = f.read()
                ctx = execjs.compile(js)
                iv = ctx.call("cipher")
                result_d = prpcrypt(key=secretKey, IV=iv).decrypt(content)
                docinfo = json.loads(result_d).get('DocInfoVo')
                # 查看次数
                view_count = docinfo.get('viewCount')
                # 文书详情
                qwContent = docinfo.get('qwContent')
            else:
                print('返回的内容为空，直接跳过')
                logger.error(f'响应的数据{res.json()} -- 返回的内容为空，直接跳过')


    def return_from_data(self):
        from_data = {
            'id': self.set_id(),
            'command': 'queryDoc',
            'params': {
                'pageNum': self.page_num,
                'sortFields': "s50:desc",
                'ciphertext': self.get_cipher_3_test(),
                'devtype': "1",
                'devid': self.set_devid(),
                'pageSize': '20',
                'queryCondition': self.queryCondition
            }
        }
        return from_data


    def return_wenshu_type(self):
        if self.s6 == 1:
            wenshu_type = "判决书"
        elif self.s6 == 2:
            wenshu_type = "裁定书"
        elif self.s6 == 3:
            wenshu_type = "调解书"
        elif self.s6 == 4:
            wenshu_type = "决定书"
        elif self.s6 == 5:
            wenshu_type = "通知书"
        elif self.s6 == 9:
            wenshu_type = "令"
        elif self.s6 == 10:
            wenshu_type = "其他"
        else:
            wenshu_type = "未知"
        return wenshu_type


if __name__ == '__main__':

    WenShu().get_wenshu_list()



