# -*-coding:utf-8-*-
import time
import re
import string
import torndb
from bs4 import BeautifulSoup
from ju_setting import INPUT_FILE_PATH
from ju_report.excel_handler.deal_excel import DealExcel
from utils.url_parser.get_page import GetPageData
from ju_report.item_parser.get_item import GetJuFloor, GetJuItem
from config.ju_define import JU_ITEM_HEADER
from ju_setting import MYSQL_USER, MYSQL_PASSWORD
from utils.log import get_file_logger


# TODO rewrite
def main():
    log = get_file_logger('ju_item_insert')
    hostaddress = 'localhost'
    database = 'ju_db'
    user = MYSQL_USER
    password = MYSQL_PASSWORD
    db = torndb.Connection(hostaddress, database, user, password)

    excel_handler = DealExcel(INPUT_FILE_PATH, 'Sheet1')
    ju_brands = excel_handler.read_column_excel(1, 2)
    ju_urls = excel_handler.read_column_excel(2, 2)
    ju_pages = GetPageData(ju_urls, ju_brands)
    result = []
    for i, j in zip(ju_urls, ju_brands):
        result.append(ju_pages.get_page(i, j))
    # 在页面中抓取出floors
    floors = []
    for index, item in enumerate(result):
        floors.append(GetJuFloor(item['data'], item['title']).get_floors())

    values = []
    time_start = time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))

    for item in floors:
        row_big_item = []
        row_small_item = []
        row_big_item = GetJuItem(item.get('big'), item['brand_name']).get_big_items()
        values.extend(row_big_item)
        small_pages = GetPageData(item['small'].get('urls'), item['brand_name']).get_pages()
        for i in small_pages:
            row_small_item.extend(GetJuItem(i, item['brand_name']).get_small_items())
        values.extend(row_small_item)

    sql_item = "INSERT INTO ju_brand_item (id, name, description, created, price, orig_price, started, item_type, brand_name) \
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    sql_num = "INSERT INTO ju_brand_item_num (item_id, sold_num) VALUES (%s, %s)"

    sql_item_detail = "INSERT INTO ju_brand_item_detail (item_id, img_src, detail_src) VALUES (%s, %s, %s)"

    db_item = []
    db_item_num = []
    db_item_detail = []
    for value in values:
        try:
            if value['str_people'] == u'\u4eba\u5df2\u4e70\n':
                is_started = True
            else:
                is_started = False
            item_id = string.atoi(re.findall(r'\d+', value['src_detail'])[0])
            db_item.append(
                [item_id, value['name'], value['desc'], value['date_time'], value['price'], value['orig_price'],
                 is_started, value['item_type'], value['brand_name']])
            db_item_num.append([item_id, value['sold_num']])
            db_item_detail.append([item_id, value['img_src'], value['src_detail']])
        except Exception, e:
            log.error(str(value['name']))
            continue
    db.insertmany(sql_item, db_item)
    db.insertmany(sql_num, db_item_num)
    db.insertmany(sql_item_detail, db_item_detail)


if __name__ in "__main__":
    main()
