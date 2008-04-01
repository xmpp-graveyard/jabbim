#-*- coding: UTF-8 -*-

import sys,os,time, re
sys.path.append('.')
from include import plugins
from twisted.python import log
from configobj import ConfigObj
from twisted.words.protocols.jabber import jid as jidT
from twisted.web import xmlrpc, server
from PyQt4 import QtCore, QtGui
from twisted.python import log
from time import time
from twisted.internet import threads
from twisted.words.xish.domish import escapeToXml
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1
from imp import load_source
from include import utils

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['formater']={'type':'list-single','label':self.main.tr("Formatter"), 'items':{'Textile':'textile', 'MarkDown':'markdown'}, 'value':'textile'}

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'format'
		self.description = 'Formatters support'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Format'
		self.version = '0.02'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.plugindir = plugindir
		self.configDialog=config(self)
		
		if main:
			self.loadConfig()
			f=open(utils.path(plugindir+'/%s.py'%self.config['formater'])) 
			textile = load_source(self.fname, plugindir+'/%s.py'%self.config['formater'], f)
			f.close()
			if self.config['formater'] == 'textile':
				self.formater = textile.textile
				self.args = {'encoding':'utf-8', 'output':'utf-8'}
			elif self.config['formater'] == 'markdown':
				self.formater = markdown
				self.args = {}
		else:
			self.loadConfig(homedir)
	
	def on_configChanged(self):
		plugindir = self.plugindir
		f=open(utils.path(plugindir+'/%s.py'%self.config['formater'])) 
		textile = load_source(self.fname, plugindir+'/%s.py'%self.config['formater'], f)
		f.close()
		if self.config['formater'] == 'textile':
			self.formater = textile.textile
			self.args = {'encoding':'utf-8', 'output':'utf-8'}
		elif self.config['formater'] == 'markdown':
			self.formater = markdown
			self.args = {}
	
	def on_groupchatMessageSend(self,jid,text="",xhtml="",composite=""):
		print text, xhtml, self.formater
		if xhtml == None or xhtml.strip() == "" or xhtml.replace('<br />','\n') == text:
			xhtml =xhtml.replace('<br />','\n')
			text = escapeToXml(text)
			print text
			xhtml = self.formater(text.encode('utf-8'), **self.args)
			print xhtml
			if text == xhtml.replace('<p>','').replace('</p>',''):
				return True

			self.main.client.sendMessage(jid, strip_html(xhtml), 'groupchat', composing = composite, xhtml = xhtml,  muc = True)
			return False
		return True

	def on_messageSend(self,jid,text="",xhtml="",composite=""):
		if xhtml == None or xhtml.strip() == "" or xhtml.replace('<br />','\n') == text:
			xhtml =xhtml.replace('<br />','\n')
			text = escapeToXml(text)
			xhtml = self.formater(text.encode('utf-8'), **self.args)
			print xhtml
			if text == xhtml.replace('<p>','').replace('</p>',''):
				return True

			self.main.client.sendMessage(jid, strip_html(xhtml).strip(), 'chat', composing = composite, xhtml = xhtml,  muc = False)
			tab,tabIndex=self.main.chat.findTab(unicode(jid)) 
			if tab: 
				tab.chat.appendXhtml(xhtml)
			return False
		return True

def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)

