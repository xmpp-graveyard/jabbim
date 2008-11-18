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
		self.config['historySave']={'type':'boolean-radio','label':self.main.tr('History saving type'),'value':'one','options':{'one':main.tr('always after command input'),'close':main.tr('on jabbim close'),'never':main.tr('never')}}
		self.config['historyDataPy']={'type':'hidden','value':''}
		self.config['historyDataXML']={'type':'hidden','value':''}
		pyPreset=['#0. volna pozice, novy preset ulozite pomoci Ctrl+Shift+0\n',
			'#1. vypis features konkretniho kontaktu\nself.main.client.getFeaturesByJid(JID)',
			'#2. jid z retezce\nself.main.getJid(JID)',
			'#3. ziskani celeho jid i s nejprioritnejsi resource\nself.main.client.getHighestJid(JID)',
			'#4. ziskani kontaktu v rosteru\nself.main.client.getContactByJid(jid)',
			'#5. nacteni pluginu\nself.main.loadPlugin(\'plugin\');\nself.main.config[\'plugins\'].append(\'plugin\');',
			'#6. vyhozeni pluginu\nself.main.unloadPlugin(\'plugin\');\nself.main.config[\'plugins\'].remove(\'plugin\');',
			'#7. volna pozice, novy preset ulozite pomoci Ctrl+Shift+7',
			'#8. volna pozice, novy preset ulozite pomoci Ctrl+Shift+8',
			'#9. volna pozice, novy preset ulozite pomoci Ctrl+Shift+9']
		tempPreset=[]
		for i in range(10):
			tempPreset.append(base64.b64encode(pyPreset[i]));			
		self.config['presetDataPy']={'type':'hidden','value':tempPreset}
		xmlPreset=['#0. volna pozice, novy preset ulozite pomoci Ctrl+Shift+0\n',
			"<iq to='USER@DOMAIN' from='you@yourserver.tld'>\n<query xmlns=''>\n</iq>",
			"<message to='USER@DOMAIN' from='you@yourserver.tld'>\n<body>Body text</body>\n</message>",
			"<presence from='you@yourserver.tld'>\n<show>???</show>\n<status>???</status>\n</presence>",
			'#4. volna pozice, novy preset ulozite pomoci Ctrl+Shift+4',
			'#5. volna pozice, novy preset ulozite pomoci Ctrl+Shift+5',
			'#6. volna pozice, novy preset ulozite pomoci Ctrl+Shift+6',
			'#7. volna pozice, novy preset ulozite pomoci Ctrl+Shift+7',
			'#8. volna pozice, novy preset ulozite pomoci Ctrl+Shift+8',
			'#9. volna pozice, novy preset ulozite pomoci Ctrl+Shift+9']
		tempPreset=[]
		for i in range(10):
			tempPreset.append(base64.b64encode(xmlPreset[i]));			

		self.config['presetDataXML']={'type':'hidden','value':tempPreset}		
		self.config['__sort__']=['notify','historyMaxCount','historySave','historyData']
		
