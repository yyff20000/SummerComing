# -*- coding:utf8 -*-
import redis
import time

# 注意事项
# password强度
# ip限定
# 重命名CONFIG命令 Redis.conf -> rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52

#
# 定义的一些常量

ONE_WEEK_IN_SECONDS = 24 * 3600 * 7
ONE_MONTH_IN_SECONDS = 24 * 3600 * 30
WATCH_SCORE = 3600 * 12 # 一篇文章被阅读时提升的热度分值
ARTICLE_PER_PAGE = 25 # 每页固定的文章数(可修改)

def connect():
    conn = redis.Redis(host='172.93.47.109', port=***, db=0, password='***')

    return conn


def is_registered(conn, weixin_id): # 检查是否注册
    return conn.sismember('users:', weixin_id)

def is_category(conn, category_id): # 检查是否存在类别
    return conn.sismember('categories:', category_id)

def is_article(conn, article_id): # 检查是否存在该文章
    return conn.sismember('articles:', article_id)

def getNameFromPhone(conn, phone):
    return conn.hget("user:" + phone, "name") # user:13388888888 返回weixinid

def getTitle(conn, id, article=True): # 获取文章标题
    return conn.hget(('article:'if article else 'category:')+id,'title')


def getContent(conn, id, article=True): # 获取文章内容
    return conn.hget(('article:'if article else 'category:')+id,'content')


def getSolveStatus(conn, article_id):
    return '未解决' if conn.sismember('unsolved:', article_id) else '已解决'


def getReply(conn, id, article = True): # 获取文章解决方案
    reply = conn.hget(('article:'if article else 'category:')+id,'reply')
    return reply if reply != '' else '未解决'

def getArticle(conn, id, article = True):
    content = getContent(conn, str(id), article)
    title = getTitle(conn, id, article)
    text = '文章id: '+ str(id) + \
        '\n文章标题: '+ title +  \
        '\n文章内容：'+ content + '\n\n'
    return text

def adminGetArticleDetail(conn, id, article = True):
    content = str(getContent(conn,str(id), article))
    weixinid = conn.hget(('article:' if article==True else 'category:')+str(id), 'poster')
    phone = ''.join(conn.smembers('phone:'+str(weixinid)))
    name = conn.hget('user:'+ phone, 'name')
    account = conn.hget('user:'+ phone, 'account')
    corp = conn.hget('user:'+phone,'corp')
    timeOrigin = conn.hget(('article:' if article==True else 'category:')+str(id), 'submitTime')
    submitTime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(float(timeOrigin)))
    reply = str(getReply(conn, str(id), article))
    text =  ('姓名：'+str(name)+'\n公司：'+str(corp)+'\n手机号：'+str(phone)+'\n主账号：'+str(account)+'\n提交时间：'+str(submitTime)) + \
        '\n内容描述: '+ content +  \
        '\n解决方案：'+ (reply if reply != '' else '待解决') + '\n\n'
    return str(text)

def userGetArticleDetail(conn, id, article = True):
    content = str(getContent(conn,str(id), article))
    weixinid = conn.hget(('article:' if article==True else 'category:')+str(id), 'poster')
    phone = ''.join(conn.smembers('phone:' + str(weixinid)))
    timeOrigin = conn.hget(('article:' if article else 'category:')+str(id), 'submitTime')
    submitTime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(float(timeOrigin)))
    reply = str(getReply(conn, str(id), article))
    text =  ('文章id：'+str(id)+'\n提交时间：'+str(submitTime)) + \
        '\n内容描述: '+ content +  \
        '\n解决方案：'+ (reply if reply != '' else '待解决') + '\n\n'
    return str(text)


def dicToText(conn, dic): # 将字典类型转成输出
    out = ''
    for i in dic.keys():
        out = out + '文章id: ' + str(i) + '\n摘要：' + dic.get(str(i)) + '\n解决状态: ' + getSolveStatus(conn, str(i)) +'\n\n'
    return out

def applyForReg(conn, content):
    tempUserId = str(conn.incr('tempUserId:'))
    conn.set('tempUser:'+tempUserId+':', content)
    conn.sadd('tempUsers:', tempUserId+':'+content)

def passApply(conn, tempUserId):
    content = conn.get('tempUser:'+tempUserId+':') # 获取注册信息
    conn.delete('tempUser:' + tempUserId + ':')
    conn.srem('tempUsers:',tempUserId+':'+content) # 删除临时内容
    contentMsg = content.split(' ')                # 按空格分开
    addUser(conn, contentMsg[0],contentMsg[1],contentMsg[2],contentMsg[3])
    register(conn, contentMsg[:2][::-1], contentMsg[-1])

def delApply(conn, tempUserId):
    content = conn.get('tempUser:' + tempUserId + ':')
    conn.delete('tempUser:' + tempUserId + ':')
    conn.srem('tempUsers:',tempUserId+':'+str(content)) # 删除临时内容

