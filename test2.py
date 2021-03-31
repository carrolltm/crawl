# 主要是需要moviepy这个库
from moviepy.editor import *
import os
from moviepy import editor

# 定义一个数组
L = []
index =0
combine_index =1
videoW =0
videoH=0
# 访问 video 文件夹 (假设视频都放在这里面)
for root, dirs, files in os.walk("./videos"):
    # 按文件名排序
    # files.sort()
    # 遍历所有文件
    for file in files:
        # 如果后缀名为 .mp4
        if os.path.splitext(file)[1] == '.mp4':
            # 拼接成完整路径
            filePath = os.path.join(root, file)
            print("正在拼接的文件名：",file)
            # 载入视频
            video = VideoFileClip(filePath)         
            # 输出 高度 和 宽度
            print(video.size)    
            index =index+1


