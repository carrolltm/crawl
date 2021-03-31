from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from selenium.webdriver.support.wait import WebDriverWait
import re
from lxml import etree
from time import sleep



def wait(driver, method, path):
    WebDriverWait(driver, 15).until(ec.presence_of_all_elements_located((method, path)))
url = 'https://passport.bilibili.com/login'
# 驱动路径按实际情况填写
browser= webdriver.Chrome(r'D:\Anaconda\acon\chromedriver.exe')

browser.get(url)
browser.find_element_by_css_selector('a[class="btn qq"]').click()  # 点击“QQ账号登录”
wait(browser, By.CSS_SELECTOR, '.lay_login_form iframe')
browser.switch_to.frame("ptlogin_iframe")  # 切换入登录界面
wait(browser, By.CSS_SELECTOR, '.qlogin_list a')
browser.find_element_by_css_selector('a[class="face"]').click()  # 点击QQ头像
time.sleep(30)
