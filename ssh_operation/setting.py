import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UP_LOG_DIR = os.path.join(BASE_DIR, 'log')
SYSTEM_CFG_DIR = os.path.join(BASE_DIR, 'config/ssh_config.cfg')
CACHE_PWD_DIR = os.path.join(BASE_DIR, 'config/cache_pwd.json')
IDENTIFY_PROCESS_DIR = os.path.join(BASE_DIR, 'document/项目识别流程masterfile.xlsx')
IDENTIFY_SHEETNAME = '项目识别问题记录'
NAME_COLUMN='D'
SERVER_PATH_COLUMN='E'
if __name__ == '__main__':
    print(BASE_DIR)
