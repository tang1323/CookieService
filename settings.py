# 超级鹰配置

CJY_USERNAME = "1171242903"
CJY_PASSWORD = "130796abc"

# 快识别平台
KXB_USERNAME = "tang1323"
KXB_PASSWORD = "130796abc"


# redis的相关设置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379


# 各个网站的登陆帐号信息
Accounts = {
    "zhihu": {
        "username": "13232732408",
        "password": "abc713912",
        "cookie_key": "zhihu:cookies",
        # 最大的cookies池
        "max_cookie_nums": 1,
        # 检测cookies的时间间隔
        "check_interval": 30
    },
    "lagou":{
        "username": "13232732408",
        "password": "tang130796",
        "cookie_key": "lagou:cookies",
        "max_cookie_nums": 1,
        "check_interval": 10
    },

    "bili": {
        "username": "13232732408",
        "password": "130796abc",
        "cookie_key": "bili:cookies",
        "max_cookie_nums":1,
        "check_interval":30
    }

}