import os

from openpyxl import load_workbook

from hongming_backend.constants import TEMPLATE_DIR


class ExcelOperation:
    def __init__(self, filename):
        self.filename = filename
        self.ws = None
        self.init_excel()

    def init_excel(self):
        """打开excel,获取报关单子表的sheet 对象,并将其赋值给self.ws"""
        wb = load_workbook(self.filename, read_only=True)  # 为脱离页眉页脚的警告,加入read_only参数
        sheet_name = 'Sheet1'  # 子表默认值
        self.ws = wb[sheet_name]  # 加载报关单子表

    def fetch_cell_value(self):
        """
        从A1 ,B1 开始读取,返回键值对数据,返回字典数据,第一列为键,第二列为值
        """
        max_row = self.ws.max_row
        final_data = {}
        for row in range(1, max_row + 1):
            key = self.ws.cell(row, 1).value
            value = self.ws.cell(row, 2).value
            final_data[key] = value if value else ""
        return final_data


if __name__ == '__main__':
    file_path = os.path.join(TEMPLATE_DIR, 'CN_20201117-142628787.xlsx')
    eo = ExcelOperation(file_path)
    eo.fetch_cell_value()
