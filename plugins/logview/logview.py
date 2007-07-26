import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui, uic
from twisted.python import log

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'logview'
		self.description = 'Extra debug window'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'LogView Plugin'
		self.version = '0.0222'
		self.category = ['log', 'misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		#self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.window = uic.loadUi("%s/plugins/%s/logWindow.ui"%(self.homeDir, self.fname))
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			QtCore.QObject.connect(self.window.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
			QtCore.QObject.connect(self.window.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
			
	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Show log",self.showSlot)
	
	def showSlot(self):
		self.window.show()
	
	def enableToggled(self, state):
		if (not self.log) and self.window.enableBox.isChecked():
			self.log = True
			log.addObserver(self.observer)
# 			self.window.logView.append('Log started')
		else:
			self.log = False
			log.removeObserver(self.observer)
	
	def observer(self, msg):
		self.window.logView.append('[%s] %s' %(time.strftime('%X'), unicode(' '.join(msg['message']))))
		if msg['isError']:
			self.main.tray.showMessage(self.main.tr("Log"),unicode(' '.join(msg['message'])), QtGui.QSystemTrayIcon.Warning, 2000)
	
	def clearLog(self):
		self.window.logView.setText('')
