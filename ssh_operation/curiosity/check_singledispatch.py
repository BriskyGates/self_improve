from functools import singledispatch

@singledispatch
def connect(address):
    print(f' 传输参数类型为：{type(address)}，不是有效类型')

@connect.register(str)
def _(address):
    ip, port = address.split(':')
    print(f'参数为字符串，IP是：{ip}, 端口是：{port}')

@connect.register(tuple)
def _(address):
    ip, port = address
    print(f'参数为元组，IP是：{ip}, 端口是：{port}')