import requests
import pandas as pd 
from fake_useragent import UserAgent
import json
import random
import time  
import emoji   # 对字符串表情符号过滤
import parsel
from lxml import etree
# 导入CSV安装包
import csv
import os
import re # 正则表达式模块
from urllib.parse import unquote  # Url解码模块
from fake_useragent import UserAgent  #UserAgent 是随机产生 ‘User-Agent’
import moviepy.editor as mp
from moviepy.editor import *
import math
from natsort import natsorted
# 拼接两个视频
def combine_two_video(): 
    # 访问 video 文件夹 (假设视频都放在这里面)
    combine_index=1
    two_combine=0
    L= []
    for root, dirs, files in os.walk("./videos"):
        # 按文件名排序
        # files.sort()
        files = natsorted(files)
        # 遍历所有文件  
        for file in files:
            # 如果后缀名为 .mp4
            if os.path.splitext(file)[1] == '.mp4':
                # 拼接成完整路径
                filePath = os.path.join(root, file)
                # 载入本地视频位置
                video_source = mp.VideoFileClip(filePath)   # .margin(5)
                L.append(video_source)
                two_combine +=1
                print("视频名字：{}".format(filePath))
                if two_combine==2:
                    #准备log图片
                    logo = (mp.ImageClip("logo.jpg")
                            .set_duration(video_source.duration) # 水印持续时间
                            .resize(height=70) # 水印的高度，会等比缩放
                            .margin(opacity=1) # 水印边距和透明度 right=4, top=4, 
                            .set_pos(("right","top"))) # 水印的位置
                    final = concatenate_videoclips(L,method="compose")
                    final = mp.CompositeVideoClip([final, logo]) 
                    # mp4文件默认用libx264编码， 比特率单位bps
                    # 还是打算去掉码率，因为码率和视频出来的体积成正比
                    # final.write_videofile("./combine_video/{}.mp4".format(combine_index), codec="libx264", bitrate="10000000")
                    final.write_videofile("./combine_video/{}.mp4".format(combine_index), codec="libx264")

                    combine_index+=1
                    L=[]
                    two_combine =0
combine_two_video()