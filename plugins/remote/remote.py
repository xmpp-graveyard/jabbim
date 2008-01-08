#-*- coding: UTF-8 -*-

import sys,os,time
sys.path.append('.')
from include import plugins
from twisted.python import log
from configobj import ConfigObj
from twisted.words.protocols.jabber import jid as jidT
from twisted.web import xmlrpc, server
from PyQt4 import QtCore, QtGui
from twisted.python import log
from time import time

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'remote'
		self.description = 'XMLRPC Remote Control'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'XMLRPC Remote'
		self.version = '0.01'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.developMode=True

		if main:
			self.pfilename = os.path.join(homedir,"xmlrpcports")
			self.loadConfig(homedir)
			self.loadConfig()
			r = Remote(main)
			from twisted.internet import reactor
			self.server = server.Site(r)
			port = 7080
			while True:
				try:
					self.conn = reactor.listenTCP(port, self.server, interface = 'localhost')
					break
				except:
					port += 1
			pfile = open(self.pfilename, "a")
			pfile.write("%s:%s\n" % (time(), port)) # timstamp (float): port (int)
			pfile.close()

		else:
			self.loadConfig(homedir)
	
	def on_remove(self):
		#remove factory and listening port here

		self.conn.stopListening()
		os.remove(self.pfilename)
			



class Remote(xmlrpc.XMLRPC):
	"""An example object to be published."""
	allowNone = True
	def __init__(self, main):
		self.main = main
		
	def xmlrpc_setStatus(self, show, status):
		self.main.sendPresence(None, show, status)
		return True
	
	def xmlrpc_startChat(self, jid, nick = None):
		print 'startChat from RPC'
		jid = self.main.getJid(jid)
		if  jid :
			if nick == None:
				nick = jid.user
			self.main.chat.addChatTab(jid.userhost(), nick, QtGui.QIcon(self.main.getIcon(status="offline",size="16x16")))
			return True
		else:
			return False
	
	def xmlrpc_joinMUC(self, jid):
		jid = self.main.getJid(jid)
		if jid:
			nickname = self.main.client.jid.user
			if self.main.chat.addGroupChatTab(jid.userhost(),nickname):
					self.main.client.joinGC(jid.userhost(), nickname)
					return True
			else:
				return False
		else:
			return False
					
