# -*- coding: UTF-8 -*-  
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header



def send_mail(content):
    mailto_list = ['yuanfeng20000@163.com']  # 收件人(列表)
    mail_host = "smtp.163.com"  # 对方邮箱的smtp服务器地址，这里是163的smtp地址
    mail_user = "yuanfeng20000"  # 用户名
    mail_pass = "***"  # 密码
    mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com
    sender = 'yuanfeng20000@163.com'

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "Myself"+"<"+mail_user+"@"+mail_postfix+">"
    message['To'] =  Header(sender, 'utf-8')
    message['Subject'] = Header('微信公众号注册申请', 'utf-8')
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host,25)                            #连接服务器  
        server.login(mail_user,mail_pass)               #登录操作  
        server.sendmail(sender, mailto_list, message.as_string())
        server.close()  
        return 'done!' 
    except Exception as e:
        print(str(e))
        return 'failed'  


# print(send_mail("15073377816 向玉卉 省公司 网络安全室"))  #邮件主题和邮件内容
