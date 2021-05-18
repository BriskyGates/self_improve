# -*- coding: UTF-8 -*-
# standard
import os
import sys
import json
from datetime import datetime
from typing import List
from typing import Dict
from typing import Any
from typing import Callable
from uuid import uuid4
from warnings import warn

# third
import httpx
import requests
from loguru import logger
from pydantic import validate_arguments
import jwt
import trio



"""
@title: oss存储的客户端
@author:walle
@file:t_client.py
@time:2021/03/21 06:56:15
@description: 
2020-4-6 对发送参数的格式进行了调整,强制使用utf-8传递参数.以避免win系统使用默认的gbk字符集进行转码
必要环境安装：  pip/pip3 install pydantic pyjwt requests
"""


SECRET_KEY = "cJcWVuUpBEXkHhESPJyWXN6o73ZbpFiwPUj42UpJKgSc"  # 加密用的key，不要修改此字符串
ALGORITHM = "HS256"  # 加密算法
HOST = "oss.docuai.cn"  # oss服务器地址
# HOST = "127.0.0.1:8001"


def generate_authorization() -> dict:
    """
    生成授权信息
    :return:
    """
    rid = uuid4().hex
    payload = {
        "rid": rid,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    authorization = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"rid": rid, "authorization": authorization}


@validate_arguments
def _upload_many(files: Dict[str, Any]) -> dict:
    """
    上传文件。参数是文件名和内容组成的字典, 请不要直接调用此函数。
    后端工程师上传文件时应该调用的是 upload_files 函数
    :param files:  件名和内容组成的字典
    :return:
    """
    resp = {"message": "success"}
    secret_dict = generate_authorization()
    url = "http://{}/t_cloud/v0/object/batch_upload?rid={}".format(HOST, secret_dict['rid'])
    headers = {"authorization": secret_dict['authorization']}
    result = None
    try:
        result = requests.post(url=url, files=files, headers=headers)
    except Exception as e:
        resp['message'] = str(e)
    finally:
        if result is None:
            pass
        else:
            if result.status_code == 200:
                resp = result.json()
            else:
                resp['message'] = "服务器返回了错误的状态码: {}".format(result.status_code)
    return resp


@validate_arguments
def upload_files(files: List[str]) -> dict:
    """
    上传文件到腾讯oss。后端工程师上传文件时应该调用本函数,不要上传json文件,那是不赞成的做法.
    :param files:  文件的,可以是绝对路径或者相对当前文件的相对路径组成的数组
    :return:
    """
    file_dict = {}
    for file_path in files:
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            if file_name.lower().endswith(".json"):
                ms = "使用oss保存json文件方法将被废止,建议把json以字典格式保存到mongodb服务器"
                warn(ms)
                # 这是json文件，需要以文本方式读取内容
                file = (file_name.encode(encoding="utf-8"), json.dumps(json.load(open(file_path, mode="r", encoding="utf-8"))))
            else:
                # 这是普通文件，以二进制方式读取内容
                with open(file_path, mode='rb') as f:
                    file = (file_name.encode(encoding="utf-8"), f.read())
            file_dict[file_name] = file
        else:
            ms = "无效的文件路径： {}".format(file_path)
            raise ValueError(ms)
    resp = _upload_many(files=file_dict)
    logger.info(resp)
    return resp


@validate_arguments
def download(oss_key: str) -> bytes:
    """
    从腾讯oss下载文件， 后端工程师上下载文件时调用。
    :param oss_key:  对象存储的唯一key
    :return:
    """
    if oss_key.lower().endswith(".json"):
        ms = "使用oss保存json文件方法将被废止,建议把json以字典格式保存到mongodb服务器"
        warn(ms)
    secret_dict = generate_authorization()
    url = "http://{}/t_cloud/v0/object/{}?rid={}".format(HOST, oss_key, secret_dict['rid'])
    headers = {"authorization": secret_dict['authorization']}
    result = requests.get(url=url, headers=headers)
    if result.status_code == 200:
        return result.json() if oss_key.lower().endswith(".json") else result.content
    else:
        raise RuntimeError("服务器返回了错误的状态码: {}".format(result.status_code))


def __post(url: str, json_dict: Dict[str, Any], headers: Dict[str, Any] = None) -> dict:
    """
    通用post函数。
    :param url:  请求地址
    :param json_dict: json数据载荷字典。
    :param headers: 请求头
    :return: 字典
    """
    resp = {"message": "success"}
    result = None
    try:
        result = requests.post(url=url, json=json_dict, headers=headers)
    except Exception as e:
        resp['message'] = str(e)
    finally:
        if result is None:
            pass
        else:
            if result.status_code == 200:
                resp = result.json()
            else:
                resp['message'] = "服务器返回了错误的状态码: {}".format(result.status_code)
    return resp


@validate_arguments
def put_dict(json_dict: Dict[str, Any]) -> dict:
    """
    把json字典保存到mongo数据库
    :param json_dict: 字典格式，key必须是字符，value只能是以下几种：
        int, float, str, list, dict, bool, None
    :return:
    """
    secret_dict = generate_authorization()
    url = "http://{}/mongo/v0/json/put?rid={}".format(HOST, secret_dict['rid'])
    headers = {"authorization": secret_dict['authorization']}
    return __post(url=url, json_dict=json_dict, headers=headers)


