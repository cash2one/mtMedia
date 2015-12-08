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
import tornado.log
import tornado.web
import tornado.ioloop
from settings import *
from tornado import gen
from handlers.cookiehandler import *
import random, time, os, sys, socket
from collections import defaultdict
from adrender import defaultAdRender, creatAdRender, creatAdJsonBack, defaultAdJsonBack
from utils.general import INTER_MSG_SHOW
from utils.general import random_str

import logging
logger = logging.getLogger(__name__)

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
    


class CoreHttpHandler(tornado.web.RequestHandler):
    def initialize(self, broker):
        self.res = None
        self.broker = broker
        self.cookiehandler = CookieHanlder(broker)
        self.ob_dist = broker.dist
        self.ob_requester = broker.requester
        self.ob_msg_server = broker.msg_server

    def prepare(self):
        self.set_header('Pragma', 'no-cache')
        self.set_header("Cache-Control", 'no-cache,no-store,must-revalidate')
        self.set_header('P3P','CP="CURa ADMa DEVa PSAo PSDo OUR BUS UNI PUR INT DEM STA PRE COM NAV OTC NOI DSP COR"')

    def getIp(self):
        try:
            ipaddr = self.request.remote_ip
            if ipaddr == 0:
                ipaddr = self.get_argument("ip", default=0)
            self.dic['ip'] = ipaddr
            logger.debug('ip:%s' % self.dic['ip'])
        except Exception:
            pass

    def dealCookie(self):
        try:
            # cookie identify
            if not self.ucookie:
                self.ucookie = self.cookiehandler.setCookie()
                self.set_cookie("m", self.ucookie, domain=DOMAIN, expires_days=uc_expires)
            else:
                if not self.cookiehandler.checkCookie(self.ucookie):
                    logger.error("UserCookie:%s is illegal!" % self.ucookie)
                    self.ucookie = self.cookiehandler.setCookie()
                    self.set_cookie("m", self.ucookie, domain=DOMAIN, expires_days=uc_expires)
            self.dic['gmuid'] = self.ucookie          
            logger.debug('cookie:%s' % self.dic['gmuid'])
        except Exception:
            pass  

    def recordReq(self):
        self.broker.countercache.queueMsgPut( self.dic )
        self.ob_msg_server.sendMsgToStat(T_IMP, self.dic)
        pass

    def recordRes(self):
        pass

    def returnGif(self):
        self.set_header('Content-Type', 'image/gif')
        self.write(IMG_DATA)

    def customResult(self):
        self.set_header("Content-Type", "text/html")
        if self.res is None:
            back = defaultAdJsonBack()
        else:
            self.dic['impid'] = self.res['impid'] = random_str()
            #back = creatAdRender(self.dic, self.res)
            back = creatAdJsonBack(self.dic, self.res)
        self.write(back)
        self.finish()

    @tornado.web.asynchronous
    #@gen.engine
    @gen.coroutine
    def get(self):
        try:
            logger.debug("-------------CORE HTTP HANDLER----------------")
            self.dic = defaultdict()
            self.dic['type'] = INTER_MSG_SHOW
            self.dic['t'] = str( int(time.time()) )
            self.dic['rid'] = str(uuid.uuid1())
            self.ucookie = self.get_cookie('m')
            self.dic['callback_id'] = self.get_argument("callback", default = None)
            self.dic['pid'] = self.get_argument("pid", default = 'mm_10001328_4164206_13516084')
            
            self.dic['ad_w'] = self.get_argument("w", default = '300')
            self.dic['ad_h'] = self.get_argument("h", default = '250')
            self.getIp()
            self.dealCookie()
            #self.res = yield self.ob_dist.dist(self.dic)
            self.res = yield self.ob_requester.getAdReturn(self.dic)
            self.customResult()
            self.recordReq()
            logger.info("---------------------------------------------")
            return
        except Exception, e:
            logger.error(e)
            self.customResult()
            return

