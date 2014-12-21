# -*-coding:utf-8-*-
from pyExcelerator import *
import xlrd
from utils.log import get_file_logger


class DealExcel(object):
    """
    将信息读出或存入excel文件中
    """

    def __init__(self, file_name, sheet_name):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.log = get_file_logger('excel_handler')

    def read_column_excel(self, column_num=1, start_row_num=1):
        """
        从某一行开始，把对应的某一列的值读取出来
        """
        try:
            file_info = xlrd.open_workbook(self.file_name)
            sheet_info = file_info.sheet_by_name(self.sheet_name)
            sheet_rows = sheet_info.nrows
            sheet_columns = sheet_info.ncols

            column_values = []
            if start_row_num > sheet_rows:
                start_row_num = 1
            elif column_num > sheet_columns:
                column_num = 0
            for i in range(start_row_num-1, sheet_rows):
                column_values.append(sheet_info.cell_value(i, column_num-1))
        except Exception, e:
            self.log.error(e)
            return []
        return column_values

    def excel_insert(self, excel_file_name, values, header, row_num=0):
        """
        将输入存入, 返回数据记录总数
        """
        w = Workbook()
        ws = w.add_sheet(u'聚划算报表')
        len_values = len(values)
        if row_num == 0:
            for index, item in enumerate(header):
                #print row_num,index,item
                try:
                    ws.write(row_num, index, item)
                except Exception, e:
                    self.log.error(e + str(item))
                    continue
            row_num = row_num + 1
        for index, value in enumerate(values):
            try:
                tmp = index + row_num
                ws.write(tmp, 0, value['name'])
                ws.write(tmp, 1, value['desc'])
                ws.write(tmp, 2, value['date_time'])
                ws.write(tmp, 3, value['price'])
                ws.write(tmp, 4, value['discount'])
                ws.write(tmp, 5, value['orig_price'])
                ws.write(tmp, 6, value['sold_num'])
                ws.write(tmp, 7, value['str_people'])
                ws.write(tmp, 8, value['brand_name'])
                ws.write(tmp, 9, value['item_type'])
                ws.write(tmp, 10, value['img_src'])
                ws.write(tmp, 11, value['src_detail'])
            except Exception, e:
                self.log.error(e)
                continue

        w.save(excel_file_name)
        return row_num
