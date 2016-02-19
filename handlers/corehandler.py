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
from adrender import creatSspAdBack, defaultAdJsonBack
from utils.general import *

import logging
logger = logging.getLogger(__name__)

IMG_FILE = open('./1x1.gif','r')
try:
    IMG_DATA = IMG_FILE.read()
finally:
    IMG_FILE.close()

REFERER = 'Referer'
USER_AGENT = 'User-Agent'

PID_CONFIG = {
"mm_10001328_4164206_13516084":{'w':'300', 'h':'250', 'flowtype':'0'},
"144106":{'w':'300', 'h':'250', 'flowtype':'0'},
"144105":{'w':'580','h':'120', 'flowtype':'2'},
"119196":{'w':'300','h':'250', 'flowtype':'0'},
"144107":{'w':'300','h':'50', 'flowtype':'0'},
"144108":{'w':'610','h':'100', 'flowtype':'0'},
"144109":{'w':'300','h':'100', 'flowtype':'0'},
"144110":{'w':'300','h':'250', 'flowtype':'0'},
"144111":{'w':'640','h':'90', 'flowtype':'0'},
"144112":{'w':'840','h':'100', 'flowtype':'0'},
"144113":{'w':'300','h':'50', 'flowtype':'0'},
"144116":{'w':'300','h':'250', 'flowtype':'0'},
"144119":{'w':'300','h':'50', 'flowtype':'0'},
"144120":{'w':'300','h':'250', 'flowtype':'0'}
}

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
            self.dic[PARA_KEY_USER] = self.ucookie          
            logger.debug('cookie:%s' % self.dic[PARA_KEY_USER])
        except Exception:
            pass  

    def recordReq(self):
        self.broker.countercache.queueMsgPut( self.dic )
        self.ob_msg_server.sendMsgToStat(T_REQ, self.dic)
        pass

    def recordRes(self):
        self.broker.countercache.queueMsgPut( self.res )
        self.ob_msg_server.sendMsgToStat(T_IMP, self.res)
        pass

    def checkJsonback(self):
        try:
            if self.dic.has_key('callback_id'):
                j = self.dic['callback_id']
                j_list = j.split('_')
                if len(j_list) == 3:
                    if is_num_by_except(j_list[2]):
                        return True
                logger.warn('Error JsonBackID:%r' % j)
            return False
        except Exception,e:
            logger.error(e)
            return False

    def getPidDetail(self):
        try:
            if self.dic.has_key(PARA_KEY_PID):
                pid = self.dic[PARA_KEY_PID]
                if PID_CONFIG.has_key(pid):
                    detail = PID_CONFIG[pid]
                    self.dic[PARA_KEY_WIDTH] = detail['w']
                    self.dic[PARA_KEY_HEIGHT] = detail['h']
                    self.dic['flowtype'] = detail['flowtype']
                    if self.dic['flowtype'] == F_TYPE_MOBILE:
                        self.dic[PARA_KEY_ISMOBILE] = True
                        self.dic[PARA_KEY_ADX] = '99'
                    else:
                        self.dic[PARA_KEY_ISMOBILE] = False
                        self.dic[PARA_KEY_ADX] = '98'
                    return True
            logger.warn('No Pid In List!')
            return False
        except Exception,e:
            logger.error(e)
            return False

    def returnGif(self):
        self.set_header('Content-Type', 'image/gif')
        self.write(IMG_DATA)

    def customResult(self):
        self.set_header("Content-Type", "text/html")
        if self.res is None:
            back = defaultAdJsonBack()
        else:
            back = creatSspAdBack(self.dic, self.res)
        self.write(back)
        self.finish()

    @tornado.web.asynchronous
    #@gen.engine
    @gen.coroutine
    def get(self):
        try:
            logger.debug("-------------CORE HTTP HANDLER----------------")
            self.dic = defaultdict()
            self.dic['type'] = INTER_MSG_REQUEST
            self.dic['t'] = str( int(time.time()) )
            #self.dic[PARA_KEY_RID] = str(uuid.uuid1())
            self.ucookie = self.get_cookie('m')
            self.dic['callback_id'] = self.get_argument("callback", default = '')
            self.dic[PARA_KEY_PID] = self.get_argument("pid", default = 'mm_10001328_4164206_13516084')
            if self.checkJsonback() and self.getPidDetail():
                self.getIp()
                self.dealCookie()
                #self.res = yield self.ob_dist.dist(self.dic)
                self.res = yield self.ob_requester.getAdReturn(self.dic)
                #self.dic[PARA_KEY_RID] = self.res[PARA_KEY_RID] = random_str()
                if self.res:
                    self.dic[PARA_KEY_RID] = self.res[PARA_KEY_RID] = str(uuid.uuid1())
                    self.res['type'] = INTER_MSG_SHOW
                    self.res[PARA_KEY_USER] = self.dic[PARA_KEY_USER]
                    self.res[PARA_KEY_ADX] = self.dic[PARA_KEY_ADX]
                    self.recordRes()

                self.recordReq()

            self.customResult()
            logger.info("---------------------------------------------")
            return
        except Exception, e:
            logger.error(e)
            self.customResult()
            return

