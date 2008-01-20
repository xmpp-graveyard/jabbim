#-*-coding:utf-8-*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
import commands

class config:
	def __init__(self, main):
		self.main = main
		self.config={}
		self.config["format"] = {
				"type": "text-multi",
				"label": self.main.tr("Format of message. %artist is replaced by artist's name, %title by track name and so on for %album, %genre, %year, %type and %totalTime"),
				"value": "/me hraje: (8) %artist - %title (%album) (8)"
				}
		self.config["amarok_off"] = {
				"type": "text-single",
				"label": self.main.tr("Message when amaroK is not running."),
				"value": "/me má vypnutý amarok :'("
				}
		self.config["amarok_paused"] = {
				"type": "text-single",
				"label": self.main.tr("Message when nothing is being played in amaroK."),
				"value": "/me zrovna nic nepřehrává :'("
				}

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'DCOPer'
		self.description = 'DCOP plugin for /amarok'
		self.author = "Josef 'Pepeq' Halicek & Jachym 'kamahl' Barvinek"
		self.name = 'dcoper'
		self.version = '0.1'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.count = 0
		self.developMode=True

		self.installTranslator()	

		self.configDialog=config(self)

		if main:
			#jid = quote(unicode(self.main.client.jid.userhost()))
			#if not os.path.isdir(self.main.homeDir+'/dcoper'):
				#os.mkdir(self.main.homeDir+'/dcoper')
			#if not os.path.isdir(self.main.homeDir+'/dcoper/'+ jid):
				#os.mkdir(self.main.homeDir+'/dcoper/'+ jid)
			self.registerHandler("onCommand", self.commandCalled, priority=5)
			self.loadConfig()
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		pass
	def commandCalled(self, cmd, args, chat, typ):
		if cmd != "amarok":
			return
		title = unicode(commands.getoutput("dcop amarok player title"))
		if title == u"call failed":
			msg = unicode(self.config["amarok_off"], "utf-8")
		if title == u"":
			msg = unicode(self.config["amarok_paused"], "utf-8")
		else:
			msg = unicode(self.config["format"], "utf-8")
			msg = msg.replace("%title", title)
			msg = msg.replace("%artist", commands.getoutput("dcop amarok player artist"))
			msg = msg.replace("%album", commands.getoutput("dcop amarok player album"))
			msg = msg.replace("%genre", commands.getoutput("dcop amarok player genre"))
			msg = msg.replace("%year", commands.getoutput("dcop amarok player year"))
			msg = msg.replace("%type", commands.getoutput("dcop amarok player type"))
			msg = msg.replace("%totalTime", commands.getoutput("dcop amarok player totalTime"))
		#playing=unicode(commands.getoutput("dcop amarok player nowPlaying"), "utf-8")
		log.msg("Playing: "+`msg`)
		self.main.client.sendMessage(unicode(chat.jid), msg, typ)

