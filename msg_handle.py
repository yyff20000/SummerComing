# -*- coding:utf8 -*-
# import self_handle_redis_part
import redis_handle
import error_handle
import receive
import search_handle

# xml = '<xml><ToUserName><![CDATA[wx1954194c36b26a40]]></ToUserName><FromUserName><![CDATA[test]]></FromUserName><CreateTime>1507866276465</CreateTime><MsgType><![CDATA[text]]></MsgType><MsgId><![CDATA[23523535345]]></MsgId></xml>'
# recMsg = receive.parse_xml(xml)
WEIXINID = 'oDFHUv8_F7PVZc0oMrVjlBrlMKto' # 电脑微信
# WEIXINID = 'oDFHUvzLomHn8Yf_37cEIpd7_X9s' # 手机微信号
# WEIXINID = 'oDFHUvyIwbdfm62_WU7amhnR12CM' #XYH

USAGE = '''
  ==本报障平台使用方式如下==
     
[ 1 ] 查看某篇解决方案，若未加文章id则按热度排列:
发送：查询 文章id/故障描述

[ 2 ] 提交故障描述，系统将自动为您匹配可能的解决方案:
发送：报障 具体的故障描述，包括......

[ 3 ] 管理员对未解决报障问题进行人工回复:
发送：回复 id 故障解决方案
'''


def reg(msg, redis_conn, weixinId): # 用户注册功能
    # 输入格式检测
    error_msg = error_handle.redis_register_format(msg)
    if error_msg == True:
        if not redis_handle.is_registered(redis_conn, weixinId):  # 检测数据库 user: 结构中是否存有该用户的微信id
            if redis_handle.getNameFromPhone(redis_conn, msg[1]) != msg[2]:
                return "[ ! ] 注册失败，手机号与姓名校验不匹配。\n" + \
                       '[ ! ] 请发送如下格式信息完成注册：\n\n' \
                       '注册 联系方式 姓名'
            # 执行注册操作
            redis_handle.register(redis_conn, msg, weixinId)
            return '[ * ] 注册成功，祝您使用愉快。 \n ' + USAGE
        else:
            # 已经注册过
            return '[ * ] 您已执行过注册操作啦~ \n' + USAGE

    else:  # 输入格式检测未通过
        return '[ ! ] 发生错误！\n' + '[ ! ] 错误信息为 : ' + error_msg + '\n' \
               '[ ! ] 请发送如下格式信息完成注册：\n\n' \
            \
               '注册 联系方式 姓名'


def check(msg, redis_conn, weixinId): # 查看文章
    try:
        if len(msg) == 1: # 未传入文章id
            if weixinId == WEIXINID:  # 若为管理员登录，则返回所有待回复文章的id
                return redis_handle.admin_check(redis_conn,)
            else:
                return redis_handle.user_check(redis_conn, weixinId,)
        elif len(msg) == 2 :
            if error_handle.is_article_num(msg[1])  :
                if redis_handle.is_article(redis_conn, msg[1]) | redis_handle.is_admin_article(redis_conn,msg[1]): # 输入 [查看 id] 获取某文章内容
                    if weixinId == WEIXINID:  # 管理员登录
                        return redis_handle.admin_check(redis_conn, msg[1])
                    else:
                        return redis_handle.user_check(redis_conn, weixinId, msg[1])
                else:
                    return '未找到对应文章'
            else :
                return search_handle.match(redis_conn, msg[1])
        else:
            return "查询格式发生错误，请检查后重新输入"
    except Exception as e:
        return 'checkError'+str(e)


def report(msg, redis_conn, weixinId): # 用户报障
    if len(msg) != 2 :
        return "报障参数错误，请检查格式"
    elif len(msg[1]) < 10 :
        return "问题描述长度过短，请提供详细的问题描述"
    try:
        return "文章id为 " + redis_handle.post_article(redis_conn, weixinId, msg[1], )
    except Exception:
        return "出错啦"


def reply(msg, redis_conn, weixinId): # 管理员回复 [!]添加实时推送功能 管理员回复解决方案后自动将消息推送至用户处
    try:
        if weixinId!=WEIXINID:
            return "非管理员没有权限回复"
        elif len(msg) != 3 :
            return "回复参数个数错误，请检查格式"
        elif not redis_handle.is_article(redis_conn, msg[1]):
            return "文章不存在"
        elif len(msg[2]) < 10 :
            return "回复长度过短"
        else:
            return redis_handle.reply(redis_conn, msg[1], msg[2])
    except Exception as e:
        return e

def msgHandle(textMsg): # 主处理函数，传入一个recMsg结构

    weixinId = textMsg.FromUserName
    msg = textMsg.Content.strip().split(' ')
    operation = msg[0] # 获取用户需要进行的操作
    redis_conn = redis_handle.connect() # 连接redis服务器，获取connect对象
    # return weixinId
    if operation == '注册':
        # 用户注册
        return reg(msg, redis_conn, weixinId)

    elif operation == '查询':
        # 判断用户id是否在 user: 中存在
        return check(msg, redis_conn, weixinId)

    elif operation == '报障':
        # 未匹配则返回报障单id，可使用[查看 报障单id]查询回复进度
        return report(msg, redis_conn, weixinId)

    elif operation == '回复':
        # 重复回复问题
        return reply(msg, redis_conn, weixinId )

    else :
        # 无法识别的输入
        msg = '==安管平台报障响应智能系统== \n'
        if not redis_handle.is_registered(redis_conn, weixinId):
            return msg + '\n[ * ] 系统尚未保存您的用户信息，请发送如下格式信息完成注册：\n\n注册 联系方式 姓名 \n如：注册 15088888888 老王'
        else:
            return msg + USAGE
