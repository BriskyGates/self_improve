import os
from logging import DEBUG

from loguru import logger

# from settings import LOG_DIR
LOG_DIR = "."


class LoguruUtil():
    def __init__(self, log_site, log_name):
        self.log_site = log_site
        self.log_name = log_name

    def loguru_main(self, log_level='INFO'):
        log_abspath = os.path.join(self.log_site, self.log_name)  # 项目根目录下生成log 文件
        logger.add(log_abspath, encoding='utf-8', level=log_level)
        # logger.info('test')


if __name__ == '__main__':
    # LoguruUtil(LOG_DIR, 'xxx.log').loguru_main(log_level='ERROR')
    # logger.info('test loguru utils')
    logger.remove(handler_id=None)  # 清楚之前的设置
    LoguruUtil(LOG_DIR, 'xxx.log').loguru_main(log_level="ERROR")
    logger.info('test')
    logger.debug('test_debug')
    logger.error('test_erro')

"""
当我们设置的日志等级高于我们代码中的日志等级, 低于该日志等级的日志不会写入日志文件中
loguru 默认有一个handler 输出到console 中, 然后通过logger.remove 可以去除默认设置
"""
