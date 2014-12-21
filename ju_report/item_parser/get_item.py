# -*-coding:utf-8-*-
import string
import time
from bs4 import BeautifulSoup
from utils.log import get_file_logger


def check_page(data_page):
    if not isinstance(data_page, unicode):
        return ''
    else:
        return data_page

class GetJuFloor(object):
    """获取unicode中的floor数据"""
    def __init__(self, page, brand_name):
        self.unicode_page = check_page(page)
        self.log = get_file_logger('ju_report')
        self.brand_name = brand_name

    def get_floors(self):
        try:
            if not self.unicode_page.strip():
                raise Exception(u'unicode_page为空')
            small_floors = {
                'urls' : [],
                'data' : [],
            }
            floors = {
                'big': '',
                'small': small_floors,
                'brand_name': self.brand_name,
            }
            soup_page = BeautifulSoup(self.unicode_page)
            i = 1
            while True:
                floor = soup_page.find(id="floor%i" % i)
                if floor:
                    data_url = floor.attrs.get('data-url', '')
                    if data_url:
                        floors['small']['urls'].append(data_url)
                        floors['small']['data'].append(floor)
                    else:
                        floors['big'] = floor
                    i = i + 1
                else:
                    break
        except Exception, e:
            self.log.error(e)
            return None
        return floors


class GetJuItem(object):
    """
    输入: 一个unicode的html页面或部分页面
    处理聚划算每个楼层的数据
    输出: 每个商品组成的item_list
    """

    def __init__(self, floor_data, brand_name):
        self.log = get_file_logger('ju_report')
        self.floor_data = floor_data
        self.brand_name = brand_name


    def get_big_items(self):
        try:
            if not self.floor_data:
                raise Exception(u'big floor_data为空')
        except Exception, e:
            self.log.error(e)
            return None

        result = []
        soup_li = self.floor_data.find_all('li')
        for i in soup_li:
            try:
                row = {
                    'name': '',
                    'desc': '',
                    'date_time': '',
                    'price': 0.0,
                    'discount': 0.0,
                    'orig_price': 0.0,
                    'sold_num': 0,
                    'str_people': u'',
                    'brand_name': '',
                    'item_type': u'热款',
                    'img_src': '',
                    'detail_src': '',
                }
                row['name'] = i.h4.string.strip()
                row['desc'] = i.h3.attrs.get('title', '')
                row['date_time'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                soup_price = i.find('span', 'price')
                row['price'] = string.atof(soup_price.em.string)
                row['orig_price'] = string.atof(string.atof(soup_price.find('del', 'oriPrice').string.encode('gbk', 'ignore')))
                row['discount'] = round(row['price']/row['orig_price'], 2)
                row['sold_num'] = string.atoi(i.find('div', 'soldcount').em.next)
                row['str_people'] = i.find('div', 'soldcount').em.next.next
                row['brand_name'] = self.brand_name
                row['item_type'] = u'热款'
                row['img_src'] = i.img.attrs.get('data-ks-lazyload', '')
                row['src_detail'] = i.a.attrs.get('href', '')
            except Exception, e:
                self.log.error(e)
                continue
            result.append(row)
        return result

    def get_small_items(self):
        result = []
        soup_small_page = BeautifulSoup(self.floor_data)
        soup_li = soup_small_page.find_all('li')
        for i in soup_li:
            try:
                row = {
                    'name': '',
                    'desc': '',
                    'date_time': '',
                    'price': 0.0,
                    'discount': 0.0,
                    'orig_price': 0.0,
                    'sold_num': 0,
                    'str_people': u'',
                    'brand_name': '',
                    'item_type': u'热款',
                    'img_src': '',
                    'detail_src': '',
                }
                row['name'] = i.h3.attrs.get('title', '')
                row['desc'] = i.h4.string.strip().replace(' ', '')
                row['date_time'] = time.strftime('%Y-%m-%d-%H:%M:%S',time.localtime(time.time()))
                soup_price = i.find('div', 'item-prices')
                row['price'] = string.atof(soup_price.em.string)
                row['orig_price'] = string.atof(string.atof(soup_price.find('del', 'orig-price').string.encode('gbk', 'ignore')))
                row['discount'] = round(row['price']/row['orig_price'], 2)
                row['sold_num'] = string.atof(i.find('span', 'sold-num').em.next)
                row['str_people'] = i.find('span', 'sold-num').em.next.next.strip()
                row['brand_name'] = self.brand_name
                row['item_type'] = u'普通'
                row['img_src'] = i.img.attrs.get('data-ks-lazyload', '')
                row['src_detail'] = i.a.attrs.get('href', '')
            except Exception, e:
                self.log.error(e)
                continue
            result.append(row)
        return result

