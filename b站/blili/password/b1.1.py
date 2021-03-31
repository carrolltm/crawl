# 导入webdriver
import os
import time
 
from selenium.webdriver.support.wait import WebDriverWait
import re
from lxml import etree

from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from func import base642str, str2base64
 
from selenium.webdriver.support import expected_conditions as EC

 
print('000-正在启用selenium...')
# 调用环境变量指定的PhantomJS浏览器创建浏览器对象
driver = webdriver.Chrome(r'D:\Anaconda\acon\chromedriver.exe')
print('000-OK')

url = 'https://passport.bilibili.com/login'
print('111-selenium正在请求页面：%s' % url)
driver.get(url)  # get方法请求页面，获取响应
print('111-请求OK')
 
print("打印标题")
print(driver.title)


# with open('b站/blili/b站登录界面.html','w') as f:
#     f.write(driver.page_source)
#     print('下载完成...\n')
# 通过xpath获取输入框
account = "abcdef"  # 账号
pwd = "MTIzNDU2"    # 密码
input_account = driver.find_element_by_xpath("/html/body/div[@id='login-app']/div[@class='login-app bottom-filling']/div[2]/div[@class='login-box clearfix']/div[@class='login-right']/div[@class='form-login']/div[@id='geetest-wrap']/div/div[2]/div[@class='item username status-box']/input[@id='login-username']")
input_account.send_keys(account)
time.sleep(0.5)
input_pwd = driver.find_element_by_xpath("/html/body/div[@id='login-app']/div[@class='login-app bottom-filling']/div[2]/div[@class='login-box clearfix']/div[@class='login-right']/div[@class='form-login']/div[@id='geetest-wrap']/div/div[2]/div[@class='item password status-box']/input[@id='login-passwd']")
input_pwd.send_keys(base642str(pwd))
time.sleep(0.5)
# 点击登录按钮，弹出图片验证码
one_click = driver.find_element_by_xpath("/html/body/div[@id='login-app']/div[@class='login-app bottom-filling']/div[2]/div[@class='login-box clearfix']/div[@class='login-right']/div[@class='form-login']/div[@id='geetest-wrap']/div/div[@class='btn-box']/a[@class='btn btn-login']")
one_click.click()
time.sleep(1)


wait = WebDriverWait(driver,20) #设置等待时间20秒

gapimg = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_item_img')))
sleep(2)
print(gapimg.size)
gapimg.screenshot(r'./captcha1.png') #将class为geetest_canvas_bg的区域截屏保存
