#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import re

from pyvirtualdisplay import Display
from selenium import webdriver

display = Display(visible=0, size=(800, 600)) # 初始化屏幕
display.start()
driver = webdriver.Chrome()  # 初始化Chrome
driver.get('https://mp.weixin.qq.com/profile?src=3&timestamp=1523434057&ver=1&signature=vM-f0gvuj2trYEA5PesbTCEhb*89l3WDzrRYEISyHF2dvMTVxY2VyXAbpOzxdRXy5IoQdVzoID-0CstADlSJyA==')
driver.save_screenshot("test.png")


html  = driver.page_source

text = re.search('msgList = (.*?)seajs', html, re.S).group(1).strip()
str = text[0:-1]
print(str)
jsonList = json.loads(str)['list']

for i in jsonList:
    url = "http://mp.weixin.qq.com"+i['app_msg_ext_info']['content_url']
driver.quit()  # 关闭浏览器