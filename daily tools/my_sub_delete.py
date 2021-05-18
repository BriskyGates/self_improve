# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Brisk
@Version        :  WIN10, Python3.7.9
------------------------------------
@IDE            ： PyCharm-> my_sub_delete
@Description    :  
@CreateTime     :  5/13/2021 10:03 AM
------------------------------------
@ModifyTime     :  
"""
import re


def delete_string_sub(pattern: list, data, repl_ch=""):
    """利用sub 删除 匹配上的字符"""
    # 这边封装成 | 连接的
    print(f'利用正则sub 删除前的数据为{data}')
    pattern_list = [f'({key})' for key in pattern]
    pattern_res = '|'.join(pattern_list)
    # new_data = re.sub(pattern, repl_ch, data, flags=re.I)
    new_data = re.sub(pattern_res, repl_ch, data, flags=re.I)
    print(f'利用正则sub 删除后的数据为{new_data}')
    return new_data


mystring = "1-13 (@PA2L4LCETNTSS) LQ190E1LW52Y 1560 2683.2000 3265.20 23.68"
mystring = "1-13 PALLET LQ190E1LW52Y 1560 2683.2000 3265.20 23.68"
# delete_string_sub(r"[(](.*?)[)]",mystring)
# delete_string_sub("\(.*?\)|PALLET", mystring)
delete_string_sub(["\(.*?\)","PALLETS"], mystring)
