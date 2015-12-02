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
from collections import defaultdict
from utils.general import INTER_MSG_CLICK

import logging
logger = logging.getLogger(__name__)

IMG_FILE = open('./1x1.gif','r')
try:
    IMG_DATA = IMG_FILE.read()
finally:
    IMG_FILE.close()

REFERER = 'Referer'
USER_AGENT = 'User-Agent'
    

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

    def recordClick():
        self.broker.countercache.queueMsgPut( self.dic )
        self.ob_msg_server.sendMsgToStat(T_CLK, self.dic)

    def dealCookie(self):
        try:
            # cookie identify
            if not self.ucookie:
                self.ucookie = self.cookiehandler.setCookie()
                self.set_cookie("uc", self.ucookie, domain=DOMAIN, expires_days=uc_expires)
            else:
                if not self.cookiehandler.checkCookie(self.ucookie):
                    logger.error("UserCookie:%s is illegal!" % self.ucookie)
                    self.ucookie = self.cookiehandler.setCookie()
                    self.set_cookie("uc", self.ucookie, domain=DOMAIN, expires_days=uc_expires)
            self.dic['gmuid'] = self.ucookie          
        except Exception:
            pass  

    def returnGif(self):
        self.set_header('Content-Type', 'image/gif')
        self.write(IMG_DATA)

    def dealRedirect(self):
        if self.aurl:
            logger.info("Url:%s" % self.aurl)
            self.redirect(self.aurl)
        else:
            logger.info('No Url')
        

    @tornado.web.asynchronous
    #@gen.engine
    @gen.coroutine
    def get(self):
        try:
            logger.debug("-------------CORE CLICK HANDLER----------------")
            self.dic = defaultdict()
            self.dic['type'] = INTER_MSG_CLICK
            self.dic['t'] = str( int(time.time()) )
            self.ucookie = self.get_cookie('uc')
            self.aurl = self.get_argument("url", default = None)
            self.getIp()
            self.dealCookie()
            self.dealRedirect()
            #print aurl
            logger.debug("-----------------------------------------------")
        except Exception, e:
            self.dealRedirect()
            return

