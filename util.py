#!/usr/bin/python
# coding=utf-8
'''
Date: 2021-01-07 12:00:26
LastEditors: Recar
LastEditTime: 2021-01-10 23:03:39
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# token RALNABTEAPQJPGJA
class SendMail(object):
    def __init__(self, name, html_path):
        msg_from = 'recar_mail@126.com'
        passward = 'RALNABTEAPQJPGJA'
        # msg_to = '1766241489@qq.com'
        msg_to = '18328082337@163.com'
        subject = 'scan结果邮件'
        outputFile = html_path
        outputApart = MIMEApplication(open(html_path, 'rb').read())
        outputApart.add_header('Content-Disposition', 'attachment', filename=outputFile)
        msg = MIMEMultipart()
        msg.attach(outputApart)
        msg[ 'Subject' ] = subject
        msg[ 'From' ] = msg_from
        msg[ 'To' ] = msg_to
        try :
            # s = smtplib.SMTP("localhost")
            s = smtplib.SMTP('smtp.126.com')
            s.login(msg_from, passward)
            s.sendmail(msg_from,msg_to,msg.as_string())
            logger.info( f'{name} 发送成功' )
        except smtplib.SMTPException as e:
            logger.error( f'{name}发送失败{e}')
        finally :
            s.quit()


class Util():

    @staticmethod
    def send_mail(name, html_path):
        pass


