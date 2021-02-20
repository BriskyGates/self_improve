import os

from loguru import logger


class LoguruUtil():

    def __init__(self, log_site, log_name):
        self.log_abspath = os.path.join(log_site, log_name)

    def loguru_main(self):
        logger.add(self.log_abspath, encoding='utf-8')


if __name__ == '__main__':
    PROJECT_BASE_DIR = '.'
    LoguruUtil(PROJECT_BASE_DIR, 'aaa_cluster.log').loguru_main()
    logger.info('1342')
