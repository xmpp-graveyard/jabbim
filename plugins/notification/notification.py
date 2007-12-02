try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys
import os
sys.path.append('.')
from include import plugins, utils

class osd(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self,None,QtCore.Qt.Window | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"),self.hide)
		#self.setFrameShape(self.Box)
		#self.setLineWidth(2)
		#self.setMidLineWidth(0)
		#self.palette().setColor(QtGui.QPalette.Window,self.palette().color(QtGui.QPalette.Highlight))
		#self.palette().setColor(QtGui.QPalette.Text,self.palette().color(QtGui.QPalette.HighlightedText))
		font=QtGui.QApplication.fontMetrics()
		self.f=QtGui.QApplication.font()
		self.f.setPixelSize(40)
		self.f.setBold(True)
		self.text=""
		self.transparent=True
		self.desktop=QtGui.QPixmap()

	def paintEvent(self,event):
		painter=QtGui.QPainter(self)
		painter.setClipping(True)
		#rect=event.region().rects()[0]
		painter.fillRect(0,0,self.width(),self.height(),QtGui.QBrush(QtGui.QColor(0,0,0)))
		
		
		if not self.transparent:
			g=QtGui.QLinearGradient(QtCore.QPointF(100, 100),QtCore.QPointF(200, 200))
			g.setColorAt(0,self.palette().color(QtGui.QPalette.Highlight))
			c=self.palette().color(QtGui.QPalette.Highlight)
			try:
				g.setColorAt(1,c.lighter())
			except:
				g.setColorAt(1,c.light())
			painter.fillRect(1,1,self.width()-2,self.height()-2,QtGui.QBrush(g))
		else:
			painter.drawPixmap(1,1,self.desktop,11,11,self.width()-2,self.height()-2)
			c=self.palette().color(QtGui.QPalette.Highlight)
			c.setAlpha(200)
			painter.fillRect(1,1,self.width()-2,self.height()-2,QtGui.QBrush(c))
		

		
		p=painter.pen()
		painter.setPen(QtGui.QPen(self.palette().color(QtGui.QPalette.HighlightedText)))
		painter.setFont(self.f)
		painter.drawText(QtCore.QRectF(0,0,self.width(),self.height()),QtCore.Qt.AlignCenter,self.text)
		painter.setPen(p)

	def view(self,text="Notification text"):
		self.text=text
		metrics=QtGui.QFontMetrics(self.f)
		height=int(metrics.height())
		width=int(metrics.width(text))
		self.desktop=QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
		self.setGeometry(10,10,width+20,height+10)
		self.show()
		self.timer.start(2000)

class Plugin(plugins.PluginBase):
	def __init__(self,main, homedir):
		plugins.PluginBase.__init__(self, main, homedir)
		self.fname = 'notification'
		self.description = 'System tray and sound notification'
		self.author = "Jan 'HanzZ' Kaluza & Josef 'PepeQ' Halicek"
		self.name = 'Notification Plugin'
		self.version = '0.556'
		self.category = ['notification']
		self.url = 'http://dev.jabbim.cz/jabbim'
		self.config['on_first_message'] = {'description':'Notify on first message from user', 'default':'True', 'value': '','type':'boolean'}
		self.config['on_muc_highlight'] = {'description':'Notify if groupchat message contains your nickname', 'default':'True', 'value': '','type':'boolean'}
		self.config['sound_first_message'] = {'description':'Play sound on first message from user', 'default':'True', 'value': '','type':'boolean'}
		self.config['sound_gc'] = {'description':'Play sound if groupchat message contains your nickname', 'default':'True', 'value': '','type':'boolean'}
		self.config['sound_on_login'] = {'description':'Play sound on login', 'default':'True', 'value': '','type':'boolean'}
		self.soundDir="sounds/" #for now lets say we have no option to change it (but it will change :)
		self.soundAvailable=1 # well, we suppose there is sundsupport
		self.sounds={} # ditictionary of playable actions, will fill in later
		# a few words to sounds directory structure: it has to contains file called simply "config"
		# this file has to contain lines in format: action=filename.wav next line for example:
		# online = user_online.wav
		# GChighlight = groupchat_highlight.wav
		# for list of actions see loadSoundConfig()
		self.loadSoundConfig("sounds/config")
		self.developMode=True
		if main:
			self.registerHandler('on_message', self.on_message)
			self.registerHandler('on_GCmessage', self.on_GCmessage)
			self.loadConfig()
			self.installTranslator()
			self.playsound('start')
			self.osd=osd()
			#self.timer=QtCore.QTimer()
			#QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.changeIcon)
			#self.main.tray.showMessage(self.tr("Notification"),self.tr("Notification plugin is activated"), QtGui.QSystemTrayIcon.Information, 2000)
		else:
			self.loadConfig(homedir)

	def loadSoundConfig(self, configFile):
		try:
			soubor = open(configFile,'r')
			lines = soubor.readlines()
			for line in lines:
					self.sounds[line.split(' = ')[0]]=line.split(' = ')[1] # so ... now, we have a dictionary
			soubor.close() # thats all we need
		except IOError:
			self.soundAvailable=0
			print "Some error occured! (IOError loading sound config file %s)"%(configFile)

	def playsound(self, action):
		if self.soundAvailable:
			if self.sounds.has_key(action): # if exist the action file
				if sys.platform == 'linux2': # linux sounds are produced using aplay
					os.system('aplay -q '+self.soundDir+self.sounds[action].strip('\n')+' &')
				else:
					QtGui.QSound.play(self.soundDir+self.sounds[action].strip('\n'))

	def buildRosterMenu(self):
		menu=self.rosterMenu()
		menu.addAction("Notification test",self.testSlot)

	def testSlot(self):
		self.main.tray.showMessage(self.tr("Notification "),self.tr("Notification plugin test :)"), QtGui.QSystemTrayIcon.Information, 2000)
		self.playsound('new_message')
		self.osd.view()

	#def startTrayBlink(self,icon="images/16x16/actions/message.png"):
		#self.trayIcon=QtGui.QIcon(icon)
		#self.ico=True
		#self.timer.start(500)
		#self.main.tray.setIcon(self.trayIcon)

	def changeIcon(self):
		if self.ico:
			self.main.tray.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
			self.ico=False
		else:
			self.ico=True
			self.main.tray.setIcon(self.trayIcon)

	def on_message(self,frm,typ,body,subject, xhtml,  chatstate,  delay, error):
		if body == None:
			return
		self.playsound('message')
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
					print "coe?"
					self.playsound('new_message')
					#self.main.tray.showMessage(self.tr("New message from ")+unicode(user), traytext, QtGui.QSystemTrayIcon.Information, 5000)
					print unicode(user)
					#self.startTrayBlink()
				else:
					print "pyco coe?"
					self.playsound('message')
	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None, error = None):
		if delay != None:
			return
		if len(unicode(frm).rsplit("/"))==2:
			user=unicode(frm).rsplit("/")[1]
			frm=unicode(frm).rsplit("/")[0]
		else:
			user=frm
		#print self.config['on_muc_highlight']['value']
		if self.config['on_muc_highlight']['value']=="True" or self.config['sound_gc_message']['value']=="True":
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==frm:
					if user == w.name:
						continue
					#print "test"
					if utils.need_highlight(unicode(w.name), unicode(body)):
						if len(body)>40:
								text=body[:40]+" ..."
						else:
								text=body
						traytext=unicode(user)+": "+text
						if self.config['sound_gc_message']['value']=="True":
							self.playsound('message')
						self.main.tray.showMessage(self.tr("New groupchat message for you"), traytext, QtGui.QSystemTrayIcon.Information, 5000)
