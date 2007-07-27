import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui, uic
from urllib import quote, unquote
from twisted.python import log

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'archive'
		self.description = 'Message Archiving'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'Archive Plugin'
		self.version = '0.045'
		self.category = ['archive']
		self.url = 'http://dev.jabbim.cz/jabbim'
# 		self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}


		if main:
			self.jid = quote(self.main.client.jid.userhost())
			if not os.path.isdir(self.main.homeDir+'/archive'):
				os.mkdir(self.main.homeDir+'/archive')
					
			if not os.path.isdir(self.main.homeDir+'/archive/'+self.jid):
				os.mkdir(self.main.homeDir+'/archive/'+self.jid)
			self.registerHandler('on_message', self.on_message)
			self.registerHandler('on_message_send', self.on_message_send)
			self.loadConfig()
			self.window = uic.loadUi("%s/plugins/%s/historyBrowser.ui"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			QtCore.QObject.connect(self.window.seznam, QtCore.SIGNAL("itemClicked ( QListWidgetItem* ) "),self.itemClicked)
			QtCore.QObject.connect(self.window.calendar, QtCore.SIGNAL("selectionChanged()"),self.calChanged)
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Archive browser",self.showSlot)
	
	def showSlot(self):
		seznam = os.listdir(self.main.homeDir+'/archive/'+self.jid)
		for jid in seznam:
			if os.path.isdir(self.main.homeDir+'/archive/'+self.jid+'/'+jid):
				continue
			else:
				self.window.seznam.addItem(unquote(jid).split('.history')[0])
		self.window.show()
	
	def calChanged(self):	
		log.msg("date clicked")
		self.window.text.setText('')
		jid = quote(unicode(self.seznam.currentItem ().text()))
		try:
			fp = open(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history')
			zpravy = fp.readlines()
			fp.close()
		except:
			log.err('no history file')
			return
		datum = self.window.calendar.selectedDate().toString('dd-MM-yyyy')
		if len(zpravy)>0:
			for zprava in zpravy:
	# 			log.msg(zprava)
				casti = zprava.split('|')
	# 			log.msg(unicode(casti))
				if datum == time.strftime('%d-%m-%Y', time.localtime(float(casti[0]))):
					self.window.text.append(unicode('[%s] %s' %(time.strftime('%X', time.localtime(float(casti[0]))), casti[5]), 'utf8'))

	
	def itemClicked(self, item):
		log.msg("item clicked")
		self.window.text.setText('')
		jid = quote(unicode(item.text()))
		try:
			fp = open(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history')
			zpravy = fp.readlines()
			fp.close()
		except:
			log.err('no history file')
			return
		datum = self.window.calendar.selectedDate().toString('dd-MM-yyyy')
		if len(zpravy)>0:
			for zprava in zpravy:
	# 			log.msg(zprava)
				casti = zprava.split('|')
	# 			log.msg(unicode(casti))
				if datum == time.strftime('%d-%m-%Y', time.localtime(float(casti[0]))):
					self.window.text.append(unicode('[%s] %s' %(time.strftime('%X', time.localtime(float(casti[0]))), casti[5]), 'utf8'))
	
	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay):
		jid = quote(frm.split('/')[0])

		fp = open(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history', 'a')
		if xhtml != None:
			telo = xhtml.replace('|', '\\|')
		else:
			telo = body.replace('|', '\\|')
		msg = '|'.join([unicode(time.time()), 'from', jid, typ, quote(unicode(subject)), telo])
		msg = msg.encode('utf8')
		fp.write(msg+'\n')
		fp.close()
	
	def on_message_send (self, to, body, typ, subject,composing, xhtml,  muc):
		if not muc:
			jid = quote(to.split('/')[0])
			fp = open(self.main.homeDir+'/archive/'+self.jid+'/'+jid+'.history', 'a')
			if xhtml != None:
				telo = xhtml.replace('|', '\\|')
			else:
				telo = body.replace('|', '\\|')
			msg = '|'.join([unicode(time.time()), 'to', jid, typ, quote(unicode(subject)), telo])
			msg = msg.encode('utf8')
			fp.write(msg+'\n')
			fp.close()
