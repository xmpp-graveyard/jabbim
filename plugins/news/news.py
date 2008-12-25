import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from urllib import quote, unquote
from twisted.python import log
from include import utils
from pyxl import jid
#exp = re.compile(" (((https?://)|(ftp://)|(www\.))[^\ ]+)|(([^\ ]*\.){2,}[0-9a-z-A-Z]{2,4}(/[^\ ]*)?)")
#exp.search('http://jabbim.cz/').group()

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['notify_tray']={'type':'boolean','label':self.main.tr("Notify in tray"),'value':'True'}
		self.config['notify_show']={'type':'boolean','label':self.main.tr("Show window on new"),'value':'True'}
		self.config['__sort__']=['notify_tray','notify_show']

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'news'
		self.description = 'Headlines window'
		self.author = u"Jiří 'Sef' Gabryš"
		self.name = 'News Plugin'
		self.version = '0.062'
		self.category = ['misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.kontakty = {} # jid:contact
		#self.config['notify_tray'] = {'description':'Notify in tray', 'default':'True', 'value': '','type':'boolean'}
		#self.config['notify_show'] = {'description':'Show window on new', 'default':'True', 'value': '','type':'boolean'}
		self.installTranslator()
		self.configDialog=config(self)
		if main:
			self.loadConfig()
			#self.installTranslator()
			self.window = self.loadWindow("%s/news.ui.py" % self.pluginDir)
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			self.registerHandler('on_message', self.on_message, priority=4)

##			self.window.ui.treeWidget.addTopLevelItem(QtGui.QTreeWidgetItem(['test', 'http://www.jabbim.cz']))
##			items = self.window.ui.treeWidget.findItems('test', QtCore.Qt.MatchExactly,0)
##			itemClicked ( QTreeWidgetItem * item, int column )
			QtCore.QObject.connect(self.window.ui.treeWidget, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem *, int )"),self.itemClicked)


		else:
			self.loadConfig(homedir)

	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction(self.main.tr("Show news"),self.showSlot)

	def showSlot(self):
		self.window.show()

	def itemClicked(self, item, col):
		self.window.ui.webView.load(QtCore.QUrl((item.data(1,0).toString())))

	def findUrl(self,body):
		url = ""
		for slovo in body.split(' '):
			if slovo.find('http://') !=-1:
				url = slovo
				continue
			elif slovo.startswith('www.'):
				url = 'http://' + slovo
		print 'url: ', url
		return url

	def on_message(self, msg):
		frm, typ, body, subject ,  xhtml,chatstate ,  delay, error = msg.legacyUnpack()
		print 'received headline!'
		if typ != 'headline':
			return True
		frm = jid.JID(frm)
##		body = utils.replace_url(body,self.main)
		items = self.window.ui.treeWidget.findItems(frm.userhost(), QtCore.Qt.MatchExactly,0)
		if len(items) == 0:
			item = QtGui.QTreeWidgetItem([frm.userhost()])
			self.window.ui.treeWidget.addTopLevelItem(item)
		else:
			item  = items[0]
		url = self.findUrl(body)
		print 'url'
		print url
		headline = QtGui.QTreeWidgetItem([subject, url])
		headline.setToolTip(0,body)
		item.addChild(headline)

		if self.config['notify_tray']=='True':
			self.main.tray.showMessage("News",subject, QtGui.QSystemTrayIcon.Information, 3000)
 			#self.main.events.addInfoEvent(header=self.tr("News: ")+subject,text=self.tr("From: ")+frm,typ='newHeadline',icon="images/32x32/status/rss-online.png", action = self.eventActivated, actionDict = [frm, index], trueCall = self.eventActivated, trueDict = [frm, index], name = '%s-%d'%(frm, index))
		if self.config['notify_show']=='True':
			self.window.show()
		print 'returning false'
		return False

	def eventActivated(self, frm, index):
		print frm, index
		item = self.kontakty[frm].item
		self.window.ui.roster.setCurrentItem(item)

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
		self.updateZpravy(frm, False)
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
# 			if setUnread :
# 				if zprava.unread:
# 					self.window.ui.zpravy.setCurrentItem(item)
# 					zprava.unread = False
# 					self.window.ui.subject.setText(zprava.subject)
# 					self.window.ui.datum.setText(unicode(time.strftime('%X %x',time.localtime(zprava.time))))
# 					self.window.ui.zprava.setHtml(zprava.body)
# 					if kontakt.neprectene() == 0:
# 						kontakt.item.setFont(font)
# 					setUnread = False

	def headlineChanged(self, item):
		log.msg('headlineChanged')
 		itm = self.window.ui.roster.currentItem()
		font =  QtGui.QFont()
		font.setBold(False)
		item.setFont(font)
		jid = unicode(itm.text())
		try:
			kontakt = self.kontakty[jid]
		except:
			return
		radek = self.window.ui.zpravy.currentRow()
		self.removeEvent('%s-%d'%(jid, radek))
		zprava = kontakt.zpravy[radek]
		zprava.unread = False
		self.window.ui.subject.setText(zprava.subject)
		self.window.ui.datum.setText(unicode(time.strftime('%X %x',time.localtime(zprava.time))))
		self.window.ui.zprava.setHtml(zprava.body)
		if kontakt.neprectene() == 0:
			kontakt.item.setFont(font)
		self.updateZpravy(jid)

	def removeEvent(self, name):
		ev = list(self.main.events.events)
		for event in ev:
			if event['name'] == name and event['typ'] == 'newHeadline':
				event['widget'].closeClicked()
				break



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
