# 1. cookies保存在redis中应该使用什么数据结构
# 2.数据结构应该满足:1.:可以随机获取 2.可以防止重复 - set

import json

# 1. 如何确保每一个网站都会单独的运行
# 2.不是每一个.py都运行,所以要一个专门的服务,需要把运行的服务运行   注册   进来
# 功能:这个服务就是管理这些网站,或者的一个定时检测cookies问题

# 就是一个管理器
from idlelib import browser

import redis
import time
from concurrent.futures import ThreadPoolExecutor, as_completed     # 这是线程池的方法
from functools import partial


class CookieServer():
    def __init__(self, settings):
        # 这是redis客户端的一个连接,decode_responses=True是很重要的
        self.redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)
        # 有多个cls要做,比如知乎或者其他网站,是一个列表,传给register方法
        self.service_list = []
        self.settings = settings

    # 哪一个网站需要做,,,,cls参数的作用:配置cls,把ZhihuLoginService传进来就行了,ZhihuLoginService调用什么方法都知道
    def register(self, cls):
        self.service_list.append(cls) # 把service_list传给cls注册(添加)进来

    # 监听zhihu里的login,监听zhihu里的cookie是否有效,是否满的
    # srv是某一个网站,把它传进来
    def login_service(self, srv):
        while 1:
            # 实例化某一个网站,比如ZhihuLoginService这个网站
            srv_cli = srv(self.settings)
            # 获取要爬取网站的名字
            srv_name = srv_cli.name
            # cookie现在有几个,用scard做一个判断
            cookie_nums = self.redis_cli.scard(self.settings.Accounts[srv_name]["cookie_key"])
            # print("现在有{}个cookie数量".format(cookie_nums))

            # cookie_nums里的cookie小于这个值的时候,,,才有位置让新的cookie装进来
            # max_cookie_nums,每个cookies池的大小都不一样
            if cookie_nums < self.settings.Accounts[srv_name]["max_cookie_nums"]:
                cookie_dict = srv_cli.login()  # 那么就可以登录了,登录后获取得cookie_dict
                # 可以放到redis数据中了,但是每一个网站 的cookie不同,所以要做在settings做一个配置了
                # json.dumps(cookie_dict)列表变成字符串，或者是字典变成变成字符串
                self.redis_cli.sadd(self.settings.Accounts[srv_name]["cookie_key"], json.dumps(cookie_dict))

            else:
                print("{srv_name}的cookies池己满,等待10s".format(srv_name=srv_name))
                time.sleep(6)

    # 检测cookies是否有效的方法
    # srv是某一个网站,比如ZhihuLoginService,把它传进来
    def check_cookie_service(self, srv):
        while 1:
            print("开始检测cookie是否可用 ")
            # 实例化某一个网站,比如ZhihuLoginService这个网站
            srv_cli = srv(self.settings)
            # 获取要爬取网站的名字
            srv_name = srv_cli.name

            # 检测所有的cookie,用redis数据库的smembers来检测， srandmember是随机的一个成员
            all_cookies = self.redis_cli.smembers(self.settings.Accounts[srv_name]["cookie_key"])
            print("目前可用的cookie数量: {}".format(len(all_cookies)))

            for cookie_str in all_cookies:
                # print("获取到cookie: {}".format(cookie_str))   # 打印出现在有哪些cookie
                print("获取到cookie.....不方便展开")
                cookie_dict = json.loads(cookie_str)    # 把cookie_str取出来
                # check_cookie()是我们之前定义的函数
                valid = srv_cli.check_cookie(cookie_dict)   # 检测这些cookie是否有效,放在valid中

                # 如果有效
                if valid:
                    print("cookie有效")

                else:
                    print("cookie已经失效,删除cookie中.......")
                    self.redis_cli.srem(self.settings.Accounts[srv_name]["cookie_key"], cookie_str)

            # 设置间隔，防止出现请求过于频繁，导致本来没失效的cookie失效了
            interval = self.settings.Accounts[srv_name]["check_interval"]
            print("{0}s 后重新开始检测cookie".format(interval))
            time.sleep(interval)

    # 这是线程池,不是多线程
    def start(self):
        # 管理线程池里的一些任务
        task_list = []

        print("启动登录服务")
        # 这里是登录的一个线程池,5个,跳到login_service方法里登录
        login_executor = ThreadPoolExecutor(max_workers=5)
        for srv in self.service_list:

            # submit有几个参数就要传几个参数,但下面的方法能把参数改造成没有
            # task = login_executor.submit(self.login_service, srv)
            # 以下是高级用法
            task = login_executor.submit(partial(self.login_service, srv))
            task_list.append(task)


        print("启动cookie检测服务")
        # 跳到check_cookie_service方法里检测cookie
        check_executor = ThreadPoolExecutor(max_workers=5)
        for srv in self.service_list:
            task = check_executor.submit(partial(self.check_cookie_service, srv))
            task_list.append(task)

        # 防止线程池退出
        for future in as_completed(task_list):
            data = future.result()
            print(data)


























