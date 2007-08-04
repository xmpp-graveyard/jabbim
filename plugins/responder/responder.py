import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui, uic
from urllib import quote, unquote
from twisted.python import log

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'responder'
		self.description = 'ICQ auto responder'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'ICQ Responder'
		self.version = '0.017'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.count = 0
# 		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		

		if main:
			self.registerHandler('on_message', self.on_message, priority = 4)
			self.config['message'] = {'description':'', 'default':"Toto je automaticka odpoved. Toto ICQ cislo je mimo provoz, jeho uzivatel nyni pouziva pouze Jabber. Muzes ho kontaktovat na jeho JabberID "+self.main.client.jid.userhost()+" . Pokud nevis jak na to, navstiv  http://www.jabbim.cz/services-start.html \n Preji pekny den.", 'value': '','type':'text'}
			self.loadConfig()

	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Show count",self.showSlot)
	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay):
		if frm.find('icq')!=-1:
			self.main.client.sendMessage(frm, self.config['message']['value'])
			self.count = self.count +1
			return False
			
	def showSlot(self):
		self.main.tray.showMessage('Responder','Messages sent: '+unicode(self.count), QtGui.QSystemTrayIcon.Information, 3000)
