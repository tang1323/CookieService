# -*- coding: utf-8 -*-
import requests
import os
import time
import pickle
from scrapy import Selector

import settings
import urllib.request
from io import BytesIO
from PIL import Image   # 这是安装pillow包，专门处理图像的
from selenium.webdriver import ActionChains     # 导入鼠标动作链对象
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from services.base_service import BaseService


class LagouLoginService(BaseService):
    name = "lagou"

    def __init__(self, settings):  # 这是封装的

        self.user_name = settings.Accounts[self.name]["username"]
        self.pass_word = settings.Accounts[self.name]["password"]
        # 如果没有cookies才去登录
        chrome_options = Options()  # 实例化这个Options(),要在webdriver.Chrome加上参数
        # chrome_options.add_argument("--headless")  # 这个就是无界面启动selenium，一定要写的
        # chrome_options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug

        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # browser = webdriver.Chrome(
        #     executable_path="D:/DecomPression-File/chromedriver_win32 (2.45-70)/chromedriver.exe")

    # 如果检测到有这个元素，就证明己经登录成功
    # def check_login(self):
    #     try:
    #         # browser.get("https://www.lagou.com/")
    #         browser.find_element_by_css_selector('.unick')
    #         browser.quit()
    #         return True
    #
    #     except Exception as e:
    #         return False

    # 这个函数一定要重载，这是检查返回的状态码是否200，就是拿到我们的cookies去看看是否还有效
    def check_cookie(self, cookie_dict):
        res = requests.get("https://www.lagou.com/", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36"},
                           cookies=cookie_dict, allow_redirects=False)
        if res.status_code != 200:
            return False
        else:
            return True

    # 这个函数一定要重载
    def login(self):

        """
        1.启动chrome（启动之前确保所有的chrome实例己经关闭）
        """

        # try:
        #     browser.maximize_window()
        # except Exception as e:
        #     pass
        browser = webdriver.Chrome(
            executable_path="D:/DecomPression-File/chromedriver_win32 (2.45-70)/chromedriver.exe")

        i = 0
        login_success = False
        while not login_success:
            # 先请求login登 录的页面
            browser.maximize_window()
            browser.get("https://www.lagou.com/")

            # time.sleep(10000)

            if i == 0:
                i += 1
                browser.find_element_by_xpath('//*[@id="changeCityBox"]/ul/li[4]/a').click()
                time.sleep(0.5)

            # 点击登录
            browser.find_element_by_css_selector("ul.passport a.login").click()
            time.sleep(0.5)

            # 用css输入帐号密码，是id就用#,是class就用.，
            # input[type="password"]是指input标签里面有个属性叫type="password"
            # 原本是.forms-top-block forms-top-password，如果有空格就用.连拼接起来
            # 原本是.input login_enter_password HtoC_JS，如果有空格就用.连拼接起来
            browser.find_element_by_css_selector('.forms-top-block.forms-top-password .input.login_enter_password.HtoC_JS').send_keys(self.user_name)
            browser.find_element_by_css_selector('.forms-top-block.forms-top-password input[type="password"]').send_keys(self.pass_word)
            browser.find_element_by_css_selector('.login-btn.login-password.sense_login_password.btn-green').click()
            time.sleep(3)



            """保存图片到本地项目"""
            # page_source就是运行js完后的html网页
            sel_css = Selector(text=browser.page_source)
            # print(sel_css)
            #
            # 这个和bilibili放在一样的路径下,图片标签
            img_urls = sel_css.css(".geetest_item_wrap img::attr(src)").extract()[0]


            # 用urlretrieve(),下载图片验证码到本地项目
            try:
                urllib.request.urlretrieve(img_urls, 'D:/Py-Project/CookieService/lagou_yzm.png')
            except:
                pass

            time.sleep(3)

            """这里是对图片以文件的形式打开，主要是为了获取图片的大小"""
            # 对图片验证码进行提取,取图片标签,geetest_table_box,geetest_item_img
            # 这个也跟bilibili一样，我在这里向上取一级
            img_label = browser.find_element_by_css_selector(".geetest_table_box img.geetest_item_img")

            """
            这个在拉勾可有可无
            但是拉勾有三种验证码，汉字点选和物体识别的图片是放在同样的路径下
            所以打开这个只是计算图片的大小而已
            """
            # 获取点触图片链接
            src = img_label.get_attribute('src')

            # 获取图片二进制内容
            img_content = requests.get(src).content
            f = BytesIO()
            f.write(img_content)

            # 将图片以文件的形式打开，主要是为了获取图片的大小
            img0 = Image.open(f)

            # 获取图片与浏览器该标签大小的比例
            scale = [img_label.size['width'] / img0.size[0],
                     img_label.size['height'] / img0.size[1]]

            """对图片进行识别"""
            # 对接打码平台，识别验证码
            from services.common.parse_code import base64_api

            img_path = 'D:\\Py-Project\\CookieService\\lagou_yzm.png'

            # 与接口对应
            code_result = base64_api(settings.KXB_USERNAME, settings.KXB_PASSWORD, img_path)
            print("验证码识别结果：", code_result)

            # 识别出来的坐标是用|隔开的，现在分隔一下
            result_list = code_result.split('|')

            position = [[int(j) for j in i.split(',')] for i in
                        result_list]  # position = [[110,234],[145,247],[25,185]]
            for items in position:  # 模拟点击

                # 实现动作链,browser是浏览器的一个对象
                # move_to_element_with_offset()翻译是移动到带偏移的元素
                # img_label是图片的标签，也是验证码在登录时候的位置
                # perform()是执行整个鼠标动作链
                ActionChains(browser).move_to_element_with_offset(img_label, items[0] * scale[0],
                                                                       items[1] * scale[1]).click().perform()
                time.sleep(1)

            # 点击确认
            browser.find_element_by_css_selector('div.geetest_commit_tip').click()
            time.sleep(3)
            # 点击登录
            try:
                browser.find_element_by_css_selector(
                    ".login-btn.login-password.sense_login_password.btn-green").click()
            except:
                pass

            time.sleep(3)
            # page_source就是运行js完后的html网页
            # res_css = Selector(text=browser.page_source)
            # return res_css

            if browser.find_element_by_css_selector('.unick'):
                login_success = True

        # 用get_cookies()获取cookies,变里获取的是一个对象
        Cookies = browser.get_cookies()
        print("保存cookies到redis中。。。")
        cookie_dict = {}

        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        browser.quit()
        return cookie_dict


if __name__ == "__main__":

    lagou = LagouLoginService(settings)
    cookie_dict = lagou.login()
    print(cookie_dict)




















