import glob
import os
import re
from pathlib import PurePath
import random


class PathDetails():
    """
    # 获取文件获取文件路径相关信息
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.pp = PurePath(file_path)
        self.base = self.pp.name

    def save2txt(self):
        pass


class FolderOperation():
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.folder_dirname = os.path.dirname(folder_path)

    def file_compete_path(self, file_path):
        return os.path.join(self.folder_path, file_path)

    def travel_folder(self, is_full=True):
        all_file_list = os.listdir(self.folder_path)
        if is_full:
            all_file_list = list(map(self.file_compete_path, all_file_list))
        return all_file_list

    def fetch_specific_files(self, pattern):
        file_list = glob.glob(os.path.join(self.folder_path, pattern))
        return file_list


if __name__ == '__main__':
    mypatg = r'C:\Users\Epiphony\Desktop\UTC2020年11月17日\cs01.dsv2020-11-17T142345SGNB004115150_gm 未提取_ONE\attachment'
    fo = FolderOperation(mypatg)
