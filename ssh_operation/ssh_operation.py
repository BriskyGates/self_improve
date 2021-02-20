import paramiko
from loguru import logger

from setting import *
from utils.new_json_uitls import JsonOperation
from utils.handle_data import HandleData
from utils.loguru_utils import LoguruUtil
from config.fetch_config import CfgOperation


class SSHOperation():
    LoguruUtil(UP_LOG_DIR, 'ssh_operation.log').loguru_main()

    def __init__(self):
        self.ssh_config = CfgOperation(SYSTEM_CFG_DIR, 'ssh').read_config()
        self.ssh_client = None
        self.final_result = ''  # 远程服务器执行命令后, 返回成功字符串
        self.hd = HandleData()
        self.name_result = {}  # 记录某次查询的服务器字符串

    @logger.catch
    def connect(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**self.ssh_config)  # 可以进行批处理, 不要每次查询都连接远程服务器
        self.ssh_client = ssh  # 通过ssh连接上linux 服务器

    def close(self):
        self.ssh_client.close()

    def find_by_option(self, option: dict):
        """
        ACHIEVEMENT:
            对find 的命令添子弹, 例如执行查找路径,参数条件,例如-name xxx.pdf
            可能在找的时候要对一些文件名进行排除
        TIPS:
            一次性查找多个文件:  # find . -type f \( -name "*.sh" -o -name "*.txt" \)
        Args:
            find_option: find 函数的参数
        Returns:

        """

        name_list = option.get('name')  # 此处可能会传入多个参数
        if len(name_list) == 0:
            logger.error('name 参数为空哦 :<')
            return False
        find_location = option.get('location', 'data/raw_file')  # location 的默认位置为data/raw_file
        jo = JsonOperation(CACHE_PWD_DIR)
        cache_cwd = jo.load_json()
        for each_name in name_list:  # 可能需要判断each 是否有后缀名
            # 在此处直接查看本地json 缓存机制
            each_pwd = cache_cwd.get(each_name)
            if each_pwd is not None:  # 缓存中存在数据, 不用往linux 服务器中查找
                self.name_result[each_name] = each_pwd
                continue
            after_name = self.hd.deal_name_option(each_name)
            find_cmd = f"find {find_location} -name '{after_name}'"
            # self.connect()
            self.run_shell(find_cmd)  # linux 进行查找命令
            # self.close()
            ssh_search = self.parser_result()  # 解析查询结果
            if ssh_search:
                each_dict = {each_name: ssh_search}
                self.name_result.update(each_dict)  # 查询结果的赋值
                jo.update_json(each_dict)  # 将新查询到的缓存到json

    def parser_result(self):
        if not self.final_result:
            return False
        logger.info(f'以换行符分割前的结果: {self.final_result}')  # 可能需要解析最后结果, 不在这边解析
        final_result_list = self.final_result.split('\n')  # 即使一个字符串不存在\n, 也会变成一个列表其中的一个元素
        logger.info(f'以换行符分割前的结果: {final_result_list}')  # 可能需要解析最后结果, 不在这边解析

        len_final_res = len(final_result_list)  # 本地需要做下缓存
        if len_final_res > 1:
            logger.critical('搜索到多条记录, 我们只取第一条文件对应的服务器路径哦 :>')
        fetch_one = final_result_list[0]
        print(fetch_one)
        return fetch_one

    def check_result(self, cmd_result):
        ssh_in, ssh_out, ssh_error = cmd_result
        error_mes = ssh_error.read()
        if not error_mes:  # 如果error_mes 为空
            self.final_result = ssh_out.read().decode()  # 由byte 转换成str
            logger.info(f'最终执行结果为: {self.final_result}')  # 可能需要解析最后结果, 不在这边解析
            return True
        logger.error('无法搜索到结果哦 :<')
        return False

    def run_shell(self, cmd):
        """
        cmd_result 参数解释:
            元组数据类型
            当cmd 为cd michael 时succ_mes 为空数据,error_mes为 'bash: 第 0 行: cd: michael: 没有那个文件或目录'
            如何路径中存在特殊符号,需要加双引号才能正常搜索到
        Args:
            cmd:

        Returns:

        """
        logger.info(f'开始执行{cmd}')
        cmd_result = self.ssh_client.exec_command(cmd)
        self.check_result(cmd_result)


if __name__ == '__main__':
    """
    调用顺序:
        实例化SSHOperation()
        连接ssh实例
        find_by_option() 传入待识别的pdf 文件名和服务器路径名
        关闭ssh 实例
        
    """
    ssho = SSHOperation()
    ssho.connect()
    # cmd = 'cd dbs;ls'
    # cmd = 'find data/raw_file -name "DYR21T035 托单.*"'
    cmd = 'find ~/data/raw_file -name "InsertPic_(01-20-15-48-40).png"'
    # cmd = 'cd michael'  # bash: 第 0 行: cd: michael: 没有那个文件或目录
    # ssho.run_shell(cmd)
    ssho.find_by_option({'name': ["InsertPic_(01-20-15-48-40).png", "DYR21T035 托单"]})
    print(ssho.name_result)
    # print(res_ssh)
