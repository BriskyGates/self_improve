from functools import singledispatch
class abs:
    def type(self,args):
        ""

class Person(abs):

    @singledispatch
    def type(self,args):
        super().type("",args)
        print("我可以接受%s类型的参数%s"%(type(args),args))

    @type.register(str)
    def _(text):
        print("str",text)

    @type.register(tuple)
    def _(text):
        print("tuple", text)

    @type.register(list)
    @type.register(dict)
    def _(text):
        print("list or dict", text)

Person.type("safly")
Person.type((1,2,3))
Person.type([1,2,3])
Person.type({"a":1})

Person.type(Person,True)

