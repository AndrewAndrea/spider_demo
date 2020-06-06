# -*- coding: utf-8 -*-

import requests
import time
from lxml import etree
import tools
from sql_tools import ConnectMysql


class AreaSpider:

    def __init__(self):
        self.session = requests.session()
        headers = """
            Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
            Accept-Encoding: gzip, deflate
            Accept-Language: zh-CN,zh;q=0.9
            Connection: keep-alive
            Cookie: AD_RS_COOKIE=20080919
            Host: www.stats.gov.cn
            Pragma: no-cache
            Referer: http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html
            Upgrade-Insecure-Requests: 1
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36
        """
        self.session.headers = tools.headers_to_dict(headers)
        self.host = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'
        self.db = ConnectMysql()

    def get_province(self):
        new_id = self.db.insert_data((0, '中国', 0))
        res = self.session.get(f'{self.host}/index.html')
        res_html = etree.HTML(res.content.decode('gbk'))
        try:
            pro_list = res_html.xpath('//tr[@class="provincetr"]/td')
        except:
            return
        province_url_list = []
        province_url_list_app = province_url_list.append
        for pro in pro_list:
            province_name = pro.xpath('./a/text()')
            province_url = pro.xpath('./a/@href')
            if not province_name and not province_url:
                continue
            print('###################下级市##################')
            parent_id = self.db.insert_data((new_id, province_name[0], 1))
            province_url_list_app((province_url[0], parent_id))
        for province in province_url_list:
            self.get_citys(province[0], province[1])
            print('-------------------分割线------------------')

    def get_citys(self, p_url, parent_id):
        res = self.session.get(f'{self.host}/{p_url}')
        res_html = None
        try:
            res_html = etree.HTML(res.content.decode('gbk'))
        except Exception as e:
            time.sleep(15)
            self.get_citys(p_url, parent_id)
        if res_html is None:
            time.sleep(15)
            self.get_citys(p_url, parent_id)
        # res_html = etree.HTML(res.content.decode('gbk'))
        try:
            city_list = res_html.xpath('//tr[@class="citytr"]/td[2]')
        except:
            return
        for city in city_list:
            city_name = city.xpath('./a/text()')
            city_url = city.xpath('./a/@href')
            if not city_name and not city_url:
                continue
            parent_c_id = self.db.insert_data((parent_id, city_name[0], 2))
            self.get_areas(city_url[0], parent_c_id)
            print('-------------------分割线------------------')
        return

    def get_areas(self, c_url, parent_c_id):
        c_code = c_url.split('/')[0]
        res = self.session.get(f'{self.host}/{c_url}')
        res_html = None
        try:
            res_html = etree.HTML(res.content.decode('gbk'))
        except Exception as e:
            time.sleep(15)
            self.get_areas(c_url, parent_c_id)
        # res_html = etree.HTML(res.content.decode('gbk'))
        if res_html is None:
            time.sleep(15)
            self.get_areas(c_url, parent_c_id)
        try:
            city_list = res_html.xpath('//tr[@class="countytr"]/td[2]')
        except:
            return
        for city in city_list:
            area_name = city.xpath('./a/text()')
            area_url = city.xpath('./a/@href')
            if not area_name and not area_url:
                continue
            parent_a_id = self.db.insert_data((parent_c_id, area_name[0], 3))
            self.get_strees(area_url[0], c_code, parent_a_id)
        return

    def get_strees(self, a_url, c_code, parent_a_id):
        a_code = a_url.split('/')[0]
        res = self.session.get(f'{self.host}/{c_code}/{a_url}')
        res_html = None
        try:
            res_html = etree.HTML(res.content.decode('gbk'))
        except Exception as e:
            time.sleep(15)
            self.get_strees(a_url, c_code, parent_a_id)
        # res_html = etree.HTML(res.content.decode('gbk'))
        if res_html is None:
            time.sleep(15)
            self.get_strees(a_url, c_code, parent_a_id)
        try:
            city_list = res_html.xpath('//tr[@class="towntr"]/td[2]')
        except:
            print('结束街道抓取')
            return
        for city in city_list:
            city_name = city.xpath('./a/text()')
            city_url = city.xpath('./a/@href')
            if not city_name and not city_url:
                continue
            parent_s_id = self.db.insert_data((parent_a_id, city_name[0], 4))
            self.get_village(t_url=city_url[0], c_code=c_code, a_code=a_code, parent_s_id=parent_s_id)
        return

    def get_village(self, t_url, c_code, a_code, parent_s_id):
        # s_code = t_url.split('/')[2]
        res = self.session.get(f'{self.host}/{c_code}/{a_code}/{t_url}')
        res_html = None
        try:
            res_html = etree.HTML(res.content.decode('gbk'))
        except Exception as e:
            time.sleep(15)
            self.get_village(t_url, c_code, a_code, parent_s_id)
        if res_html is None:
            time.sleep(15)
            self.get_village(t_url, c_code, a_code, parent_s_id)
        try:
            city_list = res_html.xpath('//tr[@class="villagetr"]/td[3]')
        except Exception as e:
            print('结束！！！')
            # print(time.sleep(30))
            return
        for city in city_list:
            city_name = city.xpath('./text()')
            if not city_name:
                continue
            self.db.insert_data((parent_s_id, city_name[0], 5))
        return


if __name__ == '__main__':
    AreaSpider().get_province()


