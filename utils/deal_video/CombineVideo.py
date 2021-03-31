# 主要是需要moviepy这个库
from moviepy.editor import *
import os
from natsort import natsorted

# 定义一个数组
L = []
index =0
all=1
# 访问 video 文件夹 (假设视频都放在这里面)
for root, dirs, files in os.walk("./testvideo"):
    # 按文件名排序
    # files.sort()
    files = natsorted(files)
    # 遍历所有文件
    for file in files:
        # 如果后缀名为 .mp4
        if os.path.splitext(file)[1] == '.mp4':
            # 拼接成完整路径
            filePath = os.path.join(root, file)
            print(filePath)
            # 载入视频
            video = VideoFileClip(filePath)
            # 添加到数组
            L.append(video)
            index +=1
            if index==2:
                # 拼接视频
                final_clip = concatenate_videoclips(L,method="compose")
                # 生成目标视频文件
                final_clip.to_videofile("./videoinput/{}.mp4".format(all), fps=24, remove_temp=True)

                index =0
                L =[]
                all+=1

