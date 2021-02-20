from os import path

from setting import CACHE_PWD_DIR
from utils.new_json_uitls import *


class HandleData():
    def __init__(self):
        self.cache_cwd = JsonOperation(CACHE_PWD_DIR).load_json()  # 避免每次调用fetch_cwd 都要加载一遍json 数据

    def deal_name_option(self, filename):
        """
        对find 参数的name 选项进行处理
        :return:
        """
        prefix, suffix = path.splitext(filename)
        if suffix:  # 如何存在文件拓展名
            return filename
        return f'{filename}.*'  # 如果不存在文件扩展名,则需要添加 .*

    def check_repeat_key(self, key: str, data: dict):
        if key in data:
            return False  # 存在键
        return True  # 不存在键

    def confirm_range(self, start, end):
        int_start = int(start)
        int_end = int(end)
        range_list = [index for index in range(int_start, int_end + 1)]
        return range_list
