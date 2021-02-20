from functools import wraps


class PlayFun():
    def __init__(self, data):
        self.data = data

    def check_empty(func):
        @wraps(func)
        def wrapper(self):
            if not self.data.strip():  # 在此处直接访问某个实例属性
                return ''
            result = func(self)
            return result

        return wrapper

    @check_empty
    def fun_main(self):
        print(f'I am {self.data}, pls call loverly')
        return '喵喵'


if __name__ == '__main__':
    # res = PlayFun().fun_main('   ')
    # res = PlayFun('vendor').fun_main()
    res = PlayFun(' ').fun_main()
    print(res)
