import requests
import pandas as pd 
# from fake_useragent import UserAgent
import json
import math
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
from natsort import natsorted
# 目标网站
url='https://www.weibo.com/a/aj/transform/loadingmoreunlogin?ajwvr=6&category=10011&page={}&lefnav=0&cursor=&__rnd=1613310575253'
headers={
    'User-Agent': UserAgent().random,
    'Cookie': 'SUB=_2AkMXRcC6f8NxqwJRmPAVym3haI5xyA3EieKhGTFhJRMxHRl-yT9jqlIftRB6PMXuVbUNvCj3bNrSTEheOHDC7H0XUmmS; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5-ssRgVEBU.1lrvZJBWo3W; SINAGLOBAL=7615478906614.841.1612271508793; _ga=GA1.2.841641562.1612407584; login_sid_t=39ce81ee14fcd5ee50291fd9dcd0ed4f; cross_origin_proto=SSL; _s_tentry=cn.bing.com; UOR=,,cn.bing.com; wb_view_log=1536*8641.25; Apache=4736068754830.531.1613308071009; ULV=1613308071036:7:7:1:4736068754830.531.1613308071009:1612660801868' 
}
# 一:proxies 1.1版本
# 参数类型 proxies = {'协议': '协议://IP:端口号'}
# proxies = {
#             'HTTP': '12.243.13.94:9939'   
#         }
#  这里使用读取csv来获得ip，不用以下方式就注释掉，直接用上面的就可以
df = pd.read_csv("ip_pool.csv")
#  这里直接变成数组格式
# 一:proxies 1.2版本
df_list=df.values.tolist()

# 这个索引是从0开始
# 我们从列表长度中获取随机IP
list_ip_len = len(df_list)
if(list_ip_len):
    csv_ip_local = random.randint(0,list_ip_len-1) # csv中用到第几个Ip了
else:
    csv_ip_local = 0      # 如果ip数目没有的话，其实这个判断没有用，只是方便后面功能留的坑
proxies = {
        # type :ip   行列定位
        df_list[csv_ip_local][0]: df_list[csv_ip_local][1]
    }
# 重新获得随机IP    
def get_randon_ip():
    if(list_ip_len):
        csv_ip_local = random.randint(0,list_ip_len-1) # csv中用到第几个Ip了
    else:
        csv_ip_local=0
        print('已经没有可用的IP地址了')  # 后面可以在这里选择是否重新爬取IP形成代理池
    new_proxies = {
        # type :ip   行列定位
        df_list[csv_ip_local][0]: df_list[csv_ip_local][1]
    }
    return new_proxies
# 获得新的headers
def get_new_header():
    new_headers={

        'User-Agent': UserAgent().random,
        'Cookie': 'SUB=_2AkMXRcC6f8NxqwJRmPAVym3haI5xyA3EieKhGTFhJRMxHRl-yT9jqlIftRB6PMXuVbUNvCj3bNrSTEheOHDC7H0XUmmS; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5-ssRgVEBU.1lrvZJBWo3W; SINAGLOBAL=7615478906614.841.1612271508793; _ga=GA1.2.841641562.1612407584; login_sid_t=39ce81ee14fcd5ee50291fd9dcd0ed4f; cross_origin_proto=SSL; _s_tentry=cn.bing.com; UOR=,,cn.bing.com; wb_view_log=1536*8641.25; Apache=4736068754830.531.1613308071009; ULV=1613308071036:7:7:1:4736068754830.531.1613308071009:1612660801868' 
    }
    return new_headers

def test_proxy(proxy):
    # 测试ip是否可用
    test_url = 'http://httpbin.org/get'
    # 参数类型
    # proxies
    # proxies = {'协议': '协议://IP:端口号'}
    # timeout 超时设置 网页响应时间3秒 超过时间会抛出异常
    try:
        resp = requests.get(url=test_url, proxies=proxy, headers=headers, timeout=3)
        
        # 查看状态码   
        if resp.status_code == 200:
            print(proxy, '\033[31mhttpbin网址测试可用\033[0m')
            return True
            
        else:
            print(proxy, 'httpbin网址测试不可用')
            return False
    # 响应应该类似于没网这种吧，响应403好像也是响应
    except Exception as e:
        print(proxy, '抛出错误：httpbin网址测试不可用')
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
# sum ：想获取的页面数
sum =28

