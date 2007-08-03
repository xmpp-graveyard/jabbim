import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui, uic
from urllib import quote, unquote
from twisted.python import log

#exp = re.compile(" (((https?://)|(ftp://)|(www\.))[^\ ]+)|(([^\ ]*\.){2,}[0-9a-z-A-Z]{2,4}(/[^\ ]*)?)")
#exp.search('http://jabbim.cz/').group()

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'news'
		self.description = 'Headlines window'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'News Plugin'
		self.version = '0.016'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.kontakty = {} # jid:contact
		self.config['notify_tray'] = {'description':'Notify in tray', 'default':'True', 'value': '','type':'boolean'}
		self.config['notify_show'] = {'description':'Show window on new', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.window = uic.loadUi("%s/plugins/%s/news.ui"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)
			QtCore.QObject.connect(self.window.roster, QtCore.SIGNAL('itemClicked ( QListWidgetItem* )'), self.contactChanged)
			QtCore.QObject.connect(self.window.zpravy, QtCore.SIGNAL('itemClicked (QListWidgetItem* )'), self.headlineChanged)
# 			QtCore.QObject.connect(self.window.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
# 			QtCore.QObject.connect(self.window.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
			
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Show news",self.showSlot)
	
	def showSlot(self):
		self.window.show()
	
	def on_message(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		if typ != 'headline':
			return True
		frm = frm.split('/')[0]
		font = QtGui.QFont()
		font.setBold(True)
		
		if self.kontakty.has_key(frm):
			self.kontakty[frm].addHeadline(subject, body)
		else:
			item = QtGui.QListWidgetItem(frm, self.window.roster)
			self.window.roster.addItem(item)
			self.kontakty[frm] = Contact(frm, item, self)
			self.kontakty[frm].addHeadline(subject, body)
		self.kontakty[frm].item.setFont(font)
		if self.config['notify_tray']['value']=='True':
			self.main.tray.showMessage("News",subject, QtGui.QSystemTrayIcon.Information, 3000)
		if self.config['notify_show']['value']=='True':
			self.window.show()
		itm = None
		itm = self.window.roster.currentItem()
		if itm!= None:
			if unicode(itm.text())==frm:
				self.updateZpravy(frm)
			
		return False
	
	def contactChanged(self, item):
		log.msg('contactChanged')
		jid = unicode(item.text())
		self.updateZpravy(jid)
	def updateZpravy(self, jid):
		try:
			kontakt = self.kontakty[jid]
		except:
			log.err(jid)
			return
		self.window.zpravy.clear()
		for zprava in kontakt.zpravy:
			item = QtGui.QListWidgetItem(zprava.subject, self.window.zpravy)
			font = QtGui.QFont()
			if zprava.unread:
				font.setBold(True)
			item.setFont(font)
			self.window.zpravy.addItem(item)
	
	def headlineChanged(self, item):
		font = font = QtGui.QFont()
		font.setBold(False)
		item.setFont(font)
		jid = unicode(self.window.roster.currentItem().text())
		try:
			kontakt = self.kontakty[jid]
		except:
			return
		radek = self.window.zpravy.currentRow()
		zprava = kontakt.zpravy[radek]
		zprava.unread = False
		self.window.subject.setText(zprava.subject)
		self.window.datum.setText(unicode(time.strftime('%X %x',time.localtime(zprava.time))))
		self.window.zprava.setText(zprava.body)
		if kontakt.neprectene() == 0:
			kontakt.item.setFont(font)
		
	

class Contact:
	def __init__(self, jid, item, plugin):
		self.jid = jid
		self.item = item
		self.plugin = plugin
		self.zpravy = []
	
	def addHeadline(self, subject, body):
		self.zpravy.append(Zprava(subject, body))
	
	def neprectene(self):
		n = 0
		for zprava in self.zpravy:
			if zprava.unread:
				n = n+1
		return n
		
class Zprava:
	def __init__(self, subject, body):
		self.subject = subject
		self.body = body
		self.time = time.time()
		self.unread = True 
