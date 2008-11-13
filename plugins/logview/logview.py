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
		self.config['historySave']={'type':'boolean-radio','label':main.tr('History saving type'),'value':'one','options':{'one':main.tr('always after command input'),'close':main.tr('on jabbim close'),'never':main.tr('never')}}
		self.config['historyData']={'type':'hidden','value':''}
		tempPreset=[]
		for i in range(10):
			tempPreset.append(base64.b64encode("print \'This is preset nr. %d\'" % i))
			
		self.config['presetData']={'type':'hidden','value':tempPreset}
		self.config['__sort__']=['notify','historyMaxCount','historySave','historyData']
		
class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'logview'
		self.installTranslator()
		self.description = self.tr('Extra debug window')
		self.author = "Jiri 'Sef' Gabrys, Ondra 'triak' Kunc"
		self.name = self.tr('LogView Plugin')
		self.version = '0.050'
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
		#Ctrl-R to erase log
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_R | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.clearLog)
		#Ctrl-E toggles enable/disable log output
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_E | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.toggleShell)
		#Ctrl+Up lists history to past
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.historyForward)
		#Ctrl+Down lists history to recently executed
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.historyBackward)
		#Ctrl+Enter(Return) executes command list
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Return),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.execute)
		#Ctrl+Shift+Up inserts previous command from history to the top of current shell
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up | QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.shellAppendPrevious)
		#preset save & load
			def gen_preset(n, load):
				if load:
					def call_it(): self.shellLoadPreset(n)
				else:
					def call_it(): self.shellSavePreset(n)
				return call_it
			keys = [QtCore.Qt.Key_0, QtCore.Qt.Key_1, QtCore.Qt.Key_2, QtCore.Qt.Key_3, QtCore.Qt.Key_4,
				QtCore.Qt.Key_5, QtCore.Qt.Key_6, QtCore.Qt.Key_7, QtCore.Qt.Key_8, QtCore.Qt.Key_9]
			for i in range(len(keys)):
				short=QtGui.QShortcut(QtGui.QKeySequence(keys[i] | QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier),self.window)
				QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"), gen_preset(i, False))
				short=QtGui.QShortcut(QtGui.QKeySequence(keys[i] | QtCore.Qt.ControlModifier),self.window)
				QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"), gen_preset(i, True))
		else:
			self.loadConfig(homedir)
	
	def buildMainWindowMenu(self):
		menu=self.mainWindowMenu()
		menu.addAction("Show log",self.showSlot)
	
	def buildMainWindowToolBar(self):
                self.toolBarButton = self.mainWindowToolBarButton()
                self.toolBarButton.setIconSize(QtCore.QSize(16,16))
		self.toolBarButton.setIcon(QtGui.QIcon("%s/icon.png" % self.pluginDir))
                QtCore.QObject.connect(self.toolBarButton, QtCore.SIGNAL("clicked()"), self.showSlot)
	
	def on_remove(self):
		if self.config['historySave']=='close':
			self.saveHistory();
		try:
			log.removeObserver(self.observer)
		except ValueError:
			pass # fixes problem with removal of unregistered observer
	
	def showSlot(self):
		self.window.show()
	def toggleShell(self):
		self.window.ui.enableBox.setChecked(not self.window.ui.enableBox.isChecked())
		
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
			self.saveHistory()
		self.window.ui.input.setText('')
		exec(code)
	def saveHistory(self):
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
	def shellAppendPrevious(self):
		self.historyPosition+=1;
		if self.historyPosition>=(len(self.history)-1):
			self.historyPosition=len(self.history)-1;
		else:
			self.window.ui.input.setText("%s\n%s" % (self.history[self.historyPosition],self.window.ui.input.toPlainText()))

	def historyBackward(self):
		self.historyPosition-=1;
		if self.historyPosition<0:
			self.historyPosition=0;
			self.window.ui.input.setText('')
		else:
			self.window.ui.input.setText(self.history[self.historyPosition])
	def shellSavePreset(self,order):
#		tmpPreset=self.config['presetData']
#		tmpPreset[order]=unicode(self.window.ui.input.toPlainText ())
		self.config['presetData'][order]=base64.b64encode(unicode(self.window.ui.input.toPlainText ()))
		self.config.write();

	def shellLoadPreset(self,order):
		self.window.ui.input.setText(base64.b64decode(self.config['presetData'][order]))
