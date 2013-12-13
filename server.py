#!/usr/bin/env python
#-*- coding: utf-8 -*-

#===========================================================
# File Name: server.py
# Author：wangzhe
# E-mail: wangzhehyd@163.com
# Created Time: 2013-11-27
# Version: 1.0
# Description: 
# Copyright: Chemical Biology Research Center
#===========================================================
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from paperpy import execute

define("port", default=8080, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class DonePageHandler(tornado.web.RequestHandler):
    def post(self):
        paper_url = self.get_argument('url')
        email_address = self.get_argument('email')
        if paper_url != '' and email_address != '':
            paper_path = execute.Sendmail(paper_url, email_address)
            if paper_path:
                self.render('done.html', url=paper_path, summary='文献已成功发送至 %s 请查收' %email_address.decode('utf-8').encode('gb18030'))
            else:
                self.render('error.html')
        elif paper_url != '' and email_address == '':
            paper_path = execute.Download(paper_url)
            if paper_path:
                self.render('done.html', url=paper_path, summary='请求的文献已下载完成')
            else:
                self.render('error.html')
        else:
            self.render('error.html')

app = tornado.web.Application(
    handlers=[(r'/', IndexHandler), (r'/done', DonePageHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    )

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