@validate_arguments
def put_dicts(dicts: List[Dict[str, Any]]) -> dict:
    """
    把一批json字典保存到mongo数据库
    :param dicts: 字典格式的数组，字典的key必须是字符，value只能是以下几种：
        int, float, str, list, dict, bool, None
    :return:
    """
    resp = {"message": "success", "data": []}
    secret_dict = generate_authorization()
    url = "http://{}/mongo/v0/json/put?rid={}".format(HOST, secret_dict['rid'])
    headers = {"authorization": secret_dict['authorization']}

    for json_dict in dicts:
        result = None
        try:
            result = requests.post(url=url, json=json_dict, headers=headers)
        except Exception as e:
            resp['message'] = str(e)
        finally:
            if result is None:
                pass
            else:
                if result.status_code == 200:
                    resp['data'].append(result.json())
                else:
                    resp['message'] = "服务器返回了错误的状态码: {}".format(result.status_code)
    return resp


@validate_arguments
def put_dict_async(json_dict: Dict[str, Any], callback: Callable = None) -> None:
    """
    把json字典保存到mongo数据库, 这是一个异步的方法,
    :param json_dict: 字典格式，key必须是字符，value只能是以下几种：
        int, float, str, list, dict, bool, None
    :param callback: 回调函数
    :return:
    """

    async def __put_dict_async(_json_dict: Dict[str, Any], _callback: Callable = None):
        """
        把json字典保存到mongo数据库, 这是一个异步的方法,
        :param _json_dict: 字典格式，key必须是字符，value只能是以下几种：
            int, float, str, list, dict, bool, None
        :param _callback: 回调函数
        :return:
        """
        resp = {"message": "success"}
        secret_dict = generate_authorization()
        url = "http://{}/mongo/v0/json/put?rid={}".format(HOST, secret_dict['rid'])
        headers = {"authorization": secret_dict['authorization']}
        async with httpx.AsyncClient() as client:
            result = None
            try:
                result = await client.post(url=url, json=_json_dict, headers=headers)
            except Exception as e:
                resp['message'] = str(e)
            finally:
                if result is None:
                    pass
                else:
                    if result.status_code == 200:
                        resp['data'] = result.json()
                    else:
                        resp['message'] = "服务器返回了错误的状态码: {}".format(result.status_code)
                if _callback is None:
                    print(resp)
                else:
                    _callback(resp)

    trio.run(__put_dict_async, json_dict, callback)


@validate_arguments
def put_dicts_async(dicts: List[Dict[str, Any]], callback: Callable = None) -> None:
    """
    把一组json字典保存到mongo数据库, 这是一个异步的方法,
    :param dicts: 字典格式的数组，字典的key必须是字符，value只能是以下几种：
        int, float, str, list, dict, bool, None
    :param callback: 回调函数
    :return:
    """

    async def __put_dicts_async(_dicts: Dict[str, Any], _callback: Callable = None):
        """
        把json字典保存到mongo数据库, 这是一个异步的方法,
        :param _dicts: 字典格式的数组，字典的key必须是字符，value只能是以下几种：
        int, float, str, list, dict, bool, None
        :param _callback: 回调函数
        :return:
        """
        resp = {"message": "success", "data": []}
        secret_dict = generate_authorization()
        url = "http://{}/mongo/v0/json/put?rid={}".format(HOST, secret_dict['rid'])
        headers = {"authorization": secret_dict['authorization']}

        async with httpx.AsyncClient() as client:
            for _json_dict in dicts:
                result = None
                try:
                    result = await client.post(url=url, json=_json_dict, headers=headers)
                except Exception as e:
                    resp['message'] = str(e)
                finally:
                    if result is None:
                        pass
                    else:
                        if result.status_code == 200:
                            resp['data'].append(result.json())
                        else:
                            resp['message'] = "服务器返回了错误的状态码: {}".format(result.status_code)
        if _callback is None:
            print(resp)
        else:
            _callback(resp)

    trio.run(__put_dicts_async, dicts, callback)


@validate_arguments
def get_dict(dict_id: str = None, oss_key: str = None) -> dict:
    """
    从mongo数据库获取json字典
    :param dict_id: 上传json到mongo时返回的id
    :param oss_key: oss存储上的oss_key,
    :return:
    """
    resp = {"message": "success"}
    secret_dict = generate_authorization()
    if dict_id is None and oss_key is None:
        resp['message'] = "至少需要一个参数"
    else:
        if dict_id is not None:
            url = "http://{}/mongo/v0/json/get?dict_id={}&rid={}".format(HOST, dict_id, secret_dict['rid'])
        else:
            ms = "使用oss_key查询json字典对象只是一个临时的过渡方案.将来会被移除.请使用dict_id进行查询"
            warn(ms)
            url = "http://{}/mongo/v0/json/get?oss_key={}&rid={}".format(HOST, oss_key, secret_dict['rid'])
        headers = {"authorization": secret_dict['authorization']}
        result = None
        try:
            result = requests.post(url=url, headers=headers)
        except Exception as e:
            resp['message'] = str(e)
        finally:
            if result is None:
                pass
            else:
                if result.status_code == 200:
                    resp = result.json()
                else:
                    resp['message'] = "服务器返回了错误的状态码: {}".format(result.status_code)
    return resp


@validate_arguments
def save_event(json_dict: Dict[str, Any]) -> dict:
    """
    把在线系统所有的操作日志写入数据库。
    :param json_dict: 字典格式，key必须是字符，value只能是以下几种：
        int, float, str, list, dict, bool, None
    :return:
    """
    secret_dict = generate_authorization()
    url = "http://{}/mongo/v0/event/save?rid={}".format(HOST, secret_dict['rid'])
    headers = {"authorization": secret_dict['authorization']}
    return __post(url=url, json_dict=json_dict, headers=headers)


if __name__ == '__main__':
    print(get_dict('607f00c8e36d71c27733b6da'))
    pass
