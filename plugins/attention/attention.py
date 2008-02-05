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

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'attention'
		self.description = 'Attention, please!'
		self.author = "Josef 'PepeQ' Halicek"
		self.name = 'Attention'
		self.version = '0.007'
		self.category = ['fun']
		self.url = 'http://dev.jabbim.cz/jabbim'

		if main:
			self.loadConfig()
			self.registerHandler('on_attention', self.on_attention)
		else:
			self.loadConfig(homedir)


	def on_attention(self, frm, body, subject, xhtml, error):
		self.main.tray.showMessage(frm,self.tr("asks for attention!"), QtGui.QSystemTrayIcon.Information, 3000)



