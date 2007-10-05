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
		self.name = 'Autoaway Plugin'
		self.version = '0.022'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.kontakty = {} # jid:contact
		self.config['away_time'] = {'description':'Minutes to autoaway', 'default':'10', 'value': '','type':'text'}
		self.config['away_text'] = {'description':'Text to show while auto away', 'default':'User is away for %i minutes.', 'value': '','type':'text'}
		self.config['preserve_show'] = {'description':"Change only status message", 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.installTranslator()
##			self.window = self.loadWindow("%s/plugins/%s/news.ui.py"%(self.homeDir, self.fname))
##			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('onInactivity', self.on_idle, priority=4)
			self.registerHandler('onActivity', self.on_active, priority=4)		
		else:
			self.loadConfig(homedir)
		
		self.message_set = False
		self.idletime = 0
		self.old_show = 'away'
		self.old_status = ''
		
	
	def on_idle(self, cas):
		self.idletime += cas
		if self.idletime > (int(self.config['away_time']['value'])*60) and not self.message_set:
			contact = self.main.client.roster['users'][self.main.client.jid.userhost()]
			self.old_show = contact.resources[self.main.client.jid.resource].show
			self.old_status = contact.resources[self.main.client.jid.resource].status
			try:
				text = self.config['away_text']['value']%(self.idletime/60)
			except:
				text = self.config['away_text']['value']
			self.main.client.sendPresence(show = 'away', status = text)
			for muc in self.main.client.groupchats.itervalues():
					self.main.client.sendPresence(show = 'away', status = text, to = '%s/%s'%(muc.jid, muc.nick))
			self.message_set = True
			log.msg('idle status poslan')
	
	def on_active(self):
		if self.message_set:
			self.idletime = 0
			self.message_set = False
			self.main.client.sendPresence(show = self.old_show, status = self.old_status)
			for muc in self.main.client.groupchats.itervalues():
				self.main.client.sendPresence(show = self.old_show, status = self.old_status, to = '%s/%s'%(muc.jid, muc.nick))
