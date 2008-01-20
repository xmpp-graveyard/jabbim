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
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'remote'
		self.description = 'XMLRPC Remote Control'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'XMLRPC Remote'
		self.version = '0.01'
		self.category = ['utils']
		self.url = 'http://dev.jabbim.cz/jabbim'

		if main:
			self.pfilename = os.path.join(homedir,"xmlrpcports")
			self.loadConfig(homedir)
			self.loadConfig()
			self.cookie = generateCookie()
			r = Remote(main, self)
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
			pfile.write("%s:%s:%s\n" % (time(), port, self.cookie)) # timstamp (float): port (int) : cookie (str)
			pfile.close()

		else:
			self.loadConfig(homedir)
	
	def on_remove(self):
		#remove factory and listening port here

		self.conn.stopListening()
		os.remove(self.pfilename)
			
def generateCookie():
	magic = unicode(globals())+unicode(time())
	return sha1(magic).hexdigest()

def checkCookie(incoming, mine):
	if incoming != mine:
		print 'bad cookie'
		return False
	else:
		return True


class Remote(xmlrpc.XMLRPC):
	"""An example object to be published."""
	allowNone = True
	def __init__(self, main, plugin):
		self.main = main
		self.cookie = plugin.cookie
		
	def xmlrpc_setStatus(self, show, status):
		self.main.sendPresence(None, show, status)
		return True
	
	def xmlrpc_startChat(self, jid, cookie, nick = None):
		print 'startChat from RPC'
		if not checkCookie(cookie, self.cookie):
			return False
		jid = self.main.getJid(jid)
		if  jid :
			if nick == None:
				nick = jid.user
			self.main.chat.addChatTab(jid.userhost(), nick, QtGui.QIcon(self.main.getIcon(status="offline",size="16x16")))
			return True
		else:
			return False
	
	def xmlrpc_joinMUC(self, jid, cookie):
		if not checkCookie(cookie, self.cookie):
			return False
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
				
	def xmlrpc_addContact(self, jid):
		jid = self.main.getJid(jid)
		if jid:
			self.main.addContactMainWindow(jid)
			return True
		else:
			return False
