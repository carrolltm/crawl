from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from selenium.webdriver.support.wait import WebDriverWait
import re
import emoji
from lxml import etree
from time import sleep
import json
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd 
#  我们这里直接点击投稿，则避免多余操作

driver = webdriver.Chrome(r'D:\Anaconda\acon\chromedriver.exe')

driver.implicitly_wait(20)
driver.get('https://www.bilibili.com')

f = open('cookie.txt','r')
listcookie = json.loads(f.read())#读取文件中的cookies数据

for cookie in listcookie:
    driver.add_cookie(cookie)#将cookies数据添加到浏览器
driver.refresh()#刷新网页
time.sleep(4)#这个时间用于手动登录,扫码登录可以适当缩短这个等待时间

create_center = driver.find_element_by_xpath("//body/div[@id='app']/div[1]/div[1]/div[1]/div[1]/div[3]/div[3]/span[1]/span[1]")  # 点击创作中心
create_center.click() # 模拟点击下一页的时候，会出现一个新窗口或者新标签
time.sleep(1)

HomePage_Handles = driver.window_handles  # 这个时候会生成一个新窗口或新标签页的句柄，代表这个窗口的模拟driver
print('当前句柄: ', HomePage_Handles )  # 会打印所有的句柄
driver.switch_to_window(HomePage_Handles[-1])  # driver切换至最新生产的页面
time.sleep(5)

# 每次首先进入的时候弹出跳过
jump_click=  driver.find_element_by_css_selector("#canvas-wrap > div > div > img")  # 点击跳过指引
jump_click.click()
time.sleep(3)
# # # 点击投稿 这个应该可以直接点击视频投稿
# contribution_button = driver.find_element_by_xpath("//a[@id='nav_upload_btn']")  
# contribution_button.click()
# time.sleep(3)
# video_contribution = driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[3]/div[1]/a[1]')  # 点击视频投稿
# video_contribution.click()
# time.sleep(4)
# 鼠标悬浮移动一下


# ActionChains(driver).move_by_offset(100, 200).perform()
# time.sleep(10)
#--------------------------------------------
# 现在全是上传本地文件了
# 因为上传文件的那部分元素在iframe中，不能直接定位元素

df = pd.read_csv("source_introd.csv")
df_list=df.values.tolist()


# list_ip_len = len(df_list)D:\python\videos\45.mp4


# 多个视频读取
video_index =len(df_list) # 视频的数目
# video_index =16

while(video_index):
    driver.switch_to.frame("videoUpload")  # 3.用name来定位
    upload_video=driver.find_element_by_css_selector("#bili-upload-btn")
    upload_video.click()


    from pykeyboard import PyKeyboard
    kk = PyKeyboard()
    sleep(1)
    kk.tap_key(kk.shift_key) #切换为英文，看实际情况是否需要
    sleep(2)
    input_video=r"D:\python\videos\{}.mp4".format(video_index) 
    kk.type_string(input_video)#打开文件所在目录，方便多个文件上传
    sleep(1)
    kk.tap_key(kk.enter_key)
    sleep(1)
    kk.tap_key(kk.enter_key)

    time.sleep(5)

    # 成功上传文件
    # 上传文件后点击个按钮进行上传----------------------------------------
    # 尝试下拉一段滚动条，让按钮能看到  这个100*450正好能看见类型到标签
    js = "window.scrollTo(100,450)"
    driver.execute_script(js)
    # 点击”转载“
    ZhuanZai=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[1]/div[4]/div[2]/div[2]')
    ZhuanZai.click()
    time.sleep(2)
    # 输入视频来源
    source_link = 'https://www.weibo.com/?category=10011'

    ZhuanZai_locate=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[1]/div[4]/div[3]/div/div/input')
    ZhuanZai_locate.send_keys(source_link )

    # 输入稿件标题
    # 根据视频对应序号得到名字

    csv_ip_local =video_index-1
    # 例如：source_title = '就吃个葡萄，你想咋滴'
    # 我们需要额外进行表情包过滤，因为chrome无法识别表情包
    source_title = re.sub(':\S+?:', ' ', emoji.demojize(str(df_list[csv_ip_local][1])))
    print(source_title)

    Manuscript_title=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[1]/div[6]/div[2]/div/div/input')
    # 里面会自动写视频标题名字：因为我视频用序号标记，所以我视频标题是序号得去掉
    Manuscript_title.send_keys(source_title)
    Manuscript_title.clear()
    Manuscript_title.send_keys(source_title)
    sleep(1)


    # 只选择"搞笑视频"这个分类按钮
    # //*[@id="content-tag-v2-container"]/div[3]/div/div[3]
    # //*[@id="content-tag-v2-container"]/div[3]/div/div[3]
    category_button=driver.find_element_by_xpath('//*[@id="content-tag-v2-container"]/div[3]/div/div[3]')
    time.sleep(1)
    category_button.click()

    # 点击“立即投稿” 实现发布
    source_release=driver.find_element_by_xpath("//span[contains(text(),'立即投稿')]")
    source_release.click()

    time.sleep(4)

    # --------上面是发布过一次------------------

    # 选择"再投一个"按钮
    again_upload=driver.find_element_by_xpath("//a[contains(text(),'再投一个')]")
    again_upload.click()
    time.sleep(3)

    # 这然后又回到原处
    video_index=video_index-1
    time.sleep(40)

time.sleep(20)