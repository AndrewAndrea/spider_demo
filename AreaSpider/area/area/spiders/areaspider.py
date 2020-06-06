# -*- coding: utf-8 -*-
import time
import traceback
from scrapy import FormRequest
from scrapy_redis import spiders
from lxml import etree
from area.items import AreaItem


class AreaSpider(spiders.RedisSpider):

    name = "area"

    redis_key = 'area:start_urls'

    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html'

    host = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019"

    item = AreaItem()

    def parse(self, response):
        res_html = None
        try:
            res_html = etree.HTML(response.body.decode('gbk'))
        except Exception as e:
            print(e)
            print(response.body)
        if res_html is None:
            time.sleep(15)
            FormRequest(url=response.url, callback=self.parse)
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
            self.item['district_id'] = province_url[0].split('.')[0]
            self.item['parent_id'] = 0
            self.item['district_name'] = province_name[0]
            self.item['level'] = 1
            # yield self.item
            province_url_list_app((province_url[0], province_url[0].split('.')[0]))

            # parent_id = self.db.insert_data((new_id, province_name[0], 1))
        for province in province_url_list:
            yield FormRequest(url=f'{self.host}/{province[0]}', meta={'parent_id': province[1]},
                              callback=self.parse_city)

    def parse_city(self, response):
        print(response.url, '解析城市数据++++++++++')
        parent_id = response.meta.get('parent_id')
        res_html = None
        try:
            res_html = etree.HTML(response.body.decode('gbk'))
        except Exception as e:
            print(e)
            print(response.body)
            time.sleep(15)
            # self.get_citys(p_url, parent_id)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_city)
        if res_html is None:
            time.sleep(15)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_city)
        # res_html = etree.HTML(res.content.decode('gbk'))
        try:
            city_list = res_html.xpath('//tr[@class="citytr"]/td[2]')
            city_code = res_html.xpath('//tr[@class="citytr"]/td[1]')
        except:
            print('结束市抓取')
            return
        city_url_list = []
        city_url_list_app = city_url_list.append
        for i in range(len(city_list)):
            city_name_str = city_list[i].xpath('./a/text()')
            city_url_str = city_list[i].xpath('./a/@href')
            city_code_str = city_code[i].xpath('./a/text()')
            if not city_name_str and not city_url_str and not city_code_str:
                continue
            self.item['district_id'] = city_code_str[0]
            self.item['parent_id'] = parent_id
            self.item['district_name'] = city_name_str[0]
            self.item['level'] = 2
            # yield self.item
            city_url_list_app((city_url_str[0], city_code_str[0]))

        for city in city_url_list:
            yield FormRequest(url=f'{self.host}/{city[0]}', meta={'parent_id': city[1],
                                                                  'c_code': city[0].split('/')[0]},
                              callback=self.parse_area)

    def parse_area(self, response):
        print(response.url, '解析区数据++++++++++')
        parent_id = response.meta.get('parent_id')
        c_code = response.meta.get('c_code')

        res_html = None
        try:
            res_html = etree.HTML(response.body.decode('gbk'))
        except Exception as e:
            print(e)
            print(response.body)
            time.sleep(15)
            # self.get_citys(p_url, parent_id)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_area)
        if res_html is None:
            time.sleep(15)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_area)
        # res_html = etree.HTML(res.content.decode('gbk'))
        try:
            county_list = res_html.xpath('//tr[@class="countytr"]/td[2]')
            county_code = res_html.xpath('//tr[@class="countytr"]/td[1]')
        except:
            print('结束市抓取')
            return
        county_url_list = []
        county_url_list_app = county_url_list.append
        for i in range(len(county_list)):
            city_name_str = county_list[i].xpath('./a/text()')
            city_url_str = county_list[i].xpath('./a/@href')
            city_code_str = county_code[i].xpath('./a/text()')
            if not city_name_str and not city_url_str and not city_code_str:
                continue
            self.item['district_id'] = city_code_str
            self.item['parent_id'] = parent_id
            self.item['district_name'] = city_name_str
            self.item['level'] = 3
            # yield self.item
            county_url_list_app((city_url_str[0], city_code_str[0]))

        for city in county_url_list:
            yield FormRequest(url=f'{self.host}/{c_code}/{city[0]}', meta={'parent_id': city[1], 'c_code': c_code,
                                                                           "a_code": city[0].split('/')[0]},
                              callback=self.parse_strees)

    def parse_strees(self, response):
        print(response.url, '解析街道数据++++++++++')
        parent_id = response.meta.get('parent_id')
        c_code = response.meta.get('c_code')
        a_code = response.meta.get('a_code')

        res_html = None
        try:
            res_html = etree.HTML(response.body.decode('gbk'))
        except Exception as e:
            print(e)
            print(response.body)
            time.sleep(15)
            # self.get_citys(p_url, parent_id)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_strees)
        if res_html is None:
            time.sleep(15)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_strees)
        # res_html = etree.HTML(res.content.decode('gbk'))
        try:
            county_list = res_html.xpath('//tr[@class="towntr"]/td[2]')
            county_code = res_html.xpath('//tr[@class="towntr"]/td[1]')
        except:
            print('结束街道抓取')
            return
        county_url_list = []
        county_url_list_app = county_url_list.append
        for i in range(len(county_list)):
            city_name_str = county_list[i].xpath('./a/text()')
            city_url_str = county_list[i].xpath('./a/@href')
            city_code_str = county_code[i].xpath('./a/text()')
            if not city_name_str and not city_url_str and not city_code_str:
                continue
            self.item['district_id'] = city_code_str[0]
            self.item['parent_id'] = parent_id
            self.item['district_name'] = city_name_str[0]
            self.item['level'] = 4
            # yield self.item
            county_url_list_app((city_url_str[0], city_code_str[0], a_code))

        for city in county_url_list:
            yield FormRequest(url=f'{self.host}/{c_code}/{a_code}/{city[0]}', meta={'parent_id': city[1]},
                              callback=self.parse_village)

    def parse_village(self, response):
        print(response.url, '解析村庄数据++++++++++')
        parent_id = response.meta.get('parent_id')
        res_html = None
        try:
            res_html = etree.HTML(response.body.decode('gbk'))
        except Exception as e:
            print(e)
            print(response.body)
            time.sleep(15)
            # self.get_citys(p_url, parent_id)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_village)

        if res_html is None:
            time.sleep(15)
            FormRequest(url=response.url, meta={'parent_id': parent_id}, callback=self.parse_village)
        # res_html = etree.HTML(res.content.decode('gbk'))
        try:

            county_list = res_html.xpath('//tr[@class="villagetr"]/td[3]')
            county_code = res_html.xpath('//tr[@class="villagetr"]/td[1]')
        except:
            print('结束村级抓取')
            return
        # county_url_list = []
        # county_url_list_app = county_url_list.append

        for i in range(len(county_list)):
            city_name = county_list[i].xpath('./text()')
            # city_url_str = county_list[i].xpath('./a/@href')
            city_code_str = county_code[i].xpath('./text()')
            if not city_name and not city_code_str:
                continue
            city_name_str = city_name[0]
            if "居委会" in city_name[0]:
                city_name_str = city_name[0].split('居委会')[0]
            if "村委会" in city_name[0]:
                city_name_str = city_name[0].split('委会')[0]
            if "居民委员会" in city_name[0]:
                city_name_str = city_name[0].split('居民委员会')[0]
            if "村村委会" in city_name[0]:
                city_name_str = city_name[0].split('村委会')[0]
            if "村民委员会" in city_name[0]:
                city_name_str = city_name[0].split('村民委员会')[0]
            if "拟居委会" in city_name[0]:
                city_name_str = city_name[0].split('拟居委会')[0]
            self.item['district_id'] = city_code_str[0]
            self.item['parent_id'] = parent_id
            self.item['district_name'] = city_name_str
            self.item['level'] = 5
            # yield self.item

        #     county_url_list_app((city_url_str, city_code_str))
        #
        # for city in county_url_list:
        #     FormRequest(url=f'{self.host}/{parent_id}/{city[0]}', meta={'parent_id': city[1]},
        #                 callback=self.parse_strees)

