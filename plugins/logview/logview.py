import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from twisted.python import log

class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'logview'
		self.description = 'Extra debug window'
		self.author = "Jiri 'Sef' Gabrys"
		self.name = 'LogView Plugin'
		self.version = '0.04'
		self.category = ['log', 'misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.history = []
		#self.config['notify'] = {'description':'', 'default':'True', 'value': '','type':'boolean'}
		if main:
			self.loadConfig()
			self.window = self.loadWindow("%s/logWindow.ui.py" % self.pluginDir)
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			QtCore.QObject.connect(self.window.ui.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
			QtCore.QObject.connect(self.window.ui.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
			QtCore.QObject.connect(self.window.ui.execute, QtCore.SIGNAL("clicked()"),self.execute)
		else:
			self.loadConfig(homedir)
	
	
	
	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction("Show log",self.showSlot)
	
	def on_remove(self):
		log.removeObserver(self.observer)
	
	def showSlot(self):
		self.window.show()
	
	def enableToggled(self, state):
		if (not self.log) and self.window.ui.enableBox.isChecked():
			self.log = True
			log.addObserver(self.observer)
			self.window.ui.logView.append('Log started')
		else:
			self.log = False
			log.removeObserver(self.observer)
	
	def observer(self, msg):
		self.window.ui.logView.append('[%s] %s' %(time.strftime('%X'), unicode(' '.join(msg['message']))))
		if msg['isError']:
			self.main.tray.showMessage(self.main.tr("Log"),unicode(' '.join(msg['message'])), QtGui.QSystemTrayIcon.Warning, 2000)
	
	def clearLog(self):
		self.window.ui.logView.setText('')
	
	def execute(self):
		code = unicode(self.window.ui.input.toPlainText ())
		self.history.append(code)
		self.window.ui.input.setText('')
		exec(code)
