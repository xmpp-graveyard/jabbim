# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils


class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'autoaway'
		self.description = 'Auto away'
		self.author = u"Jiří 'Sef' Gabryš"
		self.name = 'News Plugin'
		self.version = '0.001'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.kontakty = {} # jid:contact
		self.config['away_time'] = {'description':'Minutes to autoaway', 'default':10, 'value': '','type':'int'}
		self.config['away_text'] = {'description':'Text to show while auto away', 'default':'User is away for %i minutes.', 'value': '','type':'text'}
		self.config['preserve_show'] = {'description':"Change only status message", 'default':True, 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.installTranslator()
			self.window = self.loadWindow("%s/plugins/%s/news.ui.py"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('onInactivity', self.on_idle, priority=4)
			self.registerHandler('onActivity', self.on_active, priority=4)		
		else:
			self.loadConfig(homedir)
		
		self.message_set = False
		self.idletime = 0
#		self.old 
		
	
	def on_idle(self, cas):
		self.idletime += cas
		if self.idletime > (self.config['away_time']*60) and not self.message_set:
			pass	
