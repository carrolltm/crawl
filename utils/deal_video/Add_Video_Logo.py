import requests
import pandas as pd 
from fake_useragent import UserAgent
import json
import random
import time  
import os
import moviepy.editor as mp
from moviepy.editor import *
import math
from natsort import natsorted
def combine_two_video(): 
    # 访问 video 文件夹 (假设视频都放在这里面)
    combine_index=1
    for root, dirs, files in os.walk("./viedotest"):
        # 按文件名排序
        # files.sort()
        # 遍历所有文件
        for file in files:
            # 如果后缀名为 .mp4
            if os.path.splitext(file)[1] == '.mp4':
                # 拼接成完整路径
                filePath = os.path.join(root, file)
                #本地视频位置
                video_source = mp.VideoFileClip(filePath).margin(5)

                #准备log图片
                logo = (mp.ImageClip("logo.jpg")
                        .set_duration(video_source.duration) # 水印持续时间
                        .resize(height=70) # 水印的高度，会等比缩放
                        .margin(opacity=1) # 水印边距和透明度 right=4, top=4, 
                        .set_pos(("right","top"))) # 水印的位置

                final = mp.CompositeVideoClip([video_source, logo])
                # mp4文件默认用libx264编码， 比特率单位bps
                # final.write_videofile("./videoout/{}.mp4".format(combine_index), codec="libx264", bitrate="10000000")
                final.write_videofile("./videoout/{}.mp4".format(combine_index), codec="libx264")
                combine_index+=1

combine_two_video()