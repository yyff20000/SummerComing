# -*- coding:utf8 -*-
import os, time
from flask import Flask, g, request, make_response, render_template, send_from_directory
# import basic
import hashlib
import receive, reply
import msg_handle

app = Flask(__name__)
app.debug=True


@app.route("/", methods=['GET'])

def root():
    return render_template('download.html')


@app.route('/wx', methods = ['GET', 'POST'])

def index():
    if request.method == 'GET':
        token = '***' # your token
        query = request.args  # GET 方法附上的参数
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if ( hashlib.sha1(s).hexdigest() == signature ):
            return make_response(echostr)
        else :
            return 'not equals'
    elif request.method == 'POST':
        webData = request.data
        # print("Handle Post webdata is ", webData)
        # return webData
        recMsg = receive.parse_xml(webData)
        if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text': # 向用户返回相应的content
        # if recMsg.MsgType == 'text':
            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            content = msg_handle.msgHandle(recMsg) # 向msgHandle传入recMsg结构
            replyMsg = reply.TextMsg(toUser, fromUser, content)
            return replyMsg.send()
        else:
            print("暂且不处理")
            return "success"


@app.route('/contact', methods = ['GET'])

def contact():
    return render_template('contact.html')


# 配置文件下载路由
@app.route("/download/<filename>", methods=['GET'])

def download_file(filename):
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    directory = os.getcwd()  # 假设在当前目录
    if filename=='1':
        response = send_from_directory(directory, 'static/offline_x64.exe', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-msdownload'
    elif filename == '2':
        response = send_from_directory(directory, 'static/offline_x86.exe', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-msdownload'
    elif filename == '3':
        response = send_from_directory(directory, 'static/syslog配参考置V1.41.doc', as_attachment=True)
        response.headers['Content-Type'] = 'application/msword'
    elif filename == '4':
        response = send_from_directory(directory, 'static/**平台申请工单操作手册-20170705.doc', as_attachment=True)
        response.headers['Content-Type'] = 'application/msword'
    elif filename == '5':
        response = send_from_directory(directory, 'static/**平台账号&VPN申请表-分公司（20170426模板）.docx', as_attachment=True)
        response.headers['Content-Type'] = 'application/msword'
    elif filename == '6':
        response = send_from_directory(directory, 'static/**平台账号&VPN申请表-省公司（20170426模板）.docx', as_attachment=True)
        response.headers['Content-Type'] = 'application/msword'
    elif filename == '7':
        response = send_from_directory(directory, 'static/**安全合规操作说明文档.doc', as_attachment=True)
        response.headers['Content-Type'] = 'application/msword'
    elif filename == '8':
        response = send_from_directory(directory, 'static/***安全管控平台应用资源授权调研表-V2.xls', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-xls'
    elif filename == '9':
        response = send_from_directory(directory, 'static/**申请模板.xlsx', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-xls'
    elif filename == '10':
        response = send_from_directory(directory, 'static/模板：程序帐号登记.xlsx', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-xls'
    elif filename == '11':
        response = send_from_directory(directory, 'static/模板：应急终端登记.xlsx', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-xls'
    elif filename == '12':
        response = send_from_directory(directory, 'static/**模板.xlsx', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-xls'
    elif filename == '13':
        response = send_from_directory(directory, 'static/**平台申请表.xls', as_attachment=True)
        response.headers['Content-Type'] = 'application/x-xls'
    else:
        response = "No such file !"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

