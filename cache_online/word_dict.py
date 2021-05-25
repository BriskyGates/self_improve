# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Brisk
@Version        :  WIN10, Python3.7.9
------------------------------------
@IDE            ： PyCharm-> word_dict
@Description    :  
@CreateTime     :  5/13/2021 5:25 PM
------------------------------------
@ModifyTime     :  
"""
import traceback

from loguru import logger

from cache_online.double_array_trie import DoubleArrayTrieImp1


class WordDict(DoubleArrayTrieImp1):
    def __init__(self, data, data_type):
        super(WordDict, self).__init__(data)
        self.data = data
        self.data_type = data_type

    def add_list2tree(self):
        try:
            # 构建双数组树
            data_trie = DoubleArrayTrieImp1(self.data)  # i don't know why we need to transfer it twice
            data_trie.build(self.data)
            return data_trie
        except Exception as e:
            traceback.print_exc()
            logger.info(f"构建{self.data_type}双数组树错误{e}")
