import io
import sys
from selenium import webdriver
# sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
chrome_opt=webdriver.ChromeOptions()
# prefs={"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(executable_path="D:/Decompression-File/chromedriver_win32 (2.34-62)/chromedriver.exe",chrome_options=chrome_opt)
browser.get("https://www.baidu.com")
import time
time.sleep(300)
