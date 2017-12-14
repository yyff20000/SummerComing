# -*- coding:utf8 -*-
import re

def format(content, type):
    if type == 1: # 检测是否为全中文
        if  0:# re.match(r'^\w+$', content).group(0):
            return '请输入中文字符!'
        else:
            return True
    elif type == 2: # 检测是否为电话号码
        if not re.findall(r"1\d{10}", content):
            return '手机号码错误!'
        else:
            return True
    elif type == 3: # 检测是否为字符
        if re.findall(r'[~!@#\$\%\^&\*\(\)_\+\-=\{\}\[\]\|\\\:\'\";\<\>.,\?\/\`。，？；：“”‘’]',content):
            return True
    else :
        return '发生了未知错误，请稍后再试!'

def redis_register_format(msg):
    if not len(msg) == 3:
        return '注册参数数量有误!' # + str(len(msg))
    # for i in range(4):
    #     error_msg = format(msg[i], 1)
    #     if not error_msg == True:
    #         return error_msg
    error_msg = format(msg[1], 2)
    return error_msg

def is_article_num(s):
        try:
            a = int(s)
            if a >=0:
                return True
        except ValueError:
            return False
        return False
#
# msg = '注册 所属公司 部门 姓名 13365188628'.split(' ')
# msg = '所属公司aaa'
# print(re.match(r'[A-Za-z0-9]+', msg))

