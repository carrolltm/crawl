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
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(r'D:\Anaconda\acon\chromedriver.exe')
driver.get('https://www.bilibili.com')

f = open('cookie.txt','r')
listcookie = json.loads(f.read())#读取文件中的cookies数据

for cookie in listcookie:
    driver.add_cookie(cookie)#将cookies数据添加到浏览器
driver.refresh()#刷新网页
time.sleep(4)#这个时间用于手动登录,扫码登录可以适当缩短这个等待时间

create_center = driver.find_element_by_xpath("/html[1]/body[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[7]/a[1]/span[1]")  # 点击创作中心
create_center.click() # 模拟点击下一页的时候，会出现一个新窗口或者新标签


HomePage_Handles = driver.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
print('当前句柄: ', HomePage_Handles )  # 会打印所有的句柄
driver.switch_to_window(HomePage_Handles[-1])  # driver切换至最新生产的页面
time.sleep(3)

# 每次首先进入的时候弹出跳过
jump_click=  driver.find_element_by_css_selector("#canvas-wrap > div > div > img")  # 点击创作中心
jump_click.click()
# # 点击投稿 这个应该可以直接点击视频投稿
contribution_button = driver.find_element_by_xpath("//a[@id='nav_upload_btn']")  
contribution_button.click()
time.sleep(3)
# video_contribution = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[3]/div[1]/a[1]')  # 点击视频投稿
# video_contribution.click()
# time.sleep(4)
# 鼠标悬浮移动一下


ActionChains(driver).move_by_offset(100, 200).perform()
time.sleep(10)
#--------------------------------------------
# 现在全是上传本地文件了
from pymouse import PyMouse
from pykeyboard import PyKeyboard
kk = PyKeyboard()
upload_video=driver.find_element_by_css_selector("div.canary-container:nth-child(1) div.upload-v2-container div.upload-v2-step1-container div:nth-child(1) div.upload-btn:nth-child(4) > div.upload-btn-title:nth-child(2)")
upload_video.click()
sleep(1)
kk.tap_key(kk.shift_key) #切换为英文，看实际情况是否需要
sleep(1)
kk.type_string('D:\python\videos')#打开文件所在目录，方便多个文件上传
sleep(1)
kk.tap_key(kk.enter_key)
sleep(1)
kk.type_string('" 这样够显眼了吗 .mp4"')#多文件上传
sleep(1)
kk.tap_key(kk.enter_key)
time.sleep(10)
