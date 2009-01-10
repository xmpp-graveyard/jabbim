import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['message']={'type':'text-multi','label':self.main.tr("Auto reply"),'value':'Toto je automaticka odpoved. Toto ICQ cislo je mimo provoz, jeho uzivatel nyni pouziva pouze Jabber. Muzes ho kontaktovat na jeho JabberID [JID]. Pokud nevis jak na to, navstiv  http://www.jabbim.cz/services-start.html \n Preji pekny den.'}
		self.config['exclude']={'type':'jid-list','label':self.main.tr("Allow JIDs"),'value':[]}

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'responder'
		self.installTranslator()
		self.description = self.tr('CAREFUL!\n' +
			'Do not enable this plugin unless you intend to cut down a little on your ICQ usage.\n\n' +
			'ICQ auto responder is meant for the ICQ transport users who want to quit ICQ for good.\n' +
			'If you enable this plugin, contacts trying to write to you over ICQ will receive an automatic reply ' +
			'telling them how to reach you properly. You will NOT see their messages. ' +
			'The exact text of the automatic reply is customizable.')
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'ICQ Responder'
		self.version = '0.033'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.count = 0
		self.configDialog=config(self)
		if main:
			self.registerHandler('on_message', self.on_message, priority = 4)

			self.loadConfig()
		else:
			self.loadConfig(homedir)

	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction("Show count",self.showSlot)
	def on_message(self,msg):
		frm, typ, body, subject ,  xhtml,chatstate ,  delay, error = msg.legacyUnpack()
		jid = self.main.getJid(frm)
		if jid.host.startswith('icq') and not frm in self.config['exclude']:
			self.main.client.sendMessage(frm, self.config['message'].replace('[JID]', self.main.client.jid.userhost()))
			self.count = self.count +1
			return False
			
	def showSlot(self):
		self.main.tray.showMessage('Responder','Messages sent: '+unicode(self.count), QtGui.QSystemTrayIcon.Information, 3000)
