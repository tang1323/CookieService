import requests
import time
from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import settings
from services.common import chaojiying
from services.base_service import BaseService
from mouse import move, click


class ZhihuLoginService(BaseService):
    name = "zhihu"

    def __init__(self, settings):  # 这是封装的

        self.user_name = settings.Accounts[self.name]["username"]
        self.pass_word = settings.Accounts[self.name]["password"]
        # chrome_options = Options()
        #
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # browser = webdriver.Chrome(executable_path="D:/DecomPression-File/chromedriver_win32 (2.45-70)/chromedriver.exe")

    # 如果检测到有这个元素，就证明己经登录成功
    # def check_login(self):
    #     try:
    #         browser.find_element_by_css_selector('.Button.AppHeader-notifications.css-79elbk.Button--plain')
    #         return True
    #
    #     except Exception as e:
    #         return False

    def check_cookie(self, cookie_dict):
        res = requests.get("https://www.zhihu.com", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36"},
                           cookies=cookie_dict, allow_redirects=False)
        if res.status_code != 200:
            return False
        else:
            return True


    def login(self):

        """
        1.启动chrome（启动之前确保所有的chrome实例己经关闭）
        """

        # try:
        #     browser.maximize_window()
        # except Exception as e:
        #     pass
        chrome_options = Options()
        chrome_options.add_argument("--headless")   # 这个就是无界面启动selenium，一定要写的
        chrome_options.add_argument("--disable-gpu")  # 谷歌文档提到需要加上这个属性来规避bug

        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        browser = webdriver.Chrome(executable_path="D:/DecomPression-File/chromedriver_win32 (2.45-70)/chromedriver.exe", options=chrome_options)

        login_success = False
        while not login_success:
            browser.maximize_window()
            browser.get("https://www.zhihu.com/signin?next=%2F")
            browser.find_element_by_xpath(
                "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[1]/div[2]").click()

            browser.find_element_by_xpath(
                '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[2]/div/label/input').send_keys(
                Keys.CONTROL + "a")
            browser.find_element_by_xpath(
                '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[2]/div/label/input').send_keys(self.user_name)

            browser.find_element_by_xpath(
                "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[3]/div/label/input").send_keys(
                Keys.CONTROL + "a")
            browser.find_element_by_xpath(
                "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[3]/div/label/input").send_keys(self.pass_word)
            browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/button').click()
            # if browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[4]/div/div[2]/img') & browser.find_element_by_xpath(
            #             '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[4]/div/span/div/img'):
            #     break
            # else:
            #     time.sleep(3)
            #     while True:
            #         browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/button').click()
            #         has_en = False
            #         has_cn = False
            #         try:
            #             browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[4]/div/div[2]/img')
            #             has_cn = True  # 中文
            #         except:
            #             pass
            #
            #         try:
            #             browser.find_element_by_xpath(
            #                 '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[4]/div/span/div/img')
            #             has_en = True  # 英文
            #         except:
            #             pass
            #
            #         if has_cn or has_en:
            #             break

            time.sleep(2)



            print("正在登录，破解验证码中。。。正在判断是否登录成功")
            # if self.check_login():
            #     break
                # 判断是否成功
            try:
                english_captcha_element = browser.find_element_by_class_name("Captcha-englishImg")  # 如果是英文验证码
            except:
                english_captcha_element = None

            try:
                chinese_captcha_element = browser.find_element_by_class_name("Captcha-chineseImg")  # 如果是中文验证码

            except:
                chinese_captcha_element = None

            # 这个是中文验证码的登录
            if chinese_captcha_element:
                # 精准获取xy坐标
                ele_postion = chinese_captcha_element.location
                x_relative = ele_postion["x"]
                y_relative = ele_postion["y"] + 27

                # 但是他的计算方法并不是从窗口那里开始获取的，所以下面是固定的代码，可以去掉窗口位置,
                browser_navigation_panel_height = browser.execute_script(
                    'return window.outerHeight - window.innerHeight;'
                )  # browser_navigation_panel_height就是地址栏的高度

                # 做一个图片保存转换
                base64_text = chinese_captcha_element.get_attribute("src")
                import base64
                code = base64_text.replace("data:image/jpg;base64,", '').replace("%0A", "")  # 获取文本后的前边的文本替换成空的，但是这个base64和一般的base64不太一样，还多了一段%0A，所以也要替换掉
                # print("这是中文验证码：")
                # print(code)

                fh = open("D:/Py-project/CookieService/yzm_cn.jpeg", "wb")  # 保存这个图片叫yzm_cn.jpg
                fh.write(base64.b64decode(code))
                fh.close()

                from zheye import zheye
                z = zheye()
                positions = z.Recognize("D:/Py-project/CookieService/yzm_cn.jpeg")


                pos_arr = []
                if len(positions) == 2:
                    if positions[0][1] > positions[1][1]:
                        pos_arr.append([positions[1][1], positions[1][0]])
                        pos_arr.append([positions[0][1], positions[0][0]])

                    else:
                        pos_arr.append([positions[0][1], positions[0][0]])
                        pos_arr.append([positions[1][1], positions[1][0]])
                else:
                    pos_arr.append([positions[0][1], positions[0][0]])
                print(pos_arr)

                if len(positions) == 2:
                    # 有两个倒立文字
                    first_position = [int(pos_arr[0][0] / 2),
                                      int(pos_arr[0][1] / 2)]  # 原始图片在zheye项目的相比小一半，所以除以2，这是第一个元素
                    second_position = [int(pos_arr[1][0] / 2),
                                       int(pos_arr[1][1] / 2)]  # 原始图片在zheye项目的相比小一半，所以除以2，这是第二个元素
                    move((x_relative + first_position[0]), (y_relative + browser_navigation_panel_height + second_position[1]) + 6)  # 这是点击第一个元素
                    click()
                    move((x_relative + second_position[0]),
                         y_relative + browser_navigation_panel_height + second_position[1])  # 这是点击第二个元素
                    click()
                else:

                    # 这是有一个倒立文字
                    first_position = [int(pos_arr[0][0] / 2),
                                      int(pos_arr[0][1] / 2)]  # 原始图片在zheye项目的相比小一半，所以除以2，这是第一个元素
                    move((x_relative + first_position[0]), y_relative + browser_navigation_panel_height + first_position[1])  # 这是点击第一个元素
                    click()

                    # 再做一次登录
                # browser.find_element_by_xpath(
                #     "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[1]/div[2]").click()
                # browser.find_element_by_xpath(
                #     "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[2]/div/label/input").send_keys(
                #     Keys.CONTROL + "a")
                # browser.find_element_by_xpath(
                #     "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[2]/div/label/input").send_keys(
                #     self.user_name)
                #
                # browser.find_element_by_xpath(
                #     "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[3]/div/label/input").send_keys(
                #     Keys.CONTROL + "a")
                # browser.find_element_by_xpath(
                #     "//*[@id='root']/div/main/div/div/div/div[1]/div/form/div[3]/div/label/input").send_keys(
                #     self.pass_word)
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/button').click()

            # 英文验证码
            if english_captcha_element:

                # 做一个图片保存转换
                base64_text = english_captcha_element.get_attribute("src")
                import base64

                code = base64_text.replace("data:image/jpg;base64,", '').replace("%0A", "")     # 获取文本后的前边的文本替换成空的，但是这个base64和一般的base64不太一样，还多了一段%0A，所以也要替换掉

                fh = open("D:/Py-project/CookieService/yzm_en.jpeg", "wb")  # 保存这个图片叫yzm_en.jpg
                fh.write(base64.b64decode(code))
                fh.close()

                cjy_cli = chaojiying.Chaojiying_Client(settings.CJY_USERNAME, settings.CJY_PASSWORD, "905526")
                im = open('D:/Py-project/CookieService/yzm_en.jpeg', 'rb').read()
                code = cjy_cli.PostPic(im, 1902)
                print("英文验证码:", code)

                # 做一个while循环，怕一次不成功识别，循环到成功，再做一个break
                while True:
                    if code == "":
                        cjy_cli = chaojiying.Chaojiying_Client('1171242903', '130796abc', '905526')
                        im = open('D:/Py-project/CookieService/yzm_en.jpeg', 'rb').read()
                        code = cjy_cli.PostPic(im, 1902)
                        # print("chaojiyingshibie结果:")
                        # print(code)
                    else:
                        break

                # browser.find_element_by_css_selector('.SignFlow-password input').send_keys(Keys.CONTROL + "a")
                browser.find_element_by_xpath(
                    '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[4]/div/div/label').send_keys(
                    code["pic_str"])

                # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                #     Keys.CONTROL + "a")
                # browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
                #     self.user_name)
                #
                # browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
                # browser.find_element_by_css_selector(".SignFlow-password input").send_keys(self.pass_word)
                # submit_ele = browser.find_element_by_css_selector(".Button.SignFlow-submitButton")
                # 点击登录按钮
                browser.find_element_by_css_selector(".Button.SignFlow-submitButton.Button--primary.Button--blue").click()

                # 等待登录成功后加载个人中心信息
            time.sleep(10)
            if browser.find_element_by_css_selector('.Button.AppHeader-notifications.css-79elbk.Button--plain'):
                login_success = True

        Cookies = browser.get_cookies()
        # print(Cookies)
        print("登录成功，正在保存cookie到redis中.....")
        cookie_dict = {}

        for cookie in Cookies:
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return cookie_dict


# if __name__ == "__main__":
    # import settings

    # zhihu = ZhihuLoginService(settings)
    # cookie_dict = zhihu.login()
    # print(cookie_dict)

    # import requests
    #
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36"
    #
    # }
    # rsp = requests.get("https://www.zhihu.com", headers=headers, allow_redirects=False, cookies=cookie_dict)
    # print(rsp.status_code)
    # print(rsp.text)
