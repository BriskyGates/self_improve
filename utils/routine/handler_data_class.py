import os
import re
import textwrap
import traceback
from collections import defaultdict
from decimal import Decimal
from functools import reduce

from loguru import logger

from universal_constant import PATTERN_PURE_DIGIT, LOG_DIR, INVOICE_PATTERN
from utils.routine.loguru_utils import LoguruUtil


# constants


class HandleData():
    LoguruUtil(LOG_DIR, 'handler_data_cluster.log').loguru_main()

    @staticmethod
    def is_single(string, pattern):
        """判断当前文件名是否是分开还是合并的"""
        result = re.search(pattern, string, flags=re.I)
        if result:
            # 提取发票号,看看是否可以
            return False
        return True

    @staticmethod
    def check_multi_key_exists(data: dict, parent, child, default_value):
        """
        查看字典中parent 不存在child,则创建默认值key
        :param parent:
        :param child:
        :param default_value:
        :return:
        """
        if not data[parent].get(child):  # munch 中没有的值可以新建, 但不能取值
            data[parent][child] = default_value

    def form_inv_no_dict(self, data: list) -> dict:
        inv_data_dict = {}

        for each_inv in data:
            each_basename = os.path.basename(each_inv)
            inv_no = self.extract_specific_data(each_basename, INVOICE_PATTERN)
            inv_data_dict[inv_no] = each_inv
        return inv_data_dict

    @staticmethod
    def check_no_data(*args):
        """
        实现检查arg 多列表中的各个列表是否存在空列表
        :param data_list:
        :return:
        """
        for i in args:
            i = i.strip() if isinstance(i, str) else i
            if not i:  # 检查i 是否为空列表
                return False
        return True

    @logger.catch
    def form_data_dict(self, data: dict):
        new_data_dict = {}
        for key, value in data.items():
            if isinstance(value, list):
                new_value = self.customize_join(value)
                new_data_dict[key] = new_value
            else:
                new_data_dict[key] = value.strip()
        data_default_dict = defaultdict(str, new_data_dict)  # 创建默认字典的原因,防止用res['key']出现keyerror
        return data_default_dict

    def check_folder_exists(self, folder_path):
        """
        检查目录下是否存在folder_path, 没有则创建
        """
        exists_json_dir = os.path.exists(folder_path)
        if not exists_json_dir:
            os.makedirs(folder_path)

    def replace_list(self, full_list, half_list, data):
        visit_size = len(full_list)
        for index in range(visit_size):
            data = data.replace(full_list[index], half_list[index])
        return data

    def deal_similar_str(self, data_list, data_str):
        for each in data_list:
            if each.strip() in data_str.lower():  # data_str 统一处理成小写, each 采用去除前后空格
                return True
        else:
            return False

    @logger.catch
    def customize_join(self, data):
        new_args = filter(None, data)  # 过滤空数据
        return '\n'.join(new_args)

    def fetch_dict_data(self, data: dict, key_list):
        """取出data下 key_list中的所以键的值， 构成值的列表"""
        return [data.get(key, "") for key in key_list]

    def delete_useless_sub(self, data, pattern):
        # logger.info(f'未经处理的data为{data}')
        if not pattern:  # 如果pattern 列表为空,则返回原数据
            return data
        delimiter_after = '|'.join(pattern)
        # print(f'生成的pattern为{delimiter_after}')
        new_data = re.sub(delimiter_after, '', data, flags=re.I)
        logger.info(f'去除多余符号后的新data为{new_data}')
        return new_data
        # return new_data.replace(' ','')

    def delete_useless_symbol(self, data: str, pattern):
        """
        把data 中符合pattern的字符替换成空格
        """
        for i in pattern:
            data = data.replace(i, '')
        return data

    def delete_style_html(self, data: str):  # 去除字符串中的样式,例如body {...}
        curly_brace_index = data.rfind('}')
        if curly_brace_index != -1:
            return data[curly_brace_index + 1:]
        return data

    @logger.catch
    def keep_decimal_place(self, data: str, place):
        # 保留小数点后place位
        if not data:
            return ''
        keep_place = '0.0'.ljust(place + 2, '0')  # 原本占了两位
        new_data = Decimal(data).quantize(Decimal(keep_place))

        return str(new_data)  # 将decimal类型转换成str类型

    def form_regex_pattern(self, data_list):
        pattern_list = [f'({key})' for key in data_list]
        pattern_res = '|'.join(pattern_list)
        return pattern_res

    def check_data_length(self, data: str, len_limit):
        # 保留data中的前len_limit位数据,包括len_limit位
        if len(data) < len_limit:
            return data
        return data[:len_limit]

    def fetch_all_value(self, data: str, pattern):
        """获取字符串中所有的数值"""
        if not data:
            return ''
        value_list = re.findall(pattern, data)
        if len(value_list) > 1:
            # 把所有的value_list相加
            pass
        return value_list[0]

    @staticmethod
    def count_regex_num(data, pattern):
        pattern_count = 0  # 找出列表中符合pattern的数据个数
        for each in data:
            search_res = re.search(pattern, each, flags=re.I)
            if search_res is None:
                continue
            else:
                pattern_count += 1
        return pattern_count

    @staticmethod
    def extract_specific_data(data, pattern):
        "传进来的pattern 必须要有括号!"
        search_res = re.search(pattern, data, flags=re.I)
        if search_res is None:
            return ""
        else:
            return search_res.group(1)

    def fetch_specific_data(self, data: str, pattern, groupn=0):
        """groupn 提取的是组号"""
        data_res = re.search(pattern, data, flags=re.I)
        if data_res is not None:
            return data_res.group(groupn)
        else:
            return ""

    def sum_data(self, data_list):
        if data_list:
            return reduce(lambda x, y: x + y, data_list)
        else:
            return ''

    def fetch_not_empty(self, data1: str, data2: str):
        merge_data = [data1, data2]
        if not any(merge_data):  # 排除两个data 都不存在
            return False
        # 先去重,再把空排除掉---如果发票和箱单中的total_nw 值不同就无法做去重工作
        if not all(merge_data):  # 选择其中一个即可
            temp_data = list(filter(None, merge_data))
            return temp_data[0]  # 返回其中的数值
        # 剩下的情况是两者都有,返回其中一个数值都可以
        return data1

    def handle_value_str(self, value: str):
        """
        对数值型字符串的数字抽取, 并返回浮点数
        :param value:
        :return:
        """
        new_str = ''
        try:
            new_str = float(value)
        except ValueError:
            # ocr_result_log.info(traceback.format_exc())
            res = re.match(PATTERN_PURE_DIGIT, value)
            if res is not None:
                new_str = float(res.group(1))
        return new_str

    def fetch_limited_length(self, data: str, limited_length, out_type='list'):
        # break_long_words 规定超过width 不切割单词,添加下一行展示
        out_data = textwrap.fill(data, width=limited_length, break_long_words=False)
        if out_type == 'str':
            return out_data
        return out_data.splitlines()  # 返回提取分行的字典

    def handle_value_str_pure(self, value: str):
        """
        对数值型字符串的数字抽取, 并返回浮点数
        :param value:
        :return:
        """
        new_str = ''
        res = re.match(PATTERN_PURE_DIGIT, value)
        if res is not None:
            new_str = res.group(1)  # 提取第一个适配数值
        return new_str


if __name__ == '__main__':
    hd = HandleData()
    temp = hd.check_no_data(' ')
    print(temp)
    # ss = ''.replace('，', ",").replace('‘', "'").replace("’", "'").replace('”', '"').replace('“', '"').replace('：', ':')
    #
    # res = hd.strB2Q('，4123')
    # print(res)
    # container_str1 = "箱型箱量： 20GP加重柜 X    12\n运费条款： "
    # container_str1 = "22MT,1X20’GP\n"
    # container_str1 = "20'GP * 12;\n"
    # container_str1 = "2*40GP SA"
    # container_str1 = "1X20GP+1X40HQ ,FRE"  # 主要分成两种
    # pattern = ['\n', '’', "'", '[\u4e00-\u9fa5]', ' ']
    # hd.delete_useless_sub(container_str1, pattern)
    # hd.keep_decimal_place('12.17', 1)
