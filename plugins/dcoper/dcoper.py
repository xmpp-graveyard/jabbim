#-*-coding:utf-8-*-
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
		self.author = "Josef 'Pepeq' Halicek & Jachym 'kamahl' Barvinek"
		self.name = 'dcoper'
		self.version = '0.001'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.count = 0
		self.developMode=True
		if main:

			self.registerHandler("onCommand", self.commandCalled, priority=5)
			self.loadConfig()
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		pass
	def commandCalled(self, cmd, args, chat, typ):
		if cmd != "amarok":
			return
		playing=unicode(commands.getoutput("dcop amarok player nowPlaying"), "utf-8")
		if playing != "":
			playing="/me hraje: (8) %s (8)" % playing
		else:
			playing=unicode("AmaroK právě nic nepřehrává.", "utf-8")
		self.main.client.sendMessage(unicode(chat.jid), playing, typ)

