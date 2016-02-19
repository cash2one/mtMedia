#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Create by:  Yuanji
    Date: 2013-08-06
    For iSHOW Server
'''

"""Global configuration
"""
 
# LOG_LEVEL: DEBUG < INFO < WARN < ERROR

LOG_LEVEL = 'INFO'

'''设备ID'''
DEVICE_ID = '01'

'''服务端口配置'''
SERVER_PORT = [10001,10008]

''' Ad Core 配置'''
AD_CORE_SERVER = "http://192.168.2.15:20007/"


''' 流量分发器配置 '''
DISTRIBUTOR_SERVER = [("127.0.0.1",9000), ("127.0.0.1",9000)]

''' 超时设置 单位毫秒 '''
DISTRIBUTOR_TIME = 50

MULT_PROCESS_MODEL = False

''' Redis For adServer '''
REDISEVER = (("08dce178449f48fb.m.cnbja.kvstore.aliyuncs.com",6379),)
STATUS_REDIS_PASS = "08dce178449f48fb:MtqweBNM789"

''' MSG SERVER '''
MSG_SERVER = ('192.168.2.51',9092)
PART_NUM = 1
SENDMSG = True

''' Topic '''
T_REQ = "test"
T_IMP = "mt-show-v1"
T_CLK = "test"
T_ACT = "test"



