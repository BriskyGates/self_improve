# -*- coding: UTF-8 -*-
import os
import sys

P_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(P_PATH)
from t_client import save_event


"""
@title: 记录在线过程的所有记录（接收、识别、审核、后处理、校验、发送）
@author:walle
@file:保存处理事件的demo.py
@time:2021/04/30 16:46:59
@description: 
"""


def demo():
    """
    记录在线过程的所有记录（接收、识别、审核、后处理、校验、发送）的事件。
    本例的事件是接收文件成功事件。
    :return:
    """
    ...  # your code
    json_dict = {
        "event": "receive_file_success",
        "company_code": "hming",
        "app_code": "hming",
        "account_id": 102,  # 账户的id，不是账户名
        "business_no": "202104290948_hming_hmingapp_00083",
        "oss_key": " 20210322173639_c1cc634003461b8a7f296f322bce5ad0.pdf",
    }
    print(save_event(json_dict=json_dict))


if __name__ == '__main__':
    demo()
    pass
