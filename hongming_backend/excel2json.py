import os

from hongming_backend.constants import TEMPLATE_DIR
from utils.excel_utils import ExcelOperation
from utils.json_uitls import JsonOperation


class Excel2Json():
    """给定excel 数据, 把它写到json中"""

    def __init__(self, filename):
        self.filename = filename
        self.excel = ExcelOperation(filename)

    def main(self):
        final_data = self.excel.fetch_cell_value()
        jo = JsonOperation(self.filename)
        jo.save_json(final_data)


if __name__ == '__main__':
    bejson = os.path.join(TEMPLATE_DIR, 'CN_20201117-142628787.xlsx')
    Excel2Json(bejson).main()