def register(conn, textMsg, weixin_id): # 用户注册
    # 添加 user: 结构中用户
    conn.sadd('users:', weixin_id)
    # 添加weixinId->phone对应表
    conn.sadd('phone:'+weixin_id, textMsg[1])
    # 添加 单个用户profile
    conn.hmset('user:' + textMsg[1] , {
        'weixinId': weixin_id,
        'createtime':time.time()
    })

def addUser(conn, phone, name, corp, account):
    conn.hmset('user:' + phone, {
        'corp': corp,
        'account': account,
        'name': name,
        'phone': phone,
        'createtime': '',
        'articleDuplicate':0
    })

def userPost(conn, user, category_id, content): # 用户报障
    inter = conn.sinter(['articles:'+user,'unsolved:'])
    if inter: # 查看用户是否存在unsolved报障
        if conn.hget('user:'+conn.smembers('phone:'+user).pop(),'articleDuplicate') == '0':
            conn.hmset('user:'+conn.smembers('phone:'+user).pop(),{
                'articleDuplicate': 1
            })
            return '您有未解决的报障，若再次提交，报障将覆盖'
        else: # 已提示过
            conn.hmset('user:' + conn.smembers('phone:' + user).pop(), { # 将警示位设置为0
                'articleDuplicate': 0
            })
            article_id = str(inter.pop())
            before_category_id = str(conn.hget('article:'+article_id,'category'))
            conn.srem('category:'+before_category_id+':articles:', article_id)

    else: # 不存在未解决报障 生成新文章id
        article_id = str(conn.incr('count:')) # 自增获取用户提交的文章id
        conn.sadd('articles:', article_id)  # articles: {1,2,3,4}
        conn.sadd('articles:' + user, article_id)  # articles:oDFHUv8_F7PVZc0oMrVjlBrlMKto  {1,2,3,4}
        conn.sadd('unsolved:', article_id)  # unsolved:   {1,2,3,4}

    conn.sadd('category:' + category_id + ':articles:', article_id)  # category:1:articles: 报障类别为1时的用户文章1

    now = time.time()
    articles = 'article:' + article_id
    description = conn.hget('category:'+category_id,'content')
    conn.hmset(articles, { # 添加文章基本内容
        'title': description,
        'content': content,
        'poster': user,
        'submitTime': now,
        'solveTime':'',
        'watch': 0,
        'reply': '',
        'category': category_id
    })

    # conn.zadd('heat:', article_id, now + WATCH_SCORE) # 根据热度排序集合
    # conn.zadd('time:', article_id, now) # 根据发布时间排序集合

    return '提交报障成功，文章id是：'+article_id+'。输入[查询 '+article_id+']查看详细信息'


def adminPost(conn, poster, content, solution, needSubmitOrder = 0): #  管理员发布文章

    category_id = str(conn.incr('count:')) # 自增获取类别id
    now = time.time()
    category = 'category:' + category_id

    conn.hmset(category, { # 添加文章基本内容
        'title': content[:24]+'...',
        'content': content,
        'poster': poster,
        'submitTime': now,
        'solveTime':now,
        'watch': 0,
        'reply': solution,
        'category': category_id
    })
    conn.sadd('categories:', category_id)
    if needSubmitOrder == 1:
        conn.sadd('needSubmitOrder:', category_id)

def admin_check(conn, id = None): # 管理员输入 查看 返回类别id下所有文章
    if id == None:
        try:
            unsol = {}
            inter = sorted(conn.smembers('unsolved:'))
            if len(inter) != 0:
                for i in inter:
                    unsol[i] = getTitle(conn, i) # 未解决内容一定在articles:表里
                return dicToText(conn, unsol)[:-2]  # 返回未解决文章id
            else:
                return "全部故障均已解决！"
        except Exception:
            return "查询出错啦！"
    else:
        # print(conn.sismember('articles:',str(id)))
        return adminGetArticleDetail(conn, str(id), (conn.sismember('articles:',str(id))))[:-2] # 返回id对应文章的内容


def user_check(conn, weixinid, id = None):
    if id == None:
        try: # 根据微信id查看报障id
            if not conn.exists('articles:'+ weixinid):
                # return conn.exists('users:')
                return '尚未提交任何报障！'
            unsol = {}
            inter = conn.sinter(['unsolved:','articles:'+weixinid])
            if len(inter) != 0:
                for i in inter:
                    unsol[i] = getTitle(conn, i)
                return dicToText(conn, unsol)[:-2] # 返回未解决文章id
            else:
                return "全部故障均已解决！"
        except Exception as e:
            return 'user_checkError:'+str(e)
    else :
        return userGetArticleDetail(conn, id, (conn.sismember('articles:',id)))[:-2] # 返回id对应文章的内容


def reply(conn, articleId, content):
    try:
        now = time.time()
        conn.hmset('article:' + articleId,{
            'reply': content,
            'solveTime':now
        })
        conn.srem('unsolved:', articleId)
        return '回复成功'
    except Exception as e:
        return 'replyError:'+str(e)


