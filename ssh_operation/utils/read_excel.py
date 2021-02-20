from functools import singledispatch
import openpyxl
from loguru import logger

from setting import *
from utils.class_dispatch import methdispatch
from utils.handle_data import HandleData


class ReadExcel():
    """
    给我一个服务器路径地址<可选>,一个列表,或者字符串我可以给你返回相应的服务器路径
    可能无法处理 同名文件 所对应的坐标
    """

    def __init__(self, filename=IDENTIFY_PROCESS_DIR):
        self.filename = filename
        self.name_excel_dict = {}  # 键为坐标,值为文件名.   可以考虑
        self.sheet = self.init_xlsx()
        self.hd = HandleData()

    @logger.catch
    def fetch_value(self, cell_loc):
        """
        根据坐标获取值
        :param cell_loc: 单元格所在坐标
        :return:
        """
        cell_value = self.sheet[cell_loc].value
        # logger.info(cell_value)
        return cell_value

    def deal_crossbar(self, cell_range):
        cell_range_split = cell_range.split('-')
        cell_start = cell_range_split[0]  # 此处利用ord OR chr
        cell_end = cell_range_split[-1]
        range_list = self.hd.confirm_range(cell_start, cell_end)
        self.fetch_cell(range_list)

    @methdispatch
    def fetch_cell(self, cell_range):
        print(f' 传输参数类型为：{type(cell_range)}，不是有效类型')

    @fetch_cell.register(int)
    def _(self, cell_range: int):
        """
        获取某一个宫格

        :param cell_range: 1
        :return:
        """
        self.fetch_cell(str(cell_range))

    @fetch_cell.register(str)
    def _(self, cell_range: str):
        """
        获取某一个宫格 or区间的数据

        :param cell_range: "X" OR "X-Z"
        :return:
        """
        crossbar_index = cell_range.find('-')
        if crossbar_index == -1:  # 字符串不含有 crossbar
            name_loc = NAME_COLUMN + cell_range  # 拼接文件名所在的位置
            name_value = self.fetch_value(name_loc)
            if self.hd.check_repeat_key(name_loc, self.name_excel_dict):
                self.name_excel_dict[name_value] = name_loc
                return True
            logger.critical(f'传入的范围中存在同名文件名, 只会帮你填写第一个数值哦 :>')
            return False
        self.deal_crossbar(cell_range)
        return True

    @fetch_cell.register(list)
    def _(self, cell_range: list):
        """
        传入分散的列表区间, 例如['2','3'],也可以是数值型元素
        :param cell_range:
        :return:
        """
        cell_list = map(str, cell_range)  # 无论是数值还是字符串, 统一转成字符串
        for each_cell in cell_list:
            self.fetch_cell(each_cell)

    def init_xlsx(self):
        wb = openpyxl.load_workbook(self.filename)
        return wb[IDENTIFY_SHEETNAME]  # 读取项目识别问题记录



if __name__ == '__main__':
    rde = ReadExcel()
    # rde.fetch_value('3')  # 必须传入坐标,例如D3
    # rde.fetch_cell([5, 6, 7])
    rde.fetch_cell('3-6')
    # rde.fetch_cell(3)
    logger.info(rde.name_excel_dict)
