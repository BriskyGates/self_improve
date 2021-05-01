import json
import os
import traceback

import pdfplumber
from PyPDF2 import PdfFileWriter, PdfFileReader
from loguru import logger

from split_constant import *
from utils.file_uitls import FolderOperation
from utils.json_utils import BaseJsonOperation
from utils.loguru_utils import LoguruUtil

LoguruUtil('log', 'split_pdf.log').loguru_main(log_level="ERROR")  # initiate the LoguruUtil class
"""
后期可以根据文件名对应的json 进行分割配置
"""


class SplitPDF(BaseJsonOperation):
    def __init__(self):
        self.result_folder = ""

    def check_config_path(self, config_path_list: list):
        config_data_default = {}
        if not config_path_list:
            # raise Exception('there is no config file,pls add it')
            logger.error('there is no config file,pls add it')
            return config_data_default
        config_path = config_path_list[0]  # 只取第一个json 配置文件路径
        check_status = os.path.exists(config_path)  # 判断是否存在该路径, 防止解析过程中用户删除配置文件
        if not check_status:
            logger.error("we detect the config file, but it doesn't exist")
            return config_data_default
        config_data = self.load_json(config_path)
        return config_data

    def analyze_folder(self):
        """检查文件夹下的每个子文件夹"""
        fo = FolderOperation(UNFINISHED_DIR)
        # fo = FolderOperation(FINISHED_DIR)
        folder_file_list = fo.travel_folder()
        logger.info(folder_file_list)
        for each_file in folder_file_list:
            fo_each = FolderOperation(each_file)
            self.result_folder = os.path.join(each_file, RESULT)  # 在此创建最后的输出目录
            fo_each.check_exists_folder(self.result_folder)
            pdf_file = fo_each.fetch_specific_files("*.pdf")
            config_path = fo_each.fetch_specific_files("*.json")  # 只要有json 文件都取出来
            config_data = self.check_config_path(config_path)
            if not config_data:
                continue
            if len(pdf_file) != 1:  # 只能解析一个pdf 文件
                raise Exception('pdf file must be only one')
            self.split_pdfs(pdf_file[0], config_data)  # 只取第一个pdf 进行分割
        pass

    @logger.catch
    def main(self):
        self.analyze_folder()

    def split_pdfs(self, file_path, config_data):

        pdf_reader = PdfFileReader(file_path)  # 部分pdf 无法正常打开,这边可能分割失败
        for output_name, page_num in config_data.items():
            # file_dirname = os.path.dirname(file_path)
            output_path = os.path.join(self.result_folder, f"{output_name}.pdf")  # 放在result 目录下
            pdf_writer = PdfFileWriter()
            try:
                for each_num in page_num:
                    # Add each page to the writer object
                    # begin with index 0
                    page_info = pdf_reader.getPage(each_num - 1)
                    pdf_writer.addPage(page_info)
                with open(output_path, 'wb') as out:
                    # Write out the merged PDF
                    pdf_writer.write(out)
            except:
                logger.critical(traceback.format_exc())
                logger.error('can not fetch current specified page')  # 一页读取失败, 可能其他页也是同理
                return False


if __name__ == '__main__':
    # 检查unfinished 文件夹中的文件
    # file_path = "8898/4000648898.pdf"
    # file_path = "finished/7880/4000617880.pdf"
    sp = SplitPDF()
    sp.main()
