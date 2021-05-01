import os

from loguru import logger
from openpyxl import load_workbook

from hongming_backend.constants import TEMPLATE_DIR, HMG_COO_TEMPLATE
import pandas as pd


class ExcelMultiOperation:
    def __init__(self, filename):
        self.filename = filename

    @logger.catch
    def get_data_by_pandas(self):
        final_data = []
        title = "title"
        item = "item"
        sheet_content = pd.read_excel(self.filename, sheet_name=None, header=None)
        for each, value in sheet_content.items():
            if value.empty:  # 防止出现空子表
                continue
            value.fillna('', inplace=True)  # nan 替换成""
            final_data_temp = {}
            flag = ""  # 默认键值为空
            for i in range(0, len(value)):  # 遍历每一个子表的数据
                temp1, temp2 = value.iloc[i][0], value.iloc[i][1]  # 某一行第0个和第1个元素
                if temp1 in [title, item]:  # 出现title 则创建title键
                    final_data_temp[temp1] = {}
                    flag = temp1  # 用来判断flag是否为item
                    continue
                elif temp1 != 'type':
                    final_data_temp[flag][temp1] = temp2  # 当前默认成title的键
                else:
                    final_data_temp[temp1] = temp2  # type 直接赋值
            else:  # 循环结束后执行
                final_data.append(final_data_temp)
        logger.info(final_data)

    def main(self):
        self.get_data_by_pandas()


if __name__ == '__main__':
    file_path = "coo_出口模板.xlsx"
    c_file_path=os.path.join(HMG_COO_TEMPLATE,file_path)

    eo = ExcelMultiOperation(c_file_path)
    eo.main()
