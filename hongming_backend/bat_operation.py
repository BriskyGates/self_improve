import os
import shutil
from pathlib import Path

from loguru import logger

from hongming_backend.constants import *
from hongming_backend.excel2json import Excel2Json
from pdf_operation.file_uitls import FolderOperation
from universal_constants import FORMAT_TIME


def copy2document(filename):
    if not os.path.exists(DOCUMENT_DIR):
        os.mkdir(DOCUMENT_DIR)
    file_basename = os.path.basename(filename)
    completed_filename = f'{FORMAT_TIME}_{file_basename}'
    dst = os.path.join(DOCUMENT_DIR, completed_filename)  # 加入时间格式
    shutil.copy(filename, dst)
    logger.info(f'{file_basename} 复制到document 文件夹中')


def form_folder_json(folder_path):
    """
    加入缓存机制
    :return:
    """
    fo = FolderOperation(folder_path)
    all_xlsx_file = fo.fetch_specific_files('*.xlsx')
    for xlsx_file in all_xlsx_file:
        Excel2Json(xlsx_file).main()


def main():
    print('按序号来进行操作哦'.center(20, '='))
    print("""1. 生成泓明发票模板 2. 生成泓明提单模板 
3. 生成泓明包装证明模板 4. 将document文件夹下的excel 转换成json""")
    user_input = input('要选择的序号为:')
    user_input_mapping = {  # 字典初始化时就运行下面的代码,一行一行运行
        '1': TEMPLATE_INV_DIR,
        '2': TEMPLATE_BILL_DIR,
        '3': TEMPLATE_IDENTIFY_DIR,
        '4': DOCUMENT_DIR
    }
    user_choice = user_input_mapping.get(user_input)
    if user_input == 4:
        form_folder_json(user_choice)
    else:
        copy2document(user_input)


if __name__ == '__main__':
    main()
