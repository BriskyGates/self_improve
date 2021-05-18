# -*- coding: UTF-8 -*-
import os

import math
import sys
import json
from io import BytesIO

# locale
P_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(P_PATH)
from t_client import *


"""
@title:
@author:walle
@file:oss和mongo对比测试.py
@time:2021/04/16 17:28:45
@description: 
"""


def upload_file_to_oss(file_name):
    """
    上传文件到oss，
    :param file_name:
    :return:
    """
    begin = datetime.now()
    file_path = os.path.join(P_PATH, file_name)
    file = os.stat(file_path)
    upload_files([file_path])
    end = datetime.now()
    size = file.st_size
    size1 = file.st_size / 1024
    sec = (end - begin).total_seconds()
    speed = round((size / sec) / 1024, 3)
    ms = "上传文件到oss服务器， 文件名: {} 大小：{}K， 耗时： {}秒， 速度 {}kb/s".format(file_name, size1, sec, speed)
    print(ms)


def download_file_from_oss(oss_key: str):
    """
    从oss下载文件
    :param oss_key:
    :return:
    """
    begin = datetime.now()
    file = BytesIO(download(oss_key))
    end = datetime.now()
    size = len(file.read())
    size1 = size / 1024
    sec = (end - begin).total_seconds()
    speed = round((size / sec) / 1024, 3)
    ms = "从oss服务器下载文件，大小：{}K， 耗时： {}秒， 速度 {}kb/s".format(size1, sec, speed)
    print(ms)


def put_json_to_mongo(file_name: str) -> dict:
    """
    把json对象上传到mongodb服务器.
    :param file_name:
    :return:
    """
    begin = datetime.now()
    file_path = os.path.join(P_PATH, file_name)
    resp = None
    with open(file=file_path, mode="r", encoding="utf-8") as f:
        resp = put_dict(json.loads(f.read()))
    file = os.stat(file_path)
    end = datetime.now()
    size = file.st_size
    size1 = file.st_size / 1024
    sec = (end - begin).total_seconds()
    speed = round((size / sec) / 1024, 3)
    ms = "上传文件到mongo服务器， 文件名: {} 大小：{}K， 耗时： {}秒， 速度 {}kb/s".format(file_name, size1, sec, speed)
    print(ms)
    return resp


def put_json_to_mongo2(file_names: List[str]):
    """
    把json对象批量上传到mongodb服务器.
    :param file_names:
    :return:
    """
    begin = datetime.now()
    file_paths = [os.path.join(P_PATH, x) for x in file_names]
    resp = None
    dicts = []
    size = 0
    for file_path in file_paths:
        with open(file=file_path, mode="r", encoding="utf-8") as f:
            dicts.append(json.loads(f.read()))
            size += os.stat(file_path).st_size
    # resp = put_dicts(dicts)
    # print(resp)
    put_dicts_async(dicts)
    end = datetime.now()
    size1 = size / 1024
    sec = (end - begin).total_seconds()
    speed = round((size / sec) / 1024, 3)
    ms = "上传{}个文件到mongo服务器 大小：{}K， 耗时： {}秒， 速度 {}kb/s".format(len(dicts), size1, sec, speed)
    print(ms)




if __name__ == '__main__':
    # 上传文件到oss
    upload_file_to_oss(file["OSS客户端使用说明.pdf","t_client.py"])
    # 把json文件的内容保存到mongodb
    # print(put_json_to_mongo("出口_报关单_1616382535.json"))
    # print(put_json_to_mongo("原始发票_1614675813.json"))
    # 把json文件的内容批量保存到mongodb
    # put_json_to_mongo2(["出口_报关单_1616382535.json"])
    # 使用dict_id获取json对象
    print(get_dict("607f047919e363aee43743ec"))
    # 使用oss_key获取json对象
    # print(get_dict(oss_key="20210323090837_77028ad64ee73123030df7bbb5894c41.json"))
    # get_dict("607f046219e363aee437439b", 0)
    # begin = datetime.now()
    # get_dict("607f046219e363aee437439b", 0)
    # end = datetime.now()
    # print((end - begin).total_seconds())
    # begin = datetime.now()
    # get_dict("607f046219e363aee437439b", 1)
    # end = datetime.now()
    # print((end - begin).total_seconds())
    # put_json_to_mongo("原始发票_1614675813.json")
    # 测试上传小于16m的json文件/对象
    # upload_file_to_oss("原始发票_1614675813.json")
    # put_json_from_mongo("原始发票_1614675813.json")
    pass
