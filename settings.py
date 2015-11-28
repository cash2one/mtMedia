#!/usr/bin/python
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
SERVER_PORT = [9001,9002]

''' 流量分发器配置 '''
DISTRIBUTOR_SERVER = [("127.0.0.1",9000), ("127.0.0.1",9000)]

''' 超时设置 单位毫秒 '''
DISTRIBUTOR_TIME = 20

MULT_PROCESS_MODEL = False

''' Redis For adServer '''
REDISEVER = (("127.0.0.1",6379),)
REDISPORT = 6379



