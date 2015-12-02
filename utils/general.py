#!/usr/bin/env python

import socket
from random import Random


''' MSG TYPE '''
INTER_MSG_SHOW = 1
INTER_MSG_CLICK = 2

def SOCK():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #soc.bind((SERVIP,Port))
        return soc
    except socket.error, msg:
        print 'Failed to create socket:%s' % msg 


def random_str(randomlength = 16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
