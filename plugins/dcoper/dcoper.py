import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
import commands

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'DCOPer'
		self.description = 'DCOP plugin for /amarok'
		self.author = "Josef 'Pepeq' Halicek"
		self.name = 'dcoper'
		self.version = '0.001'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.count = 0
		self.developMode=True
# 		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.registerHandler('on_message_send', self.on_message_send, priority = 1)

			self.loadConfig()
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		pass
	def on_message_send(self, to, body, typ, subject,composing, xhtml,  muc):
		if body[:7]=="/amarok":
			playing=commands.getoutput("dcop amarok player nowPlaying") 
			if playing=='':
				playing='Ticho :)'
			if playing=='call failed':
				plying='Amarok nejede'
			self.main.client.sendMessage(to, u"/me hraje: (8)  "+playing,'chat', self.main.client.jid.userhost())
			return False

