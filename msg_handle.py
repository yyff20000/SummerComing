# -*- coding:utf8 -*-
# import self_handle_redis_part
import receive, traceback
import redis_handle, error_handle, search_handle, mail_handle

WEIXINID = ['oDFHUv8_F7PVZc0oMrVjlBrlMKto'] # 电脑微信

USAGE = '''
  ==本报障平台使用方式如下==
     
[ 1 ] 查看某篇解决方案，若未加文章id则按热度排列:
发送：查询 文章id/故障描述

[ 2 ] 提交故障描述，系统将自动为您匹配可能的解决方案:
发送：报障 类型id(无匹配故障类型请填0) 故障描述(可不填)

[ 3 ] 管理员对未解决报障问题进行人工回复:
发送：回复 id 故障解决方案

<a href="http://172.93.47.109:80/">常用资料下载</a>
<a href="http://172.93.47.109:80/contact">常用管理联系方式</a>
'''
def checkApply(redis_conn): # 查看申请
    if redis_conn.exists('tempUsers:'):
        return '\n'.join(redis_conn.smembers('tempUsers:'))
    else:
        return '暂无注册申请！'

def applyForReg(msg, redis_conn, weixinId): #申请注册
    if len(msg)!=5:
        return "[ ! ] 注册失败，参数数量有误\n" + \
               '[ ! ] 发送如下格式信息完成初始数据录入：\n\n' \
               '注册申请 电话 姓名 公司 主账号'
    elif not error_handle.format(msg[1],2):
        return "[ ! ] 注册失败，电话格式有误"
    else:
        redis_handle.applyForReg(redis_conn,' '.join(msg[1:])+' '+weixinId)
        return '发送成功！请等待管理员校验申请，并于24小时后尝试重新注册。'

def passApply(redis_conn, msg, weixinId): #同意注册
    if weixinId not in WEIXINID:
        return '非管理员，没有操作权限'
    tempUserId = msg[1].split(',')
    for i in tempUserId:
        redis_handle.passApply(redis_conn, i)
    return '添加用户成功'

def delApply(redis_conn, msg, weixinId): #删除注册信息
    if weixinId not in WEIXINID:
        return '非管理员，没有操作权限'
    tempUserId = msg[1].split(',')
    for i in tempUserId:
        redis_handle.delApply(redis_conn, i)
    return '删除信息成功'

def reg(msg, redis_conn, weixinId): # 用户注册功能
    # 输入格式检测
    error_msg = error_handle.redis_register_format(msg)
    if error_msg == True:
        if not redis_handle.is_registered(redis_conn, weixinId):  # 检测数据库 user: 结构中是否存有该用户的微信id
            if redis_handle.getNameFromPhone(redis_conn, msg[1]) != msg[2]:
                return "[ ! ] 注册失败，无匹配的用户数据\n" + \
                       '[ ! ] 发送如下格式信息完成初始数据录入,并等待管理员校验申请,24小时后尝试操作：\n\n' \
                       '注册申请 电话 姓名 公司 主账号'
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
            return redis_handle.check(redis_conn, weixinid = weixinId, isAdmin = (weixinId in WEIXINID), action = 'getUnsolved')
        elif len(msg) >= 2 :
            if error_handle.is_article_num(msg[1])  : # 是数字
                if redis_handle.is_article(redis_conn, msg[1]) | redis_handle.is_category(redis_conn,msg[1]): # 输入 [查看 id] 获取某文章内容
                    if weixinId in WEIXINID:  # 管理员登录
                        return redis_handle.check(redis_conn, id = msg[1], isAdmin = True, action='getArticle')
                    else:
                        return redis_handle.check(redis_conn, weixinid = weixinId, id = msg[1], action='getArticle')
                else:
                    return '文章id有误，未找到对应文章'
            elif msg[1] == 'ALL' :
                return redis_handle.check(redis_conn, weixinid = weixinId, isAdmin = (weixinId in WEIXINID), action = 'getALL') # 查询 ALL
            else:
                return search_handle.match(redis_conn, ''.join(msg[1:])) + '\n\n若无相符合的故障场景，请输入[报障 1 故障信息(包括ip、资源名称、故障详细情况描述等)]'
        else:
            return "查询格式发生错误，请检查后重新输入"
    except Exception as e:
        traceback.print_exc()
        return 'checkError'+str(e)


def report(msg, redis_conn, weixinId): # 用户报障
    if len(msg) < 3 :
        return "参数个数不得小于3，请输入[帮助]核对报障格式"
    if not (redis_conn.sismember('categories:', msg[1])) :
        return '未查询到分类：'+msg[1]+'，请检查参数内容'
    if redis_conn.sismember('needSubmitOrder:', msg[1]):
        if not error_handle.format(msg[2],4):
            return 'IP格式出错'
        elif len(msg) != 4:
            return '格式错误,请按[报障 类型id IP 资源名称]的格式发送报障信息'
    try:
        return redis_handle.userPost(redis_conn, weixinId, msg[1], ' '.join(msg[2:]))
    except Exception as e:
        return e


def reply(msg, redis_conn, weixinId): # 管理员回复 [!]添加实时推送功能 管理员回复解决方案后自动将消息推送至用户处
    try:
        if weixinId not in WEIXINID:
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

    msgRet = '==安管平台报障响应智能系统== \n'

    if operation == '注册申请':
        return applyForReg(msg, redis_conn, weixinId)

    if operation == '注册':
        # 用户注册
        return reg(msg, redis_conn, weixinId)

    if not redis_handle.is_registered(redis_conn, weixinId):
        return msgRet + '\n[ * ] 系统尚未保存您的用户信息，请发送如下格式信息完成注册：\n\n注册 联系方式 姓名 \n如：注册 15088888888 老王'

    if operation == '查询申请':
        return checkApply(redis_conn)

    if operation == '同意':
        return passApply(redis_conn, msg, weixinId)

    if operation == '删除':
        return delApply(redis_conn, msg, weixinId)

    elif operation == '查询':
        # 判断用户id是否在 user: 中存在
        return check(msg, redis_conn, weixinId)

    elif operation == '报障':
        # 未匹配则返回报障单id，可使用[查看 报障单id]查询回复进度
        return report(msg, redis_conn, weixinId)

    elif operation == '回复':
        # 重复回复问题
        return reply(msg, redis_conn, weixinId )

    else:
        return msgRet + USAGE



