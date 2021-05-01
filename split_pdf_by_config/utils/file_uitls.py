import glob
import os
import re
from pathlib import PurePath
import random


class PathDetails():
    """
    # 获取文件获取文件路径相关信息
    """

    def __init__(self, file_path, doc_type=''):
        self.file_path = file_path
        self.pp = PurePath(file_path)
        self.base = self.pp.name
        self.doc_type = '_' + doc_type if doc_type else ''
        self.file_name = os.path.splitext(self.base)[0]
        self.type = os.path.splitext(self.base)[-1]
        self.file_dir = self.pp.parents[0]


def handle_image_file(filename):
    image_filename_pattern = 'image\d+\.[a-z]{3}'
    result = re.match(filename, image_filename_pattern, re.I)
    if result is not None:
        return True
    else:
        return False


class FolderOperation():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.check_exists_folder(self.folder_path)

    @staticmethod
    def check_exists_folder(folder_path_customize):
        exists_status = os.path.exists(folder_path_customize)
        if not exists_status:
            os.makedirs(folder_path_customize)

    def file_compete_path(self, file_path):
        return os.path.join(self.folder_path, file_path)

    def travel_folder(self):
        file_list = os.listdir(self.folder_path)
        all_file_list = list(map(self.file_compete_path, file_list))
        return all_file_list

    # def fetch_identify_result(self):
    #     # ext = 'CN_*.xls*'
    #     ext = ""
    #     file_list = glob.glob(os.path.join(self.folder_path, ext))
    #     if len(file_list) > 1:
    #         all_log.info(f'出现多个识别结果, 请删除至一个结果哦{file_list}')
    #         return -1
    #     # print(file_list)
    #     return file_list

    def fetch_specific_files(self, pattern):
        file_list = glob.glob(os.path.join(self.folder_path, pattern))
        return file_list

    def fetch_pdf_files(self):  # 获取所有pdf文件
        ext = '*.[pP][dD][fF]'
        file_list = glob.glob(os.path.join(self.folder_path, ext))
        # print(file_list)
        return file_list

    def fetch_specific_xlsx(self):
        specific_xlsx_pattern = '*SH_Export Documents.xlsx'
        file_list = glob.glob(os.path.join(self.folder_path, specific_xlsx_pattern))
        # print(file_list)
        return file_list


if __name__ == '__main__':
    mypatg = r'C:\Users\Epiphony\Desktop\UTC2020年11月17日\cs01.dsv2020-11-17T142345SGNB004115150_gm 未提取_ONE\attachment'
    fo = FolderOperation(mypatg)
    # fo.fetch_identify_result()
    # temp = 'print data.pdf'
    # handle_same_filename(temp)
    # fo = FolderOperation(
    #     r'C:\Users\Epiphony\Desktop\海进_归类\HENKEL\详细文件\海进_2020年11月12日\alice.xin2020-11-12T114224转发 FWU20398\attachment')
    # fo.fetch_specific_xlsx()
    # PathDetails(r"C:\Users\Administrator\Desktop\海进_测试数据\Bill Of Lading - HAMA58351.PDF")
    # pd = FolderOperation(
    #     r"C:\Users\Administrator\Desktop\海进2020年11月11日_客户数据\alice.xin2020-11-11T141436U201089 S333\attachment")
    # pd.fetch_pdf_files()
