#!/usr/bin/env python

from urllib import urlencode
from collections import defaultdict
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('adrender','templates'))

MONITOR_HOST = "http://123.56.16.39"
#MONITOR_HOST = "http://click.mtty.com"
IMP_MONITOR_PATH = "/mt/show?"
CLICK_MONITOR_PATH = "/mt/click?"
IMP_MONITOR_ERROR = "/s_err.gif?"
CLICK_MONITOR_ERROR = "/c_err.gif?"

def generate_imp_url(req_dic, res_dic):
	try:
		para = defaultdict()
		para['eid'] = res_dic['eid'] if res_dic.has_key('eid') else ''
		para['aid'] = res_dic['aid'] if res_dic.has_key('aid') else ''
		para['pid'] = res_dic['pid'] if res_dic.has_key('pid') else ''
		para['cid'] = res_dic['cid'] if res_dic.has_key('cid') else ''
		para['area'] = res_dic['area'] if res_dic.has_key('area') else ''
		para['rid'] = res_dic['rid'] if res_dic.has_key('rid') else ''
		para['t'] = req_dic['t']
		para = urlencode(para)
		return MONITOR_HOST + IMP_MONITOR_PATH + para
	except Exception as e:
		print "generate_imp_url:%s" % e
		return MONITOR_HOST + IMP_MONITOR_ERROR + "info=" + e

def generate_click_url(req_dic, res_dic):
	try:
		para = defaultdict()
		para['eid'] = res_dic['eid'] if res_dic.has_key('eid') else ''
		para['aid'] = res_dic['aid'] if res_dic.has_key('aid') else ''
		para['pid'] = res_dic['pid'] if res_dic.has_key('pid') else ''
		para['cid'] = res_dic['cid'] if res_dic.has_key('cid') else ''
		para['area'] = res_dic['area'] if res_dic.has_key('area') else ''
		para['rid'] = res_dic['rid'] if res_dic.has_key('rid') else ''
		para['t'] = req_dic['t']
		para['url'] = res_dic['click_url'] if res_dic.has_key('click_url') else ''
		para = urlencode(para)
		return MONITOR_HOST + CLICK_MONITOR_PATH + para
	except Exception as e:
		print "generate_imp_url:%s" % e
		return IMP_MONITOR_HOST + CLICK_MONITOR_ERROR + "info=" + e

def creatAdRender(req_dic, res_dic):
	try:
		materail = defaultdict()
		template = env.get_template("html_0.html")
		materail['m_type'] = res_dic['m_type'] if res_dic.has_key('m_type') else 'img'
		materail['m_url'] = res_dic['m_url'] if res_dic.has_key('m_url') else ''
		#materail['click_url'] = res_dic['click_url'] if res_dic.has_key('click_url') else ''
		materail['click_url'] = generate_click_url(req_dic, res_dic)
		#materail['imp_url'] = res_dic['imp_url'] if res_dic.has_key('imp_url') else ''
		materail['imp_url'] = generate_imp_url(req_dic, res_dic)
		materail['cm_url'] = res_dic['cm_url'] if res_dic.has_key('cm_url') else ''
		materail['monitor_url'] = res_dic['monitor_url'] if res_dic.has_key('monitor_url') else ''
		materail['m_width'] = res_dic['m_width'] if res_dic.has_key('m_width') else ''
		materail['m_height'] = res_dic['m_height'] if res_dic.has_key('m_height') else ''
		html = template.render(materail = materail)
		return html
	except Exception as e:
		print "creatAdRenderError:%s" % e
		return defaultAdRender()


def defaultAdRender():
	try:
		template = env.get_template("html_0.html")
		materail = dict()
		materail['m_type'] = 'flash'
		materail['m_url'] = 'http://material.istreamsche.com/test/300x250.swf'
		materail['click_url'] = 'http://bd.kai-ying.com/dsp8/geo-tanx-yjns.html'
		materail['imp_url'] = 'http://lg.istreamsche.com/1x1.gif'
		materail['cm_url'] = 'http://lg.istreamsche.com/1x1.gif'
		materail['monitor_url'] = 'http://lg.istreamsche.com/1x1.gif'
		materail['m_width'] = '300'
		materail['m_height'] = '250'
		html = template.render(materail = materail)
		return html
	except Exception,e:
		print e
		pass


