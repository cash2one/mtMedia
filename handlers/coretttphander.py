#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
#
# Create by: Yuanji
# Date Time: 2015-04-22 15:36:00
#
###############################################################################
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
from utils.general import SOCK
from adrender import defaultAdRender

import functools

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
        self.broker = broker
        self.cookiehandler = CookieHanlder(broker)
        self.ob_dist = broker.dist

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

    def recordReq(self):
        self.broker.countercache.queueMsgPut( self.dic )
        pass

    def recordRes(self):
        pass

    def cusRedirect(self):
        self.set_header('Content-Type', 'image/gif')
        self.write(IMG_DATA)


    @gen.coroutine
    def getFetch(self):
        try:
            s = SOCK()
            s.settimeout(0.01)
            s.sendto("hehehhehehe",("127.0.0.1", 9000))
            resp = s.recvfrom(1024)
            raise gen.Return(resp[0])
            #s.close()
            #print resp
            #self.write(re_list.buffer.getvalue())
            #self.write(re_list.buffer.getvalue())
            #raise gen.Return(resp.buffer.getvalue())
            #print resp
            #raise gen.Return(resp)

        except gen.Return as e:
            print e
        except Exception, e:
            print "getFetch:%s" % e
            pass
        #http_client.close()
    
    @gen.coroutine
    def distribute(self):
        try:
            s = SOCK()
            s.settimeout(DISTRIBUTOR_TIME/1000)
            s.sendto("hehehhehehe",("127.0.0.1", 9000))
	    re = s.recvfrom(1024)
            self.write(re[0])
            self.finish()
	    s.close()
	    raise gen.Return(re[0])
        except gen.Return as e:
            print e
        except Exception,e:
            self.finish()
	    self.s.close()
            print e

    @tornado.web.asynchronous
    #@gen.engine
    @gen.coroutine
    def get(self):
        try:
            dbg("-------------CORE HTTP HANDLER----------------")
            self.dic = defaultdict()
            self.dic['t'] = str( int(time.time()) )
            self.ucookie = self.get_cookie('uc')
            self.dic['pid'] = self.get_argument("pid", default = None)
            self.dic['ad_w'] = self.get_argument("w", default = '0')
            self.dic['ad_h'] = self.get_argument("h", default = '0')
            self.getIp()
            self.dealCookie()
            self.recordReq()
            res = yield self.ob_dist.dist(self.dic)
            #print type(res)
            res = defaultAdRender()
            self.set_header("Content-Type", "text/html")
            if res:
	        self.write(res)
            else:
                # Default 
                pass
	    self.finish()
        except Exception, e:
            # Default
            print "CORE HTTP HANDLER Err: %s" % e

