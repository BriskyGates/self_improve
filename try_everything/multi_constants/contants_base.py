from contants_wrap import check_const
from constant_animal import _Animal
from constant_platform import _Platform


@check_const
class _Const(object):
    animal = _Animal()
    platform = _Platform()

    def __new__(cls, *args, **kw):  # 单例模式
        if not hasattr(cls, '_instance'):
            orig = super(_Const, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance


CONST = _Const()
print(id(CONST))