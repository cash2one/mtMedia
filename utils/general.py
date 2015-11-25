#!/usr/bin/python

import socket

def SOCK():
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #soc.bind((SERVIP,Port))
        return soc
    except socket.error, msg:
        print 'Failed to create socket:%s' % msg 
