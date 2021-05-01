#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: 十洲
@time: 2020/12/17 18:22
@desc: 日志文件
"""
import os
import datetime
from loguru import logger

class MyFilter:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        level_no = logger.level(self.level).no
        return record["level"].no == level_no

class Logger:
    def __init__(self, logger_dir):
        self.file_dir = logger_dir
        self.inf_log = logger
        self.dubg_log = logger
        self.err_log = logger

    def set_log(self, file_name):
        now_time = datetime.datetime.now().strftime('%Y%m%d')
        file_dir = self.file_dir + now_time + "/"
        if os.path.exists(file_dir):
            pass
        else:
            os.mkdir(file_dir)
        info_path = file_dir + file_name + "_" + "{time:HH_mm}_info.log"
        debug_path = file_dir + file_name + "_" + "{time:HH_mm}_debug.log"
        error_path = file_dir + file_name + "_" + "{time:HH_mm}_error.log"

        self.inf_log.add(info_path, format="{time:HH:mm:ss} {message}",
                         filter=MyFilter("INFO"), retention='5 days')
        self.dubg_log.add(debug_path, format="{time:HH:mm:ss} {message}",
                          filter=MyFilter("DEBUG"), retention='5 days')
        self.err_log.add(error_path, format="{time:HH:mm:ss} {message}",
                         filter=MyFilter("ERROR"), retention='5 days')

    def info(self, name):
        self.inf_log .info(name)

    def debug(self, name):
        self.dubg_log.error(name)

    def error(self, name):
        self.err_log.error(name)
#
# logger_dir = config.get("logger_path")
# if os.path.exists(logger_dir):
#     pass
# else:
#     os.mkdir(logger_dir)
# logging = Logger(logger_dir)
