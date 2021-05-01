from pathlib import Path

from loguru import logger
from pyunpack import Archive
import traceback


class HandlePacking():
    def __init__(self, file_path):
        """
        
        Args:
            file_path: 压缩包路径,支持相对/绝对路径
        """
        self.file_path = Path(file_path)
        self.file_suffix = self.file_path.suffix[1:].lower()  # 提取其中的后缀名, 并标准化为小写
        self.folder_path = self.file_path.parent  # folder_path 为file_path的上层目录
    @logger.catch
    def handle_pack_main(self):
        # try:
        Archive(self.file_path).extractall(self.folder_path)
        # except:
        #     traceback.print_exc()
        #     print('无法解压该文件哦,文件路径为{}'.format(self.file_path))


if __name__ == '__main__':

    riyou_path = "20210401 sudan WNK-YH-21-0723托书.rar"
    # riyou_path = "C:/Users/Epiphony/Desktop/Curiosity/Curiosity - 副本.rar1"

    from unrar import rarfile
    rar=rarfile.RarFile(riyou_path)
    temp=rar.namelist()
    pass
    # hp = HandlePacking(riyou_path)
    # hp.handle_pack_main()
    # pass
