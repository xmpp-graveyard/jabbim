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
# 		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			#self.registerHandler('on_message_send', self.on_message_send, priority = 1)

			self.registerHandler("onCommand", self.commandCalled, priority=5)
			self.loadConfig()
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		pass
	def commandCalled(self, cmd, args, muc):
		log.msg("Command: %s %s %s" % (cmd, args, muc))
		if cmd != "amarok":
			return
		playing=unicode(commands.getoutput("dcop amarok player nowPlaying"))
		playing="/me hraje: (8) %s (8)" % playing
		log.msg(playing)
		#muc.ui.line.setPlainText("/me hraje: (8) %s (8)" % playing)
		self.main.client.sendMessage(muc.jid, playing, "groupchat")
	#def on_message_send(self, to, body, typ, subject,composing, xhtml,  muc):

		#if body[:7]=="/amarok":
			#playing=unicode(commands.getoutput("dcop amarok player nowPlaying") )
			#if playing=='':
				#playing='Ticho :)'
			#if playing=='call failed':
				#playing='Amarok nejede'
			#self.main.client.sendMessage(to, u"/me hraje: (8)  "+playing,'chat', self.main.client.jid.userhost())
			#return False

