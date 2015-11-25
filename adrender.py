#!/usr/bin/python

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('adrender','templates'))


def creatAdRender():
    pass


def defaultAdRender():
    try:
        template = env.get_template("html_0.html")
	materail = dict()
	materail['type'] = 'flash'
	materail['murl'] = 'http://material.istreamsche.com/test/300x250.swf'
	materail['click_url'] = 'http://bd.kai-ying.com/dsp8/geo-tanx-yjns.html'
	materail['imp_url'] = 'http://lg.istreamsche.com/1x1.gif'
	materail['cm_url'] = 'http://lg.istreamsche.com/1x1.gif'
	materail['th_url'] = 'http://lg.istreamsche.com/1x1.gif'
	materail['width'] = '300'
	materail['height'] = '250'
        html = template.render(materail = materail)
        return html
    except Exception,e:
        print e
        pass


