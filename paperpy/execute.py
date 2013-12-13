#!/usr/bin/env python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: execute.py
# Author：wangzhe
# E-mail: wangzhehyd@163.com
# Created Time: 2013-11-01
# Version: 1.0
# Description: 
# Copyright: Chemical Biology Research Center
#===========================================================
import sendmail
from config import subject, content
from geturl import geturl
from getpaper import getpaper

def Sendmail(url, email):
    try:
         receiver = [email]
         # 实例化一个geturl类geturl_instance，用geturl方法获取url
         url_instance = geturl(url)
         pdf_link = url_instance.GetUrl()
         # 实例化一个getpaper类getpaper_instance，用getpaper方法下载文献后并返回文献路径作为邮箱附件
         paper_instance = getpaper(pdf_link)
         paper_path = paper_instance.GetPaper()
         # 发送邮件
         attachment = paper_path
         sendmail.SendEmail(receiver,subject,content,attachment)
         return paper_path
    except:
         return False

def Download(url):
    try:
         # 实例化一个geturl类geturl_instance，用geturl方法获取url
         url_instance = geturl(url)
         pdf_link = url_instance.GetUrl()
         # 实例化一个getpaper类getpaper_instance，用getpaper方法下载文献后并返回文献路径
         paper_instance = getpaper(pdf_link)
         paper_path = paper_instance.GetPaper()
         return paper_path
    except:
         return False
