# -*-coding:utf-8-*-
import time
from ju_setting import INPUT_FILE_PATH
from ju_report.excel_handler.deal_excel import DealExcel
from utils.url_parser.get_page import GetPageData
from ju_report.item_parser.get_item import GetJuFloor, GetJuItem
from config.ju_define import JU_ITEM_HEADER
from bs4 import BeautifulSoup

def get_image_input_console(url, brand_name):
    is_get_image = False
    flag = raw_input(u"===》是否抓取图片？（是：yes或y，否：任意其他输入）：%s \n" % brand_name)
    if flag.strip().lower() in ['yes', 'y']:
        is_get_image = True
    return is_get_image

def say_hi_to_start(url, brand_name):
    print u"===》品牌名称：%s" % brand_name
    print u"===》url地址：%s" % url
    print u"===》开始抓取，制作报表......"

def main():

    excel_handler = DealExcel(INPUT_FILE_PATH, 'Sheet1')
    ju_brands = excel_handler.read_column_excel(1, 2)
    ju_urls = excel_handler.read_column_excel(2, 2)
    ju_pages = GetPageData(ju_urls, ju_brands)
    result = []
    for i, j in zip(ju_urls, ju_brands):
        result.append(ju_pages.get_page(i, j))
        say_hi_to_start(i, j)
        
        is_get_image = get_image_input_console(i, j)

    # 在页面中抓取出floors
    floors = []
    for index, item in enumerate(result):
        floors.append(GetJuFloor(item['data'], item['title']).get_floors())

    values = []
    time_start = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    for item in floors:
        row_big_item = []
        row_small_item = []
        row_big_item = GetJuItem(item.get('big'), item['brand_name']).get_big_items()
        values.extend(row_big_item)
        small_pages = GetPageData(item['small'].get('urls'), item['brand_name']).get_pages()
        for i in small_pages:
            row_small_item.extend(GetJuItem(i, item['brand_name']).get_small_items())
        values.extend(row_small_item)
        excel_handler.excel_insert(item['brand_name']+time_start+'.xls', values, JU_ITEM_HEADER)


if __name__ in "__main__":
    main()
