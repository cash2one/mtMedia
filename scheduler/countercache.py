#!/usr/bin/env python
# coding=utf-8

import time
import threading
from settings import *
from collections import defaultdict
from scheduler.database import Database
from utils.log import dbg, loginfo, logwarn, logerr
from tornado.queues import Queue
from tornado.ioloop import  IOLoop
import tornado.gen

CACHE_DUR_FREQ = 1


'''
Queue Info
{   
    'type':1  # 1 pv 2 click 3 cpa ...
    'pid':xxx,
}

Cache info
{

}

'''

class CounterCache(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.m_queue = Queue()
        self.m_CacheFlag = 1
        self.m_CounterCache = None
        self.m_Cache_A = defaultdict()
        self.m_Cache_B = defaultdict()

        self.database = Database()

        self.cacheInit(self.m_Cache_A)
        self.cacheInit(self.m_Cache_B)

    def switchCache(self):
        if self.m_CacheFlag == 1:
            return self.m_Cache_A
        elif self.m_CacheFlag == 2:
            return self.m_Cache_B

    def chageCacheFlag(self):
        if self.m_CacheFlag == 1:
            self.m_CacheFlag = 2
        elif self.m_CacheFlag == 2:
            self.m_CacheFlag = 1
    
    def clearCache(self):
        if self.m_CacheFlag == 1:
            self.m_Cache_B.clear()
            self.cacheInit(self.m_Cache_B)
        elif self.m_CacheFlag == 2:
            self.m_Cache_A.clear()
            self.cacheInit(self.m_Cache_A)

    def cacheInit(self, cache):
        cache['pid_info'] = defaultdict(int)

    @tornado.gen.coroutine
    def queueMsgPut(self, msg):
        yield self.m_queue.put(msg)

    @tornado.gen.coroutine
    def queueMsgGet(self):
        while True:
            msg = yield self.m_queue.get()
            #print msg
            cache = self.switchCache()
            # put
    
    def cacheDura(self):
        cache = None
        if self.m_CacheFlag == 1:
            cache = self.m_Cache_B
        if self.m_CacheFlag == 2:
            cache = self.m_Cache_A

        #loginfo(cache)

        if cache.has_key('pid_info'):
            pass

        if cache.has_key('aid_info'):
            for aid in cache['aid_info']['exchange_price'].iterkeys():
                self.database.incAdvBidSpend(aid, cache['aid_info']['exchange_price'][aid])
                self.database.decAdvBidSpend(aid, "-%.3f" %  (float(cache['aid_info']['exchange_price'][aid])/1000))

    def run(self):
        while True:
            try:
                time.sleep( CACHE_DUR_FREQ )
                self.chageCacheFlag()
                self.cacheDura()
                self.clearCache()

            except Exception, e:
                logerr(e)
                continue


