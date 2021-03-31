from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from selenium.webdriver.support.wait import WebDriverWait
import re
from lxml import etree
from time import sleep
import json
web = webdriver.Chrome(r'D:\Anaconda\acon\chromedriver.exe')
web.get('https://www.bilibili.com')
web.delete_all_cookies()#先删除cookies
time.sleep(40)#这个时间用于手动登录,扫码登录可以适当缩短这个等待时间
dictcookies = web.get_cookies()#读取登录之后浏览器的cookies
jsoncookies = json.dumps(dictcookies)#将字典数据转成json数据便于保存

with open('cookie.txt','w') as f:#写进文本保存
    f.write(jsoncookies)
print('cookies is ok')
