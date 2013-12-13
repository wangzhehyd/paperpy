#!/usr/bin/env python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: getpaper.py
# Author：wangzhe
# E-mail: wangzhehyd@163.com
# Created Time: 2013-11-28
# Version: 1.0
# Description: 
# Copyright: Chemical Biology Research Center
#===========================================================
import urllib2
import cookielib
import time
from config import proxy_host, proxy_port

class getpaper():
    '''得到文献pdf链接后通过代理下载文献'''
    url = ''

    def __init__(self, url):
        self.url = url

    def SuccessLog(self):
        '''下载成功记录'''
        url = self.url
        f = open('static/papers/download.log', 'a')
        log = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' ' + url + ' succseefully download.' + '\n'
        f.writelines(log)
        f.close()

    def FailureLog(self):
        '''下载失败记录'''
        url = self.url
        f = open('static/papers/download.log', 'a')
        log = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ' ' + url + ' failed download.' + '\n'
        f.writelines(log)
        f.close()

    def GetPaper(self):
        '''通过代理下载文献'''
        paper_url = self.url
        try:
            cookie = cookielib.CookieJar()
            cookie_enable = urllib2.HTTPCookieProcessor(cookie)
            proxy_handler = urllib2.ProxyHandler({"http" : '%s:%s'%(proxy_host, proxy_port)})
            opener = urllib2.build_opener(cookie_enable, proxy_handler)

            paper_content = opener.open(paper_url).read()
            paper_pdf = open('static/papers/%s.pdf'%paper_url.split('pdf').split('/')[-1], 'wb')
            paper_pdf.write(paper_content)
            paper_pdf.close
            print 'Download the paper successfully!'
            self.SuccessLog()
            return 'static/papers/%s.pdf' %paper_url.split('pdf').split('/')[-1]
        except:
            print 'Download the paper failed!'
            self.FailureLog()
            return False

#单独测试
if __name__ == '__main__':
    paper = getpaper('http://pubs.acs.org/doi/abs/10.1021/jm301581y')
    paper.GetPaper()
