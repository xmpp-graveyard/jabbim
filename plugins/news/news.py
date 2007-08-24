# -*- coding: utf8 -*-
import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils
#exp = re.compile(" (((https?://)|(ftp://)|(www\.))[^\ ]+)|(([^\ ]*\.){2,}[0-9a-z-A-Z]{2,4}(/[^\ ]*)?)")
#exp.search('http://jabbim.cz/').group()

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'news'
		self.description = 'Headlines window'
		self.author = u"Jiří 'Sef' Gabryš"
		self.name = 'News Plugin'
		self.version = '0.047'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.kontakty = {} # jid:contact
		self.config['notify_tray'] = {'description':'Notify in tray', 'default':'True', 'value': '','type':'boolean'}
		self.config['notify_show'] = {'description':'Show window on new', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.installTranslator()
			self.window = self.loadWindow("%s/plugins/%s/news.ui.py"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)
			QtCore.QObject.connect(self.window.ui.roster, QtCore.SIGNAL('itemClicked ( QListWidgetItem* )'), self.contactChanged)
# 			QtCore.QObject.connect(self.window.ui.roster, QtCore.SIGNAL('itemSelectionChanged ( )'), self.contactChanged)
			QtCore.QObject.connect(self.window.ui.zpravy, QtCore.SIGNAL('itemClicked (QListWidgetItem* )'), self.headlineChanged)
# 			QtCore.QObject.connect(self.window.ui.zpravy, QtCore.SIGNAL('itemSelectionChanged ( )'), self.headlineChanged)
# 			QtCore.QObject.connect(self.window.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
# 			QtCore.QObject.connect(self.window.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
		else:
			self.loadConfig(homedir)
			
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
		body = utils.replace_url(body)
		index = 0
		if self.kontakty.has_key(frm):
			index = self.kontakty[frm].addHeadline(subject, body)
		else:
			item = QtGui.QListWidgetItem(frm, self.window.ui.roster)
			self.window.ui.roster.addItem(item)
			self.kontakty[frm] = Contact(frm, item, self)
			index = self.kontakty[frm].addHeadline(subject, body)
		self.kontakty[frm].item.setFont(font)
		if self.config['notify_tray']['value']=='True':
			self.main.tray.showMessage("News",subject, QtGui.QSystemTrayIcon.Information, 3000)
 			self.main.events.addInfoEvent(header=self.tr("News: ")+subject,text=self.tr("From: ")+frm,typ='newHeadline',icon="images/32x32/status/rss-online.png", action = self.eventActivated, actionDict = [frm, index], trueCall = self.eventActivated, trueDict = [frm, index])
		if self.config['notify_show']['value']=='True':
			self.window.show()
# 		itm = None
# 		itm = self.window.ui.roster.currentItem()
# 		if itm!= None:
# 			if unicode(itm.text())==frm:
# 				self.updateZpravy(frm)
			
		return False
	
	def eventActivated(self, frm, index):
		print frm, index
		item = self.kontakty[frm].item
		self.window.ui.roster.setCurrentItem(item)
		self.updateZpravy(frm, False)
		self.window.ui.zpravy.setCurrentRow(index)					
		zprava = self.kontakty[frm].zpravy[index]
		kontakt = self.kontakty[frm]
		zprava.unread = False
		self.window.ui.subject.setText(zprava.subject)
		self.window.ui.datum.setText(unicode(time.strftime('%X %x',time.localtime(zprava.time))))
		self.window.ui.zprava.setHtml(zprava.body)
		if kontakt.neprectene() == 0:
			font =  QtGui.QFont()
			font.setBold(False)
			kontakt.item.setFont(font)
		self.window.show()
	
	def contactChanged(self, item):
#		item = self.window.ui.roster.currentItem()
		log.msg('contactChanged')
		jid = unicode(item.text())
		self.updateZpravy(jid)
	
	def updateZpravy(self, jid, setUnread = True):
		try:
			kontakt = self.kontakty[jid]
		except:
			log.err(jid)
			return
		self.window.ui.zpravy.clear()
		
		for zprava in kontakt.zpravy:
			item = QtGui.QListWidgetItem(zprava.subject, self.window.ui.zpravy)
			font = QtGui.QFont()
			if zprava.unread:
				font.setBold(True)
			item.setFont(font)
			self.window.ui.zpravy.addItem(item)
			if setUnread :
				if zprava.unread:
					self.window.ui.zpravy.setCurrentItem(item)		
					zprava.unread = False
					self.window.ui.subject.setText(zprava.subject)
					self.window.ui.datum.setText(unicode(time.strftime('%X %x',time.localtime(zprava.time))))
					self.window.ui.zprava.setHtml(zprava.body)
					if kontakt.neprectene() == 0:
						kontakt.item.setFont(font)
					setUnread = False
	
	def headlineChanged(self, item):
		log.msg('headlineChanged')
# 		item = self.window.ui.roster.currentItem()
		font =  QtGui.QFont()
		font.setBold(False)
		item.setFont(font)
		jid = unicode(item.text())
		try:
			kontakt = self.kontakty[jid]
		except:
			return
		radek = self.window.ui.zpravy.currentRow()
		zprava = kontakt.zpravy[radek]
		zprava.unread = False
		self.window.ui.subject.setText(zprava.subject)
		self.window.ui.datum.setText(unicode(time.strftime('%X %x',time.localtime(zprava.time))))
		self.window.ui.zprava.setHtml(zprava.body)
		if kontakt.neprectene() == 0:
			kontakt.item.setFont(font)
		self.updateZpravy(jid)
		
	

class Contact:
	def __init__(self, jid, item, plugin):
		self.jid = jid
		self.item = item
		self.plugin = plugin
		self.zpravy = []
	
	def addHeadline(self, subject, body):
		self.zpravy.append(Zprava(subject, body))
		return len(self.zpravy)-1
	
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
