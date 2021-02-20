import abc

from setting import UP_LOG_DIR
from utils.loguru_utils import LoguruUtil
from ssh_operation import SSHOperation

LoguruUtil(UP_LOG_DIR, 'command_cluster.log').loguru_main()


class Receiver(object):
    """
    命令接收者，正在执行命令的地方，实现了众多命令函数
    """

    def __init__(self):
        self.ssh_client = SSHOperation()




class Command(object):
    """
    command抽象方法，子类必须要实现execute方法
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute(self):
        pass


class FindCommand(Command):
    """
    find命令类，对命令接收者类中start方法的封装
    """

    def __init__(self, receiver):
        self.receiver = receiver

    def execute(self):
        self.receiver.find()


class Client(object):
    """
    调用命令的客户端
    """

    def __init__(self, command):
        self.command = command

    def command_do(self):  # 为未来多命令做准备
        self.command.execute()


if __name__ == '__main__':
    rece = Receiver()
    find_option = {
        'location': "data/raw_file",
        "name": []  # 可能是多个文件名
    }
    # rece.form_find_option(find_option)
