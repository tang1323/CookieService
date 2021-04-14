"""这里是启动我们的sever，专门检测cookies是否有效的"""
from server import CookieServer
from services.zhihu import ZhihuLoginService
from services.lagou import LagouLoginService
import settings
import redis


srv = CookieServer(settings)

# 注册需要登录的服务
# srv.register(ZhihuLoginService)
srv.register(LagouLoginService)

# 启动cookie的服务
print("启动cookie服务")
srv.start()







