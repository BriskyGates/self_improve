from contants_base import CONST, _Const
import sys

temp = CONST.animal.cat
# CONST.animal.cat="1234"
# temp2=CONST.animal.cat
# CONST.animal.tiger = "123"  # 可是根本没有改变量
"""为什么我会有利用代码加变量的需求?"""
print(temp)
# print(temp2)
sys.modules[__name__] = CONST
print(sys.modules[__name__])


CONST = _Const()
print(id(CONST))