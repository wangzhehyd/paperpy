#!/usr/bin/env python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: geturl.py
# Author：wangzhe
# E-mail: wangzhehyd@163.com
# Created Time: 2013-11-23
# Version: 1.0
# Description: 
# Copyright: Chemical Biology Research Center
#===========================================================
import urllib2
import re
import cookielib
from config import convert_rules, redirect_rules

class geturl():
    '''根据提供的url找到文献pdf链接'''
    url = ''

    def __init__(self,url):
        self.url = url

    def CleanUrl(self):
        '''清除url的?和#号后面的文本'''
        url = self.url
        if url.find('?') != -1:
            url = url[:url.find('?')]
            if url.find('#') != -1:
                url = url[:url.find('#')]
        if url.find('#') != -1:
            url = url[:url.find('#')]
            if url.find('?') != -1:
                url = url[:url.find('?')]
        return url

    def ConvertUrl(self):
        '''用正则表达式对给出的url直接替换成文献pdf链接'''
        url = self.CleanUrl()
        try:
            for rule in convert_rules:
                find_rule = re.match(rule[0],url,re.I)
                if find_rule:
                    pdf_link = rule[1]
                    for i,v in enumerate(find_rule.groups()):
                        pdf_link = pdf_link.replace('{{' + str(i) + '}}', v)
                    return pdf_link
        except:
            return False
            

    def GetHtml(self):
        '''返回原始url的html页面内容，为跳转作准备'''
        url = self.CleanUrl()
        request = urllib2.Request(url)
        request.add_header('User-Agent' ,'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0')
        cookie = cookielib.CookieJar()
        cookie_enable = urllib2.HTTPCookieProcessor(cookie)
        opener = urllib2.build_opener(cookie_enable)
        html = opener.open(request).read()
        return html

    def RedirectUrl(self):
        '''用正则表达式匹配返回的html文本，找到跳转链接，用正则表达式把其替换成文献pdf链接'''
        url = self.CleanUrl()
        html =self.GetHtml()
        for rule in redirect_rules:
            find_rule = re.match(rule[0],url,re.I)
            if find_rule:
                find_redirect = re.findall(rule[1], html, re.I)
                if find_redirect:
                    link = find_redirect[0]
                    pdf_link = self.ConvertUrl(link)
                    return pdf_link
                else:
                    return False

    def GetUrl(self):
        '''先调用ConvertUrl函数得到文献pdf链接，没用正则匹配则调用RedirectUrl函数进行跳转'''
        try:
            url = self.ConvertUrl()
            if not url:
                url = self.RedirectUrl()
                if not url:
                    print 'Sorry, could not get the right url!'
            #print url
            return url
        except:
            return False

#单独测试
if __name__ == '__main__':
    nature = geturl('http://www.nature.com/nrc/journal/v13/n12/abs/nrc3621.html')
    nature.GetUrl()
    acs = geturl('http://pubs.acs.org/doi/abs/10.1021/jm301581y?prevSearch=FGFR%2Binhibitor&searchHistoryKey=')
    acs.GetUrl()
    pubmed = geturl('http://www.ncbi.nlm.nih.gov/pubmed/24255716')
    pubmed.GetUrl()
    #sd = geturl('http://www.sciencedirect.com/science/article/pii/S0924933813000217')
    #sd.GetUrl()
    #wiley = geturl('http://onlinelibrary.wiley.com/doi/10.1111/j.1745-7270.2008.00486.x/abstract')
    #wiley.GetUrl()
