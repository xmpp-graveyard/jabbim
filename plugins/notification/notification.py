try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys
sys.path.append('.')
from include import plugins
class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'notification'
		self.description = 'System tray notification'
		self.author = "Jan 'HanzZ' Kaluza"
		self.name = 'Notification Plugin'
		self.version = '0.035'
		self.category = ['notification']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.config['on_first_message'] = {'description':'Notify on first message from user', 'default':'True', 'value': '','type':'boolean'}
		self.config['on_muc_highlight'] = {'description':'Notify if groupchat message contains your nickname', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.registerHandler('on_message', self.on_message)
			self.registerHandler('on_GCmessage', self.on_GCmessage)
			self.loadConfig()
			self.installTranslator()
			self.main.tray.showMessage(self.tr("Notification"),self.tr("Notification plugin is activated"), QtGui.QSystemTrayIcon.Information, 2000)
		else:
			self.loadConfig(homedir)

	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Notification test",self.testSlot)

	def testSlot(self):
		self.main.tray.showMessage(self.tr("Notification "),self.tr("Notification plugin test :)"), QtGui.QSystemTrayIcon.Information, 2000)

	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay):
		if self.main.client.roster['users'].has_key(unicode(frm).rsplit("/")[0]):
			user=self.main.client.roster['users'][unicode(frm).rsplit("/")[0]].name
		else:
			user=frm
		if len(body)>40:
				traytext=body[:40]+" ..."
		else:
				traytext=body
		if self.config['on_first_message']['value']=="True":
			tab=None
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(frm):
					tab=w
					break
				if unicode(w.jid).rsplit("/")[0]==unicode(frm).rsplit("/")[0]:
					tab=w
				# we found tab
			if tab!=None:
				if tab.chat.first==None or tab.chat.first==True:
					self.main.tray.showMessage(self.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 5000)

	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		if delay != None:
			return
		if len(unicode(frm).rsplit("/"))==2:
			user=unicode(frm).rsplit("/")[1]
			frm=unicode(frm).rsplit("/")[0]
		else:
			user=frm
		#print self.config['on_muc_highlight']['value']
		if self.config['on_muc_highlight']['value']=="True":
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==frm:
					if user == w.name:
						continue
					#print "test"
					if unicode(body).lower().find(unicode(w.name).lower())!=-1:
						if len(body)>40:
								text=body[:40]+" ..."
						else:
								text=body
						traytext=unicode(user)+": "+text
						self.main.tray.showMessage(self.tr("New groupchat message for you"), traytext, QtGui.QSystemTrayIcon.Information, 5000)
