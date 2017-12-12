# -*- coding:utf8 -*-
import redis
import time

ONE_WEEK_IN_SECONDS = 24 * 3600 * 7
ONE_MONTH_IN_SECONDS = 24 * 3600 * 30
WATCH_SCORE = 3600 * 12 # 一篇文章被阅读时提升的热度分值
ARTICLE_PER_PAGE = 25 # 每页固定的文章数(可修改)

def connect():
    conn = redis.StrictRedis.from_url(url = '***')
    return conn

# article = 'article:10000'
# conn.zadd('score:', article, 100000000)
# conn.zrem('score:', article)
# print(conn.zscore('score:', article))

def is_registered(conn, weixin_id): # 检查是否注册
    return conn.sismember('users:', weixin_id)


def is_article(conn, article_id): # 检查是否存在该文章
    return conn.sismember('articles:', article_id)


def getTitle(conn, article_id): # 获取文章标题
    return conn.hget('article:'+article_id,'title')


def getContent(conn, article_id): # 获取文章内容
    return conn.hget('article:'+article_id,'content')


def getSolveStatus(conn, article_id):
    return '未解决' if conn.sismember('unsolved:', article_id) else '已解决'


def getReply(conn, article_id): # 获取文章解决方案
    reply = conn.hget('article:'+article_id,'reply')
    return reply if reply != '' else '未解决'

def getArticle(conn, article_id):
    content = getContent(conn, str(article_id))
    title = getTitle(conn, article_id)
    text = '文章id: '+ str(article_id) + \
        '\n文章标题: '+ title +  \
        '\n文章内容：'+ content + '\n\n'
    return text

def getArticleDetail(conn, article_id):
    content = str(getContent(conn,str(article_id)))
    reply = str(conn.hget(name='article:'+article_id, key='reply'))
    text = '文章id: '+ str(article_id) + \
        '\n内容描述: '+ content +  \
        '\n解决方案：'+ (reply if reply != '' else '待解决') + '\n\n'
    return str(text)


def dicToText(conn, dic): # 将字典类型转成输出
    out = ''
    for i in dic.keys():
        out = out + '文章id: ' + str(i) + '\n摘要：' + dic.get(str(i)) + '\n解决状态: ' + getSolveStatus(conn, str(i)) +'\n\n'
    return out


def register(conn, textMsg, weixin_id): # 用户注册
    # 添加 user: 结构中用户
    conn.sadd('users:', weixin_id)
    # 添加 单个用户profile
    conn.hmset('user:' + weixin_id , {
        'corp': textMsg[1],
        'depart' : textMsg[2],
        'name': textMsg[3],
        'phone': textMsg[4],
        'createtime': time.time(),
    })


def post_article(conn, user, content, solution= None): #  发布文章，缺少 [!] 关键字添加功能

    article_id = str(conn.incr('count:')) # 自增获取文章id
    # watch = 'watch:' + article_id
    # conn.sadd(watch, user) # 创建文章热度
    # conn.expire(watch, ONE_MONTH_IN_SECONDS)

    now = time.time()
    article = 'article:' + article_id

    conn.hmset(article, { # 添加文章基本内容
        'title': content[:24]+'...',
        #'link' : link,
        'content': content,
        'poster': user,
        'time': now,
        'watch': 0,
        'reply': solution if solution != None else '' # 管理员回复的解决方案
    })

    # conn.zadd('heat:', article_id, now + WATCH_SCORE) # 根据热度排序集合
    # conn.zadd('time:', article_id, now) # 根据发布时间排序集合

    conn.sadd('articles:', article_id)
    conn.sadd('articles:'+user, article_id)
    if solution == None:
        conn.sadd('unsolved:', article_id)
    return article_id


# def get_articles(conn, page, order = 'heat:'): # order 可取 'heat:' 或 'time:'
#     start = (page - 1) * ARTICLE_PER_PAGE
#     end  = start + ARTICLE_PER_PAGE - 1
#
#     id_set = conn.zrevrange(order, start, end)
#     for id in id_set:
#         article_data = conn.hgetall(id)


def admin_check(conn, id = None): # 管理员输入 查看
    if id == None:
        try:
            unsol = {}
            inter = conn.smembers('unsolved:')
            if len(inter) != 0:
                for i in inter:
                    unsol[i] = getTitle(conn, i)
                return dicToText(conn, unsol)[:-2]  # 返回未解决文章id
            else:
                return "全部故障均已解决！"
        except Exception:
            return "查询出错啦！"
    else:
        return getArticleDetail(conn, id)[:-2] # 返回id对应文章的内容


def user_check(conn, weixinid, id = None):
    if id == None:
        try: # 根据微信id查看报障id
            # return 'lalala'
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
            return e
    else:
        return getArticleDetail(conn, id)[:-2] # 返回id对应文章的内容


def reply(conn, articleId, content):

    try:
        conn.hmset('article:' + articleId,{
            'reply': content
        })
        conn.srem('unsolved:', articleId)
        return '回复成功'
    except Exception as e:
        return e


