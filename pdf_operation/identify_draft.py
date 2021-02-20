import pdfplumber
from loguru import logger
import re

from constants import *
from file_uitls import FolderOperation


class IdentifyDraft:
    def __init__(self, filename, search_word: list):
        """

        Args:
            filename:
            search_word: 统一用大写
        """
        self.filename = filename
        self.search_word = search_word
        self.page_one_word = ""
        self.page_part_word = ""  # 第一页部分文字
        self.init_read_pdf()

    def init_read_pdf(self):
        with pdfplumber.open(self.filename) as pdf:
            all_page = pdf.pages
            if len(all_page) > 0:
                page_one = all_page[0]  # 只读取第一页的数据来判断是否为草稿件
                self.page_one_word = page_one.extract_text().upper()
            else:
                raise Exception('当前pdf 是空白')

    def loc_word(self):
        """
        定位SHIPPER以前数据看看是否有草稿件关键词
        Returns:

        """
        keyword_shipper = "SHIPPER"
        shipper_res = re.search(keyword_shipper, self.page_one_word, flags=re.I)
        if shipper_res is None:
            raise Exception(f'无法定位关键字{keyword_shipper},源数据为{self.page_one_word[:50]}')
        real_shipper = shipper_res.group()
        shipper_index = self.page_one_word.find(real_shipper)
        self.page_part_word = self.page_one_word[:shipper_index].upper()

    def search_draft_word(self):
        """
        分成部分搜和全局搜
        部分搜采用定位shipper前面的字符,查看是否存在草稿件关键词
        Returns:

        """
        for word in self.search_word:
            if word == 'DRAFT' and word in self.page_one_word:  # 全局搜
                return True
            else:
                self.loc_word()
                if word in self.page_part_word:
                    return True
        else:  # 循环结束未找到代表不是草稿件
            return False


if __name__ == '__main__':
    # fo = FolderOperation(CASES_DIR)
    # pdf_file_list = fo.fetch_specific_files('*.pdf')
    # logger.info(pdf_file_list)
    # for pdf_file in pdf_file_list:
    #     draft_id = IdentifyDraft(pdf_file, search_word)
    #     check_res = draft_id.search_draft_word()
    #     if check_res:
    #         logger.critical('LOVELY DRAFT')
    #     else:
    #         logger.critical('NOT DRAFT')
    pdf_file=r'D:\Agglutinate_Project\pdf_operation\cases\SGOT0060078.pdf'
    draft_id = IdentifyDraft(pdf_file, SEARCH_WORD)
    check_res = draft_id.search_draft_word()
    if check_res:
        logger.critical('LOVELY DRAFT')
    else:
        logger.critical('NOT DRAFT')