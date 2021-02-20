import json
import os

from loguru import logger

from setting import CACHE_PWD_DIR


class BaseJsonOperation:

    def save_json(self, data: dict, out_path: str):  # 如果out_path 中不存在给定的路径,会报错哦,例如 ./result/t.json,因为不存在result 文件夹会报错
        with open(out_path, 'w', encoding="utf-8") as fw:
            json.dump(data, fw, indent=4, ensure_ascii=False)

    def load_json(self, in_path):
        with open(in_path, 'r', encoding="utf-8") as fr:
            temp = json.load(fr)
            return temp


class JsonOperation():
    def __init__(self, file_path):
        self.file_path = file_path

    @logger.catch  # 加载文件可能出现问题
    def load_json(self):
        """
        :param file:
        :return:
        """
        with open(self.file_path, 'r', encoding="utf-8") as fr:
            # logger.info(f'正在处理{self.file_path}')
            temp = json.load(fr)
            return temp

    def save_json(self, obj):
        """
        :param obj: dict 数据
        :param path:
        :return:
        """
        # 针对海进的文件名加入类型识别前缀
        with open(self.file_path, 'w', encoding="utf-8") as fw:
            json.dump(obj, fw, indent=4, ensure_ascii=False)
        print(f'{self.file_path}生成完成')

    def update_json(self, data: dict):
        old_dict = self.load_json()
        old_dict.update(data)  # 更新data数据
        self.save_json(old_dict)


if __name__ == '__main__':
    jo = JsonOperation(CACHE_PWD_DIR)
    jo.update_json({'a': 'b'})
    pass
    # base_json = BaseJsonOperation()
    # final_data = {'beijing': 'abc'}
    # base_json.save_json(final_data, './result/final_export.json')
    # jo = JsonOperate(
    #     'D:\项目相关2020年11月6日\docuai_dmu\main_process_control_tool\source\shipping_note\dl.caspianli2021-01-15T143407大木订舱委托----297\托书-DAS21M019.pdf')
    # jo.fetch_json_path()
