#-*- coding: UTF-8 -*-

import sys,os,time, re
sys.path.append('.')
from include import plugins
from twisted.python import log
from configobj import ConfigObj
from twisted.web import xmlrpc, server
from PyQt4 import QtCore, QtGui
from twisted.python import log
from time import time
from twisted.internet import threads
from twisted.words.xish.domish import escapeToXml
import time
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1
from imp import load_source
from include import utils
from twisted.internet import  threads,  reactor
from twisted.web.microdom import parseString

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'uniemoticons'
		self.description = 'Universal emoticons'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'UniEmoticons'
		self.version = '0.01'
		self.category = ['fun']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.current = {}	
		if main:
			self.loadConfig()
			self.registerHandler('on_message', self.on_message,  priority = 1)
			self.registerHandler('on_GCmessage', self.on_GCmessage,  priority = 1)
			threads.deferToThread(self.loadCurrentEmoticons)
		else:
			self.loadConfig(homedir)
		
	def loadCurrentEmoticons(self):
		for k in sorted(self.main.emoticonsWidget.smileys.iterkeys(), key=len, reverse=True):
			v = self.main.emoticonsWidget.smileys[k]
			fp = open(v, 'rb')
			self.current[k] = sha1(fp.read()).hexdigest()
			self.main.client.bobDef[self.current[k]] = v
			self.main.client.bobDef.write()
			fp.close()
		self.main.client.bobDef.write()
		self.loadAllEmoticons()

	def on_messageSend(self,msg):
		if  self.main.client.hasFeature(msg.to.full(), 'urn:xmpp:tmp:bob') or msg.typ == 'groupchat':
			if msg.xhtml != None:
				for k,  cid in self.current.iteritems():
					msg.xhtml = msg.xhtml.replace(k, '<img src="cid:%s" alt="%s" />'%(cid, k))
					print msg.xhtml
			elif msg.body != None:
				xhtm = msg.body
				for k,  cid in self.current.iteritems():
					xhtm = xhtm.replace(k, '<img src="cid:%s" alt="%s" />'%(cid, k))
					print xhtm
			
				if xhtm != msg.body:
					msg.xhtml = xhtm
		return msg
	
	def on_message(self,  msg,  typ = 'on_message'):
		changed = False
		if msg.xhtml != None:
			dom = parseString(unicode('<p>'+msg.xhtml+'</p>'))
			#seznam = {}
			
			for el in dom.getElementsByTagName('img'):
				src = el.getAttribute('src')
				if src != None and src.startswith('cid:'):
					print src
					cid = src.split(':')[1]
					link = self.main.client.bobCacheDir+cid
					el.setAttribute('src', link)
					changed = True
					self.main.client.getBOBData(msg.frm.full(),  cid)
			msg.setXHTML(unicode(dom.toxml()))
		if changed:
			reactor.callLater(0.5, self.main.client.dispatcher.publishEvent,typ,  msg)
			return False
	
	def on_GCmessage(self,  msg,  typ = 'on_GCmessage'):
		self.on_message(msg,  typ)
		
	def loadAllEmoticons(self):
		# emoticons from Jabbim root directory
		packs=os.listdir("emoticons/")
		for pack in packs:
			if os.path.isdir('emoticons/'+pack):
				emoticons=os.listdir('emoticons/'+pack+"/")
				for emoticon in emoticons:
					if emoticon.endswith('.cfg'):
						emo=pack+"/"+emoticon
						#config=ConfigObj("emoticons/"+emo,encoding='UTF8')
						loaded,config=self.main.loadJabbimExtraConfig("emoticons/"+emo,'emoticons/default/smileys.cfg')
						if loaded:
							for v in config['emoticons'].itervalues():
								v ="emoticons/"+pack+'/'+v
								if not v in self.main.client.bobDef.values():
									try:
										fp = open(v, 'rb')
										hash = sha1(fp.read()).hexdigest()
										fp.close()
										self.main.client.bobDef[hash] = v
									except:
										continue

		# emoticons from users home directory
		packs=os.listdir(self.main.realHomeDir+"/emoticons")
		for pack in packs:
			if os.path.isdir(self.main.realHomeDir+"/emoticons/"+pack):
				emoticons=os.listdir(self.main.realHomeDir+"/emoticons/"+pack+"/")
				for emoticon in emoticons:
					if emoticon.endswith('.cfg'):
						emo=pack+"/"+emoticon
						#config=ConfigObj(self.main.realHomeDir+"/emoticons/"+emo,encoding='UTF8')
						loaded,config=self.main.loadJabbimExtraConfig(self.main.realHomeDir+"/emoticons/"+emo,'emoticons/default/smileys.cfg')
						if loaded:
							for v in config['emoticons'].itervalues():
								v = self.main.realHomeDir+"/emoticons/"+pack+'/'+v
								if not v in self.main.client.bobDef.values():
									try:
										fp = open(v, 'rb')
										hash = sha1(fp.read()).hexdigest()
										fp.close()
										self.main.client.bobDef[hash] = v
									except:
										continue
			self.main.client.bobDef.write()
		
