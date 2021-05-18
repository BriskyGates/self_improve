# -*- coding:utf-8 -*-
# standard
import asyncio
import os
import sys
import re
from datetime import datetime
from functools import partial

# third
import httpx
import requests
from colorama import Fore
from loguru import logger as uru_logger

# locale
P_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(P_PATH)


"""
@title: 使用 pysnooper构建的客户端,
@author:walle
@file:snoop_clients
@time:2021/04/13 09:49:38
@description:
目前支持2种日志工具： pysnooper  和 loguru ，未来可能会增加标准的logger

loguru: 这是最常用的日志，使用方法：
首先下载clients.py到你的项目中。然后
##########################
from clients import get_logger

logger = get_logger()
logger.error("错误信息“）
logger.info("info信息“）
logger.debug("debug信息“）
##########################
pysnooper的特点是记录的特别详细.特别适合于捕捉分析问题.
一般用在排查复杂问题时临时使用。问题排除后注销或者删除即可。
由于它的日志输出量太大.会拖慢程序运行，所以不适合在生产环境中长期使用
.注意,pysnooper 在 pycharm 的debug模式无效.
*--*--*--*
依赖安装 pip/pip3 install pysnooper colorama  httpx loguru
正常的异步函数运行  asyncio.run(func())  # python 3.8
如果你处于更低的python版本或者windows平台上,那么你需要第三方的异步库
有关异步的第三方库
curio https://github.com/dabeaz/curio
一个可以在unix和windows上运行的异步库,可以很好的替代async的标准库,拥有2倍以上的性能.
curio.run(func)  # 注意没有括号
trio https://github.com/python-trio/trio
一个curio的跟随者, 虽然只诞生了不到一年(截至2021-04-13,curio诞生了一年多),单追随者甚至比curio更多,
trio.run(func)  # 注意没有括号
以上2个库不能同时import,并且httpx已经不再支持curio
实测中,和原生库提升了不到2倍的差距. 作为替代品还是不错的.

虽然使用rpc写入日志也是一个好文档方案，但是由于日志写比较频繁，和用于关键业务的rpc在一起的话，担心会影响核心业务。暂时
不采用这个方案  2021-5-8
"""


LOG_SERVER_HOST = "121.5.100.192:7014"  # 日志服务器的主机地址，包含端口号
# LOG_SERVER_HOST = "127.0.0.1:8001"  # 日志服务器的主机地址，包含端口号
APP_NAME = "brisk_logger"  # 用于唯一标识你的项目,要求是的不重复 todo: 请改成你自己定义的值


async def async_post_log(url: str, payload: dict):
    """
    发送请求到日志服务器
    :param url: 日志接口
    :param payload: 请求载荷
    :return:
    """
    begin = datetime.now()
    async with httpx.AsyncClient() as client:
        resp = {"message": "success"}
        result = None
        try:
            result = await client.post(url, json=payload)
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
            print(resp)
    end = datetime.now()
    print("异步请求耗时： {}秒".format((end - begin).total_seconds()))


def post_log(url: str, payload: dict):
    """
    发送请求到日志服务器
    :param url: 日志接口
    :param payload: 请求载荷
    :return:
    """
    begin = datetime.now()
    resp = {"message": "success"}
    result = None
    try:
        result = requests.post(url, json=payload)
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
        print(resp)
    end = datetime.now()
    print("同步请求耗时： {}秒".format((end - begin).total_seconds()))


def stream_handler(mes):
    """
    pysnooper的记录函数
    :param mes: 日志内容
    :return:
    """
    mes = re.sub(r"\n", "", mes)
    print(Fore.YELLOW + mes)
    data = {
        "app_name": APP_NAME,
        "content": mes
    }
    url = "http://{}}/log/v0/stack/add".format(LOG_SERVER_HOST)
    if hasattr(asyncio, 'run'):
        asyncio.run(async_post_log(url=url, payload=data))
    else:
        post_log(url=url, payload=data)


def loguru_handler(mes: str, level: str):
    """
    pysnooper的记录函数
    :param mes: 日志内容
    :param level: 日志级别
    :return:
    """
    mes = re.sub(r"\n", "", mes)
    print(Fore.GREEN + mes)
    data = {
        "app_name": APP_NAME,
        "level": level.lower(),
        "content": mes
    }
    url = "http://{}/log/v0/manual/add".format(LOG_SERVER_HOST)
    print(url)
    if level == mes.split(" ", 1)[0]:
        if hasattr(asyncio, 'run'):
            # 优先使用异步，但是3.8版本以下的没有 run 这个方法
            asyncio.run(async_post_log(url=url, payload=data))
        else:
            post_log(url=url, payload=data)
    else:
        # 忽略重要程度低的handler对重要程度高的日志的记录行为，（默认debug会记录info和error级别的日志）
        pass


def get_logger(file_prefix: str = None, *args, **kwargs):
    """
    返回一个loguru的实例,这个实例具备写入日志服务器的功能
    :param file_prefix: 文件名前缀
    :return:
    """
    file_prefix = "{}_".format(file_prefix) if isinstance(file_prefix, str) and len(file_prefix) > 0 else ''
    log_dir = os.path.join(P_PATH, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    info_path = os.path.join(log_dir, file_prefix + "{time:YY_MM_DD}_info.log")
    debug_path = os.path.join(log_dir, file_prefix + "{time:YY_MM_DD}_debug.log")
    error_path = os.path.join(log_dir, file_prefix + "{time:YY_MM_DD}_error.log")
    """
    add的可用参数
    rotation="500 MB"   # 文件过大就会重新生成一个文件
    rotation="12:00"    # 每天12点创建新文件
    rotation="1 week"   # 文件时间过长就会创建新文件
    retention="10 days" # 一段时间后会清空
    compression="zip"   # 保存zip格式
    enqueue=True        # 异步写入
    serialize=True      # 序列化为json
    """
    setting = {
        "rotation": "0:00",
        "retention": "5 days",
        "encoding": "utf-8",
        "format": "{time:HH:mm:ss} {message}",
    }
    setting2 = {
        "format": "{level} {time:HH:mm:ss} {message}",
    }
    uru_logger.add(sink=partial(loguru_handler, level="DEBUG"), level="DEBUG", **setting2)
    uru_logger.add(debug_path, level="DEBUG", **setting)
    uru_logger.add(sink=partial(loguru_handler, level="INFO"), level="INFO", **setting2)
    uru_logger.add(info_path, level="INFO", **setting)
    uru_logger.add(sink=partial(loguru_handler, level="ERROR"), level="ERROR", **setting2)
    uru_logger.add(error_path, level="ERROR", **setting)
    return uru_logger


if __name__ == "__main__":
    logger = get_logger()
    kw = {
        "app_name": "test_app",
        "level": "info",
        "content": "我是日志212121"
    }
    logger.info("121")
    # logger.debug("我是debug日志212121")
    # logger.error("我是error日志212121")
    pass
