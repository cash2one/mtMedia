#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Create by: Yuanji
# Date Time: 2015-04-22 15:36:00
#
###############################################################################
import uuid
import urllib
import tornado.web
import tornado.ioloop
from settings import *
from tornado import gen
import tornado.httpserver
from tornado.httpclient import *
from handlers.cookiehandler import *
import random, time, os, sys, socket
from utils.log import init_syslog, logimpr, loginfo,logclick, dbg, logwarn, logerr, _lvl
from collections import defaultdict

IMG_FILE = open('./1x1.gif','r')
try:
    IMG_DATA = IMG_FILE.read()
finally:
    IMG_FILE.close()

REFERER = 'Referer'
USER_AGENT = 'User-Agent'

def urlsafe_b64encode(string):
    encoded = base64.urlsafe_b64encode(string)
    return encoded.replace( '=', '' )

def urlsafe_b64decode(s):
    mod4 = len(s) % 4
    if mod4:
        s += ((4 - mod4) * '=')
    return base64.urlsafe_b64decode(str(s))
    

class ClickHandler(tornado.web.RequestHandler):
    def initialize(self, broker):
        self.broker = broker
        self.cookiehandler = CookieHanlder(broker)

    def prepare(self):
        self.set_header('P3P','CP="CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"')

    def getIp(self):
        try:
            ipaddr = self.request.remote_ip
            if ipaddr == 0:
                ipaddr = self.get_argument("ip", default=0)
            self.dic['ip'] = ipaddr
        except Exception:
            pass

    def dealCookie(self):
        try:
            # cookie identify
            if not self.ucookie:
                self.ucookie = self.cookiehandler.setCookie()
                self.set_cookie("uc", self.ucookie, domain=DOMAIN, expires_days=uc_expires)
            else:
                if not self.cookiehandler.checkCookie(self.ucookie):
                    dbg("UserCookie:%s is illegal!" % self.ucookie)
                    self.ucookie = self.cookiehandler.setCookie()
                    self.set_cookie("uc", self.ucookie, domain=DOMAIN, expires_days=uc_expires)
            self.dic['gmuid'] = self.ucookie          
        except Exception:
            pass  

    def returnGif(self):
        self.set_header('Content-Type', 'image/gif')
        self.write(IMG_DATA)

    @tornado.web.asynchronous
    #@gen.engine
    @gen.coroutine
    def get(self):
        try:
            dbg("-------------CORE HTTP HANDLER----------------")
            self.dic = defaultdict()
            self.dic['t'] = str( int(time.time()) )
            self.ucookie = self.get_cookie('uc')
            aurl = self.get_argument("url", default = None)
            self.getIp()
            self.dealCookie()
            self.redirect(aurl)
            #print aurl
        except Exception, e:
            return

