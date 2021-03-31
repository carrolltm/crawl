import base64
import time
 
 
def timestamp2datems(timestamp):
    '''
    时间戳转为日期字串，精确到ms。单位s
    :param timestamp:时间戳
    :return:日期字串
    '''
    local_time = time.localtime(timestamp)
    # data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_head = time.strftime("%Y-%m-%d_%H-%M-%S", local_time)
    data_secs = (timestamp - int(timestamp)) * 1000
    dt_ms = "%s.%03d" % (data_head, data_secs)
    # print(dt_ms)
    return dt_ms
 
 
def bit2humanView(bit_val):
    '''
    文件大小bit转为人类易读大小bit、KB、MB
    :param bit_val:字节数值
    :return:人类易读大小和单位
    '''
    is2kb = int(bit_val / 1042)  # 转换为kb取整
    is2mb = int(bit_val / 1024 / 1024)  # 转为mb取整
    is2gb = int(bit_val / 1024 / 1024 / 1024)  # 转为gb取整
    if is2gb is not 0:
        gb_val = bit_val / 1024 / 1024 / 1024
        return "%.2f GB" % gb_val
    if is2mb is not 0:
        mb_val = bit_val / 1024 / 1024
        return "%.2f MB" % mb_val
    if is2kb is not 0:
        kb_val = bit_val / 1024
        return "%.2f KB" % kb_val
    return "%s bit" % bit_val
 
 
def str2base64(pwd_decode_str):
    '''
    明文str转为base64密文
    :param pwd_decode_str: 明文str
    :return: base64密文
    '''
    base64_encrypt = base64.b64encode(pwd_decode_str.encode('utf-8'))
    pwd_encode_str = str(base64_encrypt, 'utf-8')
    return pwd_encode_str
 
 
def base642str(pwd_encode_str):
    '''
    base64密文转为明文str
    :param pwd_encode_str: base64密文
    :return: 明文str
    '''
    base64_decrypt = base64.b64decode(pwd_encode_str.encode('utf-8'))
    pwd_decode_str = str(base64_decrypt, 'utf-8')
    return pwd_decode_str