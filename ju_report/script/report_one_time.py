# -*-coding:utf-8-*-
import time
from ju_setting import INPUT_FILE_PATH
from ju_report.excel_handler.deal_excel import DealExcel
from utils.url_parser.get_page import GetPageData
from ju_report.item_parser.get_item import GetJuFloor, GetJuItem
from config.ju_define import JU_ITEM_HEADER
from bs4 import BeautifulSoup

def get_image_input(url, brand_name):
    is_get_image = False
    flag = raw_input("===》是否抓取的图片？（是：yes或y，否：任意其他输入） \n")
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
        page = ju_pages.get_page(i, j)
        row_big_item = []
        row_small_item = []
        say_hi_to_start(i, j)
        if not page:
            failed = raw_input("===》抓取失败，请检查网路是否正常，按任意键退出......")
            return False
        else:
            floor = GetJuFloor(page['data'], page['title']).get_floors()
            time_start = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            row_big_item = GetJuItem(floor.get('big'), floor['brand_name']).get_big_items()
            result.extend(row_big_item)
            small_pages = GetPageData(floor['small'].get('urls'), floor['brand_name']).get_pages()
            for i in small_pages:
                row_small_item.extend(GetJuItem(i, j).get_small_items())
            result.extend(row_small_item)
            excel_handler.excel_insert(j+time_start+'.xls', result, JU_ITEM_HEADER)
            print u"%s 报表制作完成" % (j+time_start+'.xls')
            if get_image_input(i, j):
                for item in result:
                    GetPageData.get_images(item['img_src'], item['name'])
    success = raw_input("===》运行结束，按任意键退出......\n")
    return True

if __name__ in "__main__":
    main()
