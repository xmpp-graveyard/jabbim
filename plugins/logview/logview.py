import sys,os,time
sys.path.append('.')
from include import plugins
from PyQt4 import QtCore, QtGui
from twisted.python import log
import base64

class config:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['notify']={'type':'boolean','label':self.main.tr("Notify on error?"),'value':'False'}
		self.config['historyMaxCount']={'type':'number-spin','label':self.main.tr("Max history entries"),'value':'50'}
		self.config['historySave']={'type':'boolean-radio','label':main.tr('History saving type'),'value':'one','options':{'one':main.tr('always after command input'),'btn':main.tr('button clicked'),'never':main.tr('never')}}
		self.config['historyData']={'type':'hidden','value':''}
		self.config['__sort__']=['notify','historyMaxCount','historySave','historyData']
		
class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'logview'
		self.installTranslator()
		self.description = self.tr('Extra debug window')
		self.author = "Jiri 'Sef' Gabrys, Ondra 'triak' Kunc"
		self.name = self.tr('LogView Plugin')
		self.version = '0.042'
		self.category = ['log', 'misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.history = []
		self.historyPosition=-1;
		self.configDialog=config(self)
		if main:
			self.loadConfig()
			self.loadHistory()
			self.window = self.loadWindow("%s/logWindow.ui.py" % self.pluginDir)
			self.window.setWindowIcon(self.main.windowIcon())
			self.log = False
			QtCore.QObject.connect(self.window.ui.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
			QtCore.QObject.connect(self.window.ui.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
			QtCore.QObject.connect(self.window.ui.execute, QtCore.SIGNAL("clicked()"),self.execute)
#			short=QtGui.QShortcut("ctrl+f",self.window)
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.historyForward)
#			short=QtGui.QShortcut("ctrl+b",self.window)
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.historyBackward)
#			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Enter),self.window)
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Return),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.execute)
			#QtCore.Qt.Key_Enter a QtCore.Qt.CTRL

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
		self.window.ui.logView.append('[%s] %s' %(time.strftime('%X'), unicode(' '.join(msg['message']).replace("<","&lt;").replace(">","&gt;"))))
		if msg['isError'] and self.config['notify'] == 'True':
			self.main.tray.showMessage(self.main.tr("Log"),unicode(' '.join(msg['message'])), QtGui.QSystemTrayIcon.Warning, 2000)
	
	def clearLog(self):
		self.window.ui.logView.setText('')
	
	def execute(self):
		code = unicode(self.window.ui.input.toPlainText ())
		self.window.ui.logView.append(self.window.ui.input.toPlainText ())
		self.history.insert(0,code)
		self.history=self.history[0:long(self.config['historyMaxCount'])]
		self.historyPosition=-1;
		if self.config['historySave']=='one':
			self.historySave()
		self.window.ui.input.setText('')
		exec(code)
	def historySave(self):
		tmpHistory=[];
		for historyItem in self.history:
			tmpHistory.append(base64.b64encode(historyItem));
		self.config['historyData']=tmpHistory
		self.config.write()
	def loadHistory(self):
		self.history=[];
		tmpHistory=self.config['historyData'];
		for historyItem in tmpHistory:
			self.history.append(base64.b64decode(historyItem))
	def historyForward(self):
		self.historyPosition+=1;
		if self.historyPosition>=(len(self.history)-1):
			self.historyPosition=len(self.history)-1;
			self.window.ui.input.setText(self.tr('print \'history ends here\''))
		else:
			self.window.ui.input.setText(self.history[self.historyPosition])
	def historyBackward(self):
		self.historyPosition-=1;
		if self.historyPosition<0:
			self.historyPosition=0;
			self.window.ui.input.setText('')
		else:
			self.window.ui.input.setText(self.history[self.historyPosition])