# 1. 创建文件对象
csv_obj = open('source_introd.csv','w',encoding='utf-8',newline='' "")
# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(csv_obj)
# 3. 构建列表头
csv_writer.writerow(["index","name","OpenUrl"])

video_number=1 #下载的第几个视频


# # 判断该视频前面已经下载过
# flag = os.path.isfile('already_upload.csv')
# if flag is False:   # 如果该文件存在
#     continue
# 已经存在的文件
already_upload_filename = "already_upload.csv"
already_upload = pd.read_csv(already_upload_filename)
while(sum):
    #  检测该IP是否有效 对http://httpbin.org/get 进行检测
    print("------------------------------------当前爬取得是第{}个页面--------------------------------".format(sum))
    if test_proxy(proxies):
        
        url=url.format(sum)   
        html_data=requests.get(url=url,headers=headers,proxies=proxies)
        # 设置一个退出标志，如果IP都不可用就会陷入一个死循环
        mark_exit=1

        # 如果该ip地址被屏蔽，从csv文件中获得一个没有被微博屏蔽的IP
        
        if(html_data.status_code!=200):  # 这种判断方式可能会出现 没有访问数据的情况
        # if html_data.content == None:
            proxies=get_randon_ip()

            # 设置一个退出标志，如果IP都不可用就会陷入一个死循环
            mark_exit =50    # 设置循环得到IP测试机会
            while(True): 
                html_data=requests.get(url=url,headers=headers,proxies=proxies)
                if(html_data.status_code!=200):
                    mark_exit =mark_exit-1
                    proxies=get_randon_ip()
                    html_data=requests.get(url=url,headers=headers,proxies=proxies)
                else:
                    break
                if(mark_exit==0):
                    break
        if(mark_exit==0):
            break       
        # 将获取到的Html网页源代码写到返回的html.html中
        # with代表着不使用该文件时就被自动关闭

        # 返回的都是编码好的json数据
        decode_html_data = unquote(html_data.text, 'utf-8')
        try:
            html_data = json.loads(decode_html_data)["data"]  # 这个地方就是json格式了
        except Exception as e:
            print("json 数据出错的原因")
            with open('返回的html.html','wb') as f:
                f.write(bytes(decode_html_data,encoding='utf8'))
            continue
        
        Url_data = re.findall('UG_list_v2 clearfix([\d\D]*?)noopener noreferrer',html_data)  # 这是一个列表: .com参数 unistore(结尾)
        final_url_data=[]
        title_arr=[]
        
        index =1  
        # 前面正则表达式缩小范围，然后获得视频标题和视频Url 
        for url_item in Url_data:
            # url_item = url_item+'视频'
            # url_item = url_item
            # -------------------------获得视频标题------------------------------
            # 去掉html标签性质的，得到的是汉字
            # list_title_s(.*?)的微博视频
            try:
                title_item=re.findall('list_title_s(.*?)视频',url_item)[0]  # 这是一个列表: .com参数 unistore(结尾)
                # for title_item in title_data:

                # 下面是对title数据进行格式处理，删掉一个没必要的文字
                pre = re.compile('>(.*?)<')
                origin_title= ''.join(pre.findall(title_item))
                # 删除这种格式的： 假如过年回家亲戚都说真话(左右两边带井号)
                # 可以不断去match，然后删除 
                # 匹配成功re.search方法返回一个匹配的对象，否则返回None。
                get_search=re.search('#(.*?)#', origin_title)
                while(True):
                    if get_search==None:
                        break
                    origin_title=re.sub(get_search.group(), "",origin_title)
                    get_search=re.search('#(.*?)#',origin_title)
                # 对于为空字符串（也就是得到没有名字得视频就直接去掉）
                if(len(origin_title.strip())!=0):

                    # 字符串去除前后空白符和表情符号
                    origin_title=re.sub(':\S+?:', ' ', emoji.demojize(origin_title.strip()))
                    # 再去掉 &nbsp;
                    origin_title=re.sub('[&nbsp;]','',origin_title)

                    # 在csv中真正判断   # 视频还没有下载过（上传过）
                    if(len(already_upload .loc[already_upload ['name']==origin_title])==0):
                        # 获得视频对外的地址
                        video_open_url =re.findall('视频"(.*?)alt',url_item)[0]  # 这是一个列表: .com参数 unistore(结尾)
                        # 得到 " href="http:\/\/t.cn\/A6tnIOfV" 
                        video_open_url=re.findall('="(.*?)"',video_open_url)[0]  
                        # 得到 http:\/\/t.cn\/A6tnIOfV
                        video_open_url=video_open_url.replace('\\','')
                        # 得到 http://t.cn/A6tnIOfV
                        # 保存到第三列
                    
                        title_arr.append(origin_title)   
                        # 在这里我们对已经对获得视频判断是否前面已经获得过
                        # 拼接字符串和编码,得到视频源地址
                        encode_url=re.findall('video_src=([\d\D]*?)unistore',url_item)[0]
                        url_item = unquote(encode_url, 'utf-8')+'unistore,video'
                        final_url_data.append(url_item)  # 其实都可以不保存
                        # 对上面的url数据进行获取和存储 
                        # 发生异常: TypeError: a bytes-like object is required, not 'str'
                        try:
                            # 别一直死用一个IP，user-agent可以不用经常换
                            proxies=get_randon_ip()   

                            video_data = requests.get(url=url_item, proxies=proxies, headers=headers, timeout=5)
                            
                            # 查看状态码   
                            if video_data.status_code == 200:
                                print( '第{}个Url微博视频链接\033[31m可用,总第{}个下载视频链接\033[0m'.format(index,video_number))


                                # 4. 写入csv文件内容
                                if video_number%2 ==0:
                                    combine_wirte = math.floor(video_number/2)
                                    csv_writer.writerow([combine_wirte,origin_title,video_open_url])
                                video_order= video_number
                                video_number =video_number+1 # 保存的总的视频数+1

                                # 在 already_upload.csv 文件中写入该行
                                already_upload_len = len(already_upload.values.tolist())
                                already_upload.loc[already_upload_len]=[already_upload_len+1,title_arr[index-1],video_open_url]
                                already_upload.to_csv(already_upload_filename ,index=None)

                                # 将获得到的视频存储到文件中
                                with open('videos\\'+str(video_order)+'.mp4','wb') as f:
                                    f.write(video_data.content)
                                    print('下载完成...\n')
                            
                            else:
                                print('第{}个Url微博视频链接不可用'.format(index))
                                # 不可用的话接着获得随机代理
                                proxies=get_randon_ip()
                                headers =get_new_header()
                                
                            index = index+1
                        except Exception as e:
                            
                            print('抛出错误：第{}个Url微博视频链接不可用'.format(index))
                            print(url_item)
                    else:
                        print('the video is already exist,so we need pass!!!')
            except Exception as e:
                print("超出索引的原因:第一次正则表达式里面出现两个noopener noreferrer")
        print('最终解析到视频Url的个数',len(Url_data))
        print('最终解析到视频标题的个数',len(title_arr))
        print()

        # 将解析到的视频Url保存起来
        f = open('最后视频Url.html','w',encoding='utf-8')
        for item_title,item_url in zip(title_arr,final_url_data):
            f.write(item_title+"\n")
            f.write(item_url+"\n")

        f.close()

        sum = sum-1


# 5. 关闭文件
csv_obj.close()

# 加上水印和边框  文件变成combine——vid
combine_two_video()


        


    






