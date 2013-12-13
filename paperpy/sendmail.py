#!/usr/bin/env python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: sendmail.py
# Author：wangzhe
# E-mail: wangzhehyd@163.com
# Created Time: 2013-11-01
# Version: 1.0
# Description: A python script to send email 
# Copyright: Chemical Biology Research Center
#===========================================================
import os, smtplib, mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import email_host, email_user, email_pass, email_postfix

def SendEmail(receiver,subject,content,attachment = None):
    '''
    receiver: email receiver
    subject: email subject
    content: email content
    attachment: email attachment
    sendEmail("receiver@example.com","subject","content","attachment")
    '''
    main_msg = MIMEMultipart()
    text_msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    main_msg.attach(text_msg)

    if attachment != None or os.path.exists(attachment):
        contype,encoding = mimetypes.guess_type(attachment)
    if contype is None or encoding is not None:
        contype = 'application/octet-stream'    
    maintype,subtype = contype.split('/',1)

    file = open(attachment,'rb')
    file_msg = MIMEBase(maintype,subtype)
    file_msg.set_payload(file.read())
    file.close()
    encoders.encode_base64(file_msg)

    basename = os.path.basename(attachment)
    file_msg.add_header('Content-Disposition','attachment',filename = basename.decode('utf-8').encode('gb2312'))
    main_msg.attach(file_msg)

    main_msg['subject'] = subject
    main_msg['from'] = "<"+email_user+"@"+email_postfix+">"
    main_msg['to'] = "; ".join(receiver)  
    try:
        smtp = smtplib.SMTP()
        smtp.connect(email_host)
        smtp.login(email_user,email_pass)
        smtp.sendmail(main_msg['from'],main_msg['to'],main_msg.as_string())
        smtp.close()
        print "Send email to  %s  successfully!" %main_msg['to']
    except Exception, error:
        print 'Send email failed to : %s' % error
        exit()
