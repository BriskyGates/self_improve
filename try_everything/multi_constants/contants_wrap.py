from functools import wraps


def check_const(cls):
    @wraps(cls)
    def new_setattr(self, name, value):
        raise Exception('const: {} can not be changed'.format(name))

    cls.__setattr__ = new_setattr  # 检测到对常量进行修复则调用new_setattr()方法
    return cls
