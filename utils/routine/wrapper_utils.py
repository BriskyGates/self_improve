from functools import wraps

from loguru import logger


def check_empty(return_value=""):
    def first_deco(func):
        @wraps(func)
        def wrapper(self, data: list):  # 适用于类的检查传入参数是否为空
            # 去除args 中的空字符串
            new_args = list(filter(None, data))  # 去除data 中的空字符串
            if not new_args:  # 直接传入filter 对象不行, 必须经过list() 函数处理
                return return_value
            result = func(self, new_args)
            return result

        return wrapper

    return first_deco

def check_class_attr(check_item: list):
    """

    Args:
        check_item: 检查其中的类属性是否为空,eg. ["name","age"]

    Returns:

    """

    def first_deco(func):
        @wraps(func)
        def wrapper(self,*args):
            for item in check_item:  # 如果check_item中某个属性为空,则直接返回,不继续下面操作
                item_value = getattr(self, item)
                if not item_value:  # 一旦存在存在为空数据直接不比较
                    logger.critical(f'the attribute "{item}" of current class is empty :<')
                    return False
            func(self,*args)

        return wrapper

    return first_deco


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:  # cls 为instances中的一个键，该类的构造函数作为值
            instances[cls] = cls(*args, **kwargs)  # 某类的构造方法
        return instances[cls]

    return get_instance


class A(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @check_class_attr(check_item=['name'])
    def print_attr(self):
        print(self.name)
        print(self.age)

        # print(self.__getattribute__(self.name))
        # object.__getattr__(self, name)
        # getattr(self, self.name)


"""
hasattr() and callable() # 这样子来判断的

# 这样子会更好
invert_op = getattr(self, "invert_op", None)
if callable(invert_op):
    invert_op(self.path.parent_op)

"""
if __name__ == '__main__':
    a = A('scar', 'countenance')
    # name=a.__getattribute__('name')
    # print(name)
    a.print_attr()
    # print(getattr(A, 'name', None))
