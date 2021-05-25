import os

from loguru import logger

LOG_DIR = "."


class MyFilter:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):  # record 为每一个要记录的日志对象
        level_no = logger.level(self.level).no  # 查看self.level对应的日志的序号
        return record["level"].no == level_no


class MultiLoguru():
    def __init__(self, log_site, log_name):
        self.log_site = log_site
        self.log_name = log_name

    def main(self):
        log_path_info = os.path.join(self.log_site, f'INFO_{self.log_name}')  # 项目根目录下生成log 文件
        log_path_error = os.path.join(self.log_site, f'ERROR_{self.log_name}')  # 项目根目录下生成log 文件

        logger.add(log_path_info, rotation="500 MB", encoding='utf-8',filter=MyFilter("INFO"))  # Automatically rotate too big file
        logger.add(log_path_error, rotation="500 MB", encoding='utf-8',
                   level='ERROR',filter=MyFilter("ERROR"))  # Automatically rotate too big file


if __name__ == '__main__':
    MultiLoguru(LOG_DIR, 'mysql_file.log').main()
    logger.info("abc")
    logger.error("abc")
