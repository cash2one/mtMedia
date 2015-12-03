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
AD_CORE_SERVER = "http://127.0.0.1:8899/tbid"


''' 流量分发器配置 '''
DISTRIBUTOR_SERVER = [("127.0.0.1",9000), ("127.0.0.1",9000)]

''' 超时设置 单位毫秒 '''
DISTRIBUTOR_TIME = 500

MULT_PROCESS_MODEL = False

''' Redis For adServer '''
REDISEVER = (("192.168.1.1",6379),)

''' MSG SERVER '''
MSG_SERVER = ('192.168.1.4',69092)
PART_NUM = 1
SENDMSG = True

''' Topic '''
T_IMP = "test"
T_CLK = "test"
T_ACT = "test"



