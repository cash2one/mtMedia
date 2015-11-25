#!/usr/bin/python

import json
import socket
from tornado import gen
from settings import DISTRIBUTOR_SERVER
from settings import DISTRIBUTOR_TIME
from utils.general import SOCK

class Distributor():
    def __init__(self):
        self.m_server_list = DISTRIBUTOR_SERVER
        self.m_len = len(self.m_server_list)
        self.counter = 0
        if self.m_len == 0:
            print "No DISTRIBUTOR_SERVER In Settings!"

    def _get(self):
        if self.m_len == 0:
            return None
        if self.counter < self.m_len:
            pass
        else:
            self.counter = 0
        return self.m_server_list[self.counter]

    @gen.coroutine
    def dist(self, dic):
        #try:
        if 1:
            dis_server = self._get()
            if dis_server is None:
                return
            else:
                try:
                    s = SOCK()
                    s.settimeout(float(DISTRIBUTOR_TIME)/1000)
                    s.sendto( json.dumps(dic), dis_server)
                    self.counter = self.counter + 1
	            re = s.recvfrom(1024)
	            raise gen.Return()
                except gen.Return as res_info:
	            s.close()
                    return re[0]# info
                except socket.timeout:
	            s.close()
                    print 'timeout'
                    return None
                    # record
                except Exception, e:
	            s.close()
                    print e
                    return None
        #except Exception, e:
        #    print "Dist Err:%s" % e          
