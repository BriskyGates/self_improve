import json
import os
from pathlib import Path

from loguru import logger


class BaseJsonOperation:

    def save_json(self, data: dict, out_path: str):  # 如果out_path 中不存在给定的路径,会报错哦,例如 ./result/t.json,因为不存在result 文件夹会报错
        with open(out_path, 'w', encoding="utf-8") as fw:
            json.dump(data, fw, indent=4, ensure_ascii=False)

    def load_json(self, in_path):
        with open(in_path, 'r', encoding="utf-8") as fr:
            temp = json.load(fr)
            print(temp)
            return temp


class JsonOperation():
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.json_path = ''

    def fetch_json_path(self):
        """
        提取路径中的后缀, 用.json 替换
        :return:
        """
        fp = Path(self.file_path)
        fp_suffix = fp.suffix
        if not fp_suffix:
            raise TypeError('该文件无后缀')
        json_suffix = '.json'
        self.json_path = self.file_path.replace(fp_suffix, json_suffix)

    @logger.catch  # 加载文件可能出现问题
    def load_json(self):
        """
        :return:
        """
        with open(self.file_path, 'r', encoding="utf-8") as fr:
            # logger.info(f'正在处理{self.file_path}')
            temp = json.load(fr)
            return temp

    def save_json(self, obj):
        """
        :param obj: dict 数据
        :return:
        """
        self.fetch_json_path()
        # 针对海进的文件名加入类型识别前缀
        with open(self.json_path, 'w', encoding="utf-8") as fw:
            json.dump(obj, fw, indent=4, ensure_ascii=False)
        print(f'{self.json_path}生成完成')


if __name__ == '__main__':
    # jo = JsonOperation(CACHE_PWD_DIR)
    # jo.update_json({'a': 'b'})
    pass
    base_json = BaseJsonOperation()
    base_json.load_json('SEA_CBL_SI2101119.txt')
    # final_data = {'beijing': 'abc'}
    # base_json.save_json(final_data, './result/final_export.json')
    # jo = JsonOperate(
    #     'D:\项目相关2020年11月6日\docuai_dmu\main_process_control_tool\source\shipping_note\dl.caspianli2021-01-15T143407大木订舱委托----297\托书-DAS21M019.pdf')
    # jo.fetch_json_path()
