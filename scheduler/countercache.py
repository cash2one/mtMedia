#!/usr/bin/env python
# coding=utf-8

import time
import threading
from settings import *
from collections import defaultdict
from scheduler.database import Database
from tornado.queues import Queue
from tornado.ioloop import  IOLoop
import tornado.gen

from utils.general import INTER_MSG_SHOW, INTER_MSG_CLICK, INTER_MSG_REQUEST

import logging
logger = logging.getLogger(__name__)

CACHE_DUR_FREQ = 5


class CounterCache(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.m_queue = Queue()
        self.m_CacheFlag = 1
        self.m_CounterCache = None
        self.m_Cache_A = defaultdict()
        self.m_Cache_B = defaultdict()

        self.database = Database(redis_conf = REDISEVER)

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
        cache['pid_info'] = { 'request':defaultdict(int), 'response':defaultdict(int),}
        cache['eid_info'] = { 'pv':defaultdict(int), }
        cache['click_info'] = { 'pid':defaultdict(int), 'eid':defaultdict(int) }

    @tornado.gen.coroutine
    def queueMsgPut(self, msg):
        yield self.m_queue.put(msg)

    @tornado.gen.coroutine
    def queueMsgGet(self):
        while True:
            msg = yield self.m_queue.get()
            #print msg
            logger.info('QueueGet:%r' % msg)
            self.cacheInfoPut(msg)

    def cacheInfoPut(self, msg):
        cache = self.switchCache()
        if msg.has_key('type') and msg['type'] == INTER_MSG_REQUEST:
            if msg.has_key('pid'):
                pid = msg['pid']
                pid_request = cache['pid_info']['request']
                pid_request[pid] = pid_request[pid] + 1

        if msg.has_key('type') and msg['type'] == INTER_MSG_SHOW:
            if msg.has_key('eid'):
                eid = msg['eid']
                imp_info_eid = cache['eid_info']['pv']
                imp_info_eid[eid] = imp_info_eid[eid] + 1

        if msg.has_key('type') and msg['type'] == INTER_MSG_CLICK:
            if msg.has_key('pid') and msg.has_key('eid'):
                pid = msg['pid']
                eid = msg['eid']
                click_info_pid = cache['click_info']['pid']
                click_info_eid = cache['click_info']['eid']
                click_info_pid[pid] = click_info_pid[pid] + 1
                click_info_eid[eid] = click_info_eid[eid] + 1
            else:
                logger.warn("cacheInfoPut lose pid or eid:%r" % msg)
            #print cache


    def cacheDura(self):
        cache = None
        if self.m_CacheFlag == 1:
            cache = self.m_Cache_B
        if self.m_CacheFlag == 2:
            cache = self.m_Cache_A

        if cache.has_key('pid_info'):
            pids = cache['pid_info']['request']
            for pid in pids.iterkeys():
                self.database.incPidRequest(pid, pids[pid])
                logger.debug("cacheDura Pid Request:%s %r" % (pid, pids[pid]))

        if cache.has_key('eid_info'):
            eids = cache['eid_info']['pv']
            for eid in eids.iterkeys():
                self.database.incEidShow(eid, eids[eid])
                logger.debug("cacheDura Eid Show:%s %r" % (eid, eids[eid]))

        if cache.has_key('click_info'):
            pids = cache['click_info']['pid']
            for pid in pids.iterkeys():
                self.database.incPidClick(pid, pids[pid])
                logger.debug("cacheDura Pid Click:%s %r" % (pid, pids[pid]))
            eids = cache['click_info']['eid']
            for eid in eids.iterkeys():
                self.database.incEidClick(eid, eids[eid])
                logger.debug("cacheDura Eid Click:%s %r" % (eid, eids[eid]))

        #if cache.has_key('aid_info'):
        #    for aid in cache['aid_info']['exchange_price'].iterkeys():
        #        self.database.incAdvBidSpend(aid, cache['aid_info']['exchange_price'][aid])
        #        self.database.decAdvBidSpend(aid, "-%.3f" %  (float(cache['aid_info']['exchange_price'][aid])/1000))

    def run(self):
        while True:
            try:
                time.sleep( CACHE_DUR_FREQ )
                self.chageCacheFlag()
                self.cacheDura()
                self.clearCache()

            except Exception, e:
                continue


