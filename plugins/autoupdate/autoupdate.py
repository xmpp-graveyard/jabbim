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
		self.fname = 'autoupdate'
		self.description = 'Autoupdate'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Autoupdate'
		self.version = '0.02'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.plugindir = plugindir

		
		if main:
			self.loadConfig()
			self.registerHandler('on_authd',self.on_authd)
		else:
			self.loadConfig(homedir)

	def on_authd(self):
		self.main.client.callRemote('rpc@jabbim.cz/service', 'updateCore', (self.main.client.jid.host, sha1(self.main.client.jid.userhost()).hexdigest(), self.main.client.client_os, self.main.client.version)).addCallback(self._update)

	def _update(self, vysledek):
		print vysledek
		if vysledek[0][0] == False:
			#nemame posledni verzi
			self.main.tray.showMessage(frm,self.tr("New version of Jabbim is available!"), QtGui.QSystemTrayIcon.Information, 3000)
	
