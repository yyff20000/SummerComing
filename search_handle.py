# -*- coding:utf8 -*-

import jieba
import jieba.posseg as pseg
import redis
import error_handle
import redis_handle

jieba.load_userdict('./word.dic')

# 输入内容 分词 获得名词 存到临时集合中 根据关联程度返回文章摘要和id 查看id 获得文章内容和
def match(redis_conn, userInput):
    try:
        id = 1
        i = 0
        relation = {} # 文章id 与所搜索内容关联度映射表
        out = ''
        if seperate(redis_conn, userInput, 'User') != True: # 首先构造用户输入的分词集
            return 'UserInputError'
        while redis_handle.is_article(redis_conn, str(id)): # 循环获取所有文章的内容
            # print('id:'+str(id))
            articleContent = redis_handle.getContent(redis_conn, str(id)) # 构造了当前文章的分词集
            if seperate(redis_conn, articleContent, 'Db') != True:
                return 'DbInputError'
            # print(redis_conn.sinter(['tmpDbWordList','tmpUserWordList']))
            count = len(redis_conn.sinter(['tmpDbWordList','tmpUserWordList']))
            if count != 0:
                relation[str(id)] = str(count)  # 映射赋值
            id = id + 1
        # print(relation)
        rel = dictSort(relation)
        if rel == {}:
            return '无匹配数据'
        for key in rel.keys():
            if i == 3:
                return out[:-2]
            else:
                i += 1
                if not redis_handle.is_article(conn,key):
                    return out[:-2]
                out += redis_handle.getArticleDetail(conn,key)
        return out[:-2]
    except Exception as e :
        return e

def seperate(redis_conn, content, input): # 构造分词集 input = Db / User 代表数据原有文章内容或用户查询内容
    try:
        if input == None:
            return
        redis_conn.delete('tmp'+input+'WordList')  # 先清零
        forbid = ['uj', 'x', 't', 'v', 'zg', 'd']  # 设置词性过滤表
        wordList = pseg.cut(content)
        for words in wordList :
            if words.flag not in forbid and not error_handle.format(words.word, 3): # 词性过滤、且不是特殊字符
                # print(words.word)
                redis_conn.sadd('tmp'+input+'WordList', words.word)
        return True
    except Exception as e:
        print(e)
        return e

def dictSort(dic): # 按照键值从大到小排序
    try:
        out = {}
        dict = sorted(dic.items(), key=lambda d: d[1], reverse=True)
        for i in dict:
            out[str(i[0])] = str(i[1])
        return out
    except Exception as e:
        return e

# a = {'1': '1', '2':'2'}
# print(dictSort(a))

conn = redis_handle.connect()
print(match(conn,'用户'))
# print(redis_handle.is_article(conn, 'article:1'))

# seg_list = jieba.cut_for_search(abc)  # 搜索引擎模式
# for word, flag in seg_list:
#     print('%s %s' % (word, flag))