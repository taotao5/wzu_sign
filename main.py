# -*- coding: utf8 -*-
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def main_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    result = sign_in()
    title = '今日健康打卡结果'
    if result['errcode'] == 0:
        title += "<提交成功>"
    else:
        title += "<提交失败>"

    ret = send_mail(title, str(result))
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


def sign_in():
    url = "https://lightapp.wzu.edu.cn/api/questionnaire/questionnaire/addMyAnswer"

    # 提交的json, 自己抓包
    payload = ""
    
    # headers通过抓包获取即可， 需要保持原样， 注意Cookie和User-Agent
    headers = {
        'Host': 'lightapp.wzu.edu.cn',
        'Content-Type': 'application/json',
        'Origin': 'https://lightapp.wzu.edu.cn',
        'Cookie': '',
        'Content-Length': '5824',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent':
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 weishao(6.7.5) wsi18n(zh)',
        'Referer':
        'https://lightapp.wzu.edu.cn/questionnaire/addanswer?page_from=onpublic&activityid=2237&can_repeat=1',
        'Accept-Language': 'zh-cn',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload.encode('utf-8'))

    responseBody = json.loads(response.text)
    return responseBody


def send_mail(title, message):
    ''' title:邮件标题'''
    ''' message:邮件正文'''
    my_sender = '******@qq.com'  # 发件人邮箱账号
    my_pass = 'asdasderwegrgr'  # 发件人邮箱授权码，第一步得到的
    my_user = '******@qq.com'  # 收件人邮箱账号，可以发送给自己
    ret = True
    try:
        mail_msg = """
            <p>""" + message + """ </p>
            """
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = formataddr(
            ["TAOTAO", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["TAOTAO",
                                my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = title  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com",
                                  465)  # 发件人邮箱中的SMTP服务器，端口是465，固定的，不能更改
        server.login(my_sender,
                     my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.set_debuglevel(1)
        server.sendmail(my_sender, [
            my_user,
        ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as err:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(err)
        ret = False
    return ret
