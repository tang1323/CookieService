"""在这里的函数，必须要重载它，不然会报错"""
import abc


# 元类编程
class BaseService(metaclass=abc.ABCMeta):
    # 1.第一种解决方案： 在父类的方法中抛出异常
    # 2.第二种解决方案： 使用抽象基类（推荐）
    @abc.abstractclassmethod
    def login(self):
        # raise NotImplementedError
        pass

    @abc.abstractclassmethod
    def check_cookie(self, cookie_dict):
        pass






# 测试
class Lagou(BaseService):
    name = "lagou"

    # 强制性的效果
    def login(self):
            print("login in {}".format(self.name))


if __name__ == "__main__":
    l = Lagou()
    l.login()