class Plugin(plugins.PluginBase):
	def __init__(self, main, homedir, plugindir):
		plugins.PluginBase.__init__(self, main, homedir, plugindir)
		self.fname = 'devconsole'
		self.installTranslator()
		self.description = self.tr('Extra debug window')
		self.author = "Jiri 'Sef' Gabrys, Ondra 'triak' Kunc"
		self.name = self.tr('DevConsoles Plugin')
		self.version = '0.060'
		self.category = ['log', 'misc']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.historyPy = []
		self.historyXML = []
		self.historyPyPosition=-1;
		self.historyXMLPosition=-1;
		self.configDialog=config(self)
		if main:
			self.loadConfig()
			self.loadHistory()
			self.window = self.loadWindow("%s/devconsole.ui.py" % self.pluginDir)
			self.window.setWindowIcon(self.main.windowIcon())
			self.window.ui.tabWidget.setTabIcon(0,QtGui.QIcon("%s/xml.png" % self.pluginDir))
			self.window.ui.tabWidget.setTabIcon(1,QtGui.QIcon("%s/python.png" % self.pluginDir))
			self.log = False
			self.registerHandler('onXmlEvent',self.onXml)

		#both tabs
			#Ctrl+Enter(Return) executes command list
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL | QtCore.Qt.Key_Return),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.ctrlEnter)
			#Ctrl-E toggles enable/disable log output
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_E | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.toggleEnabled)
			
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_S | QtCore.Qt.AltModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.setTabShell)
			
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_X | QtCore.Qt.AltModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.setTabXML)
			
			#Ctrl-R to erase log
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_R | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.clearLog)
			#Ctrl+Up lists history to past
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.historyBackward)
			#Ctrl+Down lists history to recently executed
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Down | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.historyForward)
		#xml console
			QtCore.QObject.connect(self.window.ui.send,QtCore.SIGNAL("clicked()"),self.send)
			QtCore.QObject.connect(self.window.ui.message,QtCore.SIGNAL("clicked()"),self.message)
			QtCore.QObject.connect(self.window.ui.presence,QtCore.SIGNAL("clicked()"),self.presence)
			QtCore.QObject.connect(self.window.ui.iq,QtCore.SIGNAL("clicked()"),self.iq)
			QtCore.QObject.connect(self.window.ui.clear,QtCore.SIGNAL("clicked()"),self.clearLog)
			
		#python console
			QtCore.QObject.connect(self.window.ui.enableBox, QtCore.SIGNAL("stateChanged(int)"),self.enableToggled)
			QtCore.QObject.connect(self.window.ui.clearButton, QtCore.SIGNAL("clicked()"),self.clearLog)
			QtCore.QObject.connect(self.window.ui.execute, QtCore.SIGNAL("clicked()"),self.execute)
			#Ctrl+Shift+Up inserts previous command from history to the top of current shell
			short=QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up | QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier),self.window)
			QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.shellAppendPrevious)
			#preset save & load
			def gen_preset(n, load):
				if load:
					def call_it(): self.loadPreset(n)
				else:
					def call_it(): self.savePreset(n)
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
		menu.addAction("Show console",self.showSlot)
	
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
	def toggleEnabled(self):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.window.ui.enableBox.setChecked(not self.window.ui.enableBox.isChecked())
		else:
			self.window.ui.enable.setChecked(not self.window.ui.enable.isChecked())
		
	def enableToggled(self, state):
		if (not self.log) and self.window.ui.enableBox.isChecked():
			self.log = True
			log.addObserver(self.observer)
			self.window.ui.logView.append('Log started')
		else:
			self.log = False
			log.removeObserver(self.observer)
	
	def observer(self, msg, fromThread=False):
		if not fromThread:
			self.main.reactor.callFromThread(self.observer,msg,True)
			return
		self.window.ui.logView.append('[%s] %s' %(time.strftime('%X'), unicode(' '.join(msg['message']).replace("<","&lt;").replace(">","&gt;"))))
		if msg['isError'] and self.config['notify'] == 'True':
			self.main.tray.showMessage(self.main.tr("Log"),unicode(' '.join(msg['message'])), QtGui.QSystemTrayIcon.Warning, 2000)
	
	def clearLog(self):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.window.ui.logView.setText('');
		else:
			self.window.ui.xml.setText('');
	def ctrlEnter(self):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.execute()
		else:
			self.send()
	
	def execute(self):
		code = unicode(self.window.ui.input.toPlainText ())
		self.window.ui.logView.append(self.window.ui.input.toPlainText ())
		self.historyPy.insert(0,code)
		self.historyPy=self.historyPy[0:long(self.config['historyMaxCount'])]
		self.historyPyPosition=-1;
		if self.config['historySave']=='one':
			self.saveHistory()
		self.window.ui.input.setText('')
		exec(code)
	def saveHistory(self):
		tmpHistory=[];
		for historyItem in self.historyPy:
			tmpHistory.append(base64.b64encode(historyItem));
		self.config['historyDataPy']=tmpHistory
		tmpHistory=[];
		for historyItem in self.historyXML:
			tmpHistory.append(base64.b64encode(historyItem));
		self.config['historyDataXML']=tmpHistory
		self.config.write()
	def loadHistory(self):
		self.historyPy=[];
		self.historyXML=[];
		tmpHistory=self.config['historyDataPy'];
		for historyItem in tmpHistory:
			self.historyPy.append(base64.b64decode(historyItem))
		tmpHistory=self.config['historyDataXML'];
		for historyItem in tmpHistory:
			self.historyXML.append(base64.b64decode(historyItem))
	def historyForward(self):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.historyPyPosition-=1;
			if self.historyPyPosition<0:
				self.historyPyPosition=-1;
				self.window.ui.input.setText('')
			else:
				self.window.ui.input.setText(self.historyPy[self.historyPyPosition])
		else:
			self.historyXMLPosition-=1;
			if self.historyXMLPosition<0:
				self.historyXMLPosition=-1;
				self.window.ui.textEdit.setText('')
			else:
				self.window.ui.textEdit.setText(self.historyXML[self.historyXMLPosition])
			
	def shellAppendPrevious(self):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.historyPyPosition+=1;
			if self.historyPyPosition>(len(self.historyPy)-1):
				self.historyPyPosition=len(self.historyPy)-1;
			else:
				self.window.ui.input.setText("%s\n%s" % (self.historyPy[self.historyPyPosition],self.window.ui.input.toPlainText()))
		else:
			self.historyXMLPosition+=1;
			if self.historyXMLPosition>(len(self.historyXML)-1):
				self.historyXMLPosition=len(self.historyXML)-1;
			else:
				self.window.ui.textEdit.setText("%s\n%s" % (self.historyXML[self.historyXMLPosition],self.window.ui.textEdit.toPlainText()))	

	def historyBackward(self):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.historyPyPosition+=1;
			if self.historyPyPosition>=len(self.historyPy):
				self.historyPyPosition=len(self.historyPy);
				self.window.ui.input.setText(self.tr('print \'History END\''))
			else:
				self.window.ui.input.setText(self.historyPy[self.historyPyPosition])
		else:
			self.historyXMLPosition+=1;
			if self.historyXMLPosition>=len(self.historyXML):
				self.historyXMLPosition=len(self.historyXML);
				self.window.ui.textEdit.setText(self.tr("<message>------HISTORY-END------</message>"))
			else:
				self.window.ui.textEdit.setText(self.historyXML[self.historyXMLPosition])
	def savePreset(self,order):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.config['presetDataPy'][order]=base64.b64encode(unicode(self.window.ui.input.toPlainText ()))
			self.config.write();
		else:
			self.config['presetDataXML'][order]=base64.b64encode(unicode(self.window.ui.textEdit.toPlainText ()))
			self.config.write();

	def loadPreset(self,order):
		if self.window.ui.tabWidget.currentIndex()==1:
			self.window.ui.input.setText(base64.b64decode(self.config['presetDataPy'][order]))
		else:
			self.window.ui.textEdit.setText(base64.b64decode(self.config['presetDataXML'][order]))
		
	def iq(self):
		self.window.ui.textEdit.setText("<iq to='USER@DOMAIN' from='"+self.main.client.jid.full()+"'>\n<query xmlns=''>\n</iq>")

	def message(self):
		self.window.ui.textEdit.setText("<message to='USER@DOMAIN' from='"+self.main.client.jid.full()+"'>\n<body>Body text</body>\n</message>")

	def presence(self):
		self.window.ui.textEdit.setText("<presence from='"+self.main.client.jid.full()+"'>\n<show>???</show>\n<status>???</status>\n</presence>")

	def send(self):
		text=unicode(self.window.ui.textEdit.toPlainText())
		self.historyXML.insert(0,text)
		self.historyXML=self.historyXML[0:long(self.config['historyMaxCount'])]
		self.historyXMLPosition=-1;
		try:
			self.main.client.xmlstream.send(text)
		except:
			log.err("can't send")
		self.window.ui.textEdit.setText("")
		if self.config['historySave']=='one':
			self.saveHistory()
	def onXml(self,xml):
		if self.window.ui.enable.isChecked():
			text=unicode(xml);
			self.window.ui.xml.append(text+"\n\n");
	def setTabXML(self):
		self.window.ui.tabWidget.setCurrentIndex(0);
	
	def setTabShell(self):
		self.window.ui.tabWidget.setCurrentIndex(1);

