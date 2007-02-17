"""
Piskvorky is jabber based game.
Copyright (C) 2007 Jan Kaluza

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
	
from jabber import *
import sys,os,time,random
from configobj import ConfigObj

from mainwindow import *
from login import *
from preferences import *
from roster import *
from status import *
from chatwindow import *
from joingroupchat import *
from addcontact import *

#import games

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=Ui_mainWindow()
		self.ui.setupUi(self)
		self.loadRoster()
		# Signals
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.addContact, QtCore.SIGNAL("clicked(bool)"),self.addContact)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tick)
		self.timer.start(50)
		self.homeDir=self.getHomeDir()
		self.loadConfig()
		self.loadSkin()
		self.loadStatus()
		self.loadBookmarks()
		self.loadGroupchat()
		self.groupchat=[]
		self.users={}
		self.groups={}
		self.groups["Unknown"]={"item":self.ui.roster,"users":{}}
		self.chat=chatWindow(self,self,jab)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)

	def preferencesClicked(self,bool):
		# shows preferences
		w=preferencesWindow(self,self)
		w.show()


	def loadSkin(self):
		# loads config and repairs config file
		self.skin=ConfigObj('skins/default.conf',encoding='UTF8')

	def addContact(self,bool):
		contact=addContactWindow(self,jab)
		contact.exec_()

	def loadGroupchat(self):
		self.groupchatMenu=QtGui.QMenu(self.ui.groupchat)
		
		action=self.groupchatMenu.addAction(self.tr("Join new groupchat"))
		action.setData(QtCore.QVariant("new"))
		
		self.groupchatMenu.addSeparator()
		
		for k,v in self.bookmarks.iteritems():
			action=self.groupchatMenu.addAction(unicode(k))
			action.setData(QtCore.QVariant(v))
		
		self.ui.groupchat.setMenu(self.groupchatMenu)
		app.connect(self.groupchatMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.groupchatChanged)

	def loadRoster(self):
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=rosterWidget(self.ui.rosterWidget,self,jab)
		layout.addWidget(self.ui.roster)

	def loadStatus(self):
		self.statuses={"online":QtGui.QIcon("images/status/online.png"),
						"available":QtGui.QIcon("images/status/online.png"),
						"offline":QtGui.QIcon("images/status/offline.png"),
						"chat":QtGui.QIcon("images/status/chat.png"),
						"away":QtGui.QIcon("images/status/away.png"),
						"xa":QtGui.QIcon("images/status/xa.png"),
						"dnd":QtGui.QIcon("images/status/dnd.png"),
						"None":QtGui.QIcon("images/status/offline.png")
						}
		self.nickSort={"online":"1",
						"available":"1",
						"chat":"2",
						"away":"3",
						"xa":"4",
						"dnd":"5",
						"None":"9",
						"offline":"9"
						}
		self.statusMenu=QtGui.QMenu(self.ui.statusButton)
		action=self.statusMenu.addAction(self.statuses['online'],self.tr("Online"))
		action.setData(QtCore.QVariant("online"))
		action=self.statusMenu.addAction(self.statuses['chat'],self.tr("Chatty"))
		action.setData(QtCore.QVariant("chat"))
		action=self.statusMenu.addAction(self.statuses['away'],self.tr("Away"))
		action.setData(QtCore.QVariant("away"))
		action=self.statusMenu.addAction(self.statuses['xa'],self.tr("Extended away"))
		action.setData(QtCore.QVariant("xa"))
		action=self.statusMenu.addAction(self.statuses['dnd'],self.tr("DND"))
		action.setData(QtCore.QVariant("dnd"))
		self.ui.statusButton.setMenu(self.statusMenu)
		app.connect(self.statusMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusChanged)
		self.offline=True


	def groupchatChanged(self,action):
		data=action.data()
		data=data.toString()
		if data=="new":
			newchat=joinGroupChatWindow(self,jab)
			ret=newchat.exec_()
			if ret==1:
				self.chat.show()
		else:
			room=unicode(action.text())
			nickname=unicode(data)
			jab.getIntoRoom(room,nickname)
			self.groupchat.append(room)
			self.chat.addGroupChatTab(room,nickname)
	def statusChanged(self,action):
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.statuses[str(data)])
		setstatus=statusWindow(data)
		setstatus.exec_()


	def loadBookmarks(self):
		# loads config and repairs config file
		self.bookmarks=ConfigObj(self.homeDir+'/.jgames/bookmarks',encoding='UTF8')
		if len(self.bookmarks)==0:
			if not os.path.isdir(self.homeDir+'/.jgames'):
				os.mkdir(self.homeDir+'/.jgames')
			self.bookmarks=ConfigObj(self.homeDir+'/.jgames/bookmarks',encoding='UTF8')
			self.bookmarks.write()

	def loadConfig(self):
		# loads config and repairs config file
		configs=["jid","passwd","savePasswd"]
		self.config=ConfigObj(self.homeDir+'/.jgames/config',encoding='UTF8')
		if len(self.config)==0:
			if not os.path.isdir(self.homeDir+'/.jgames'):
				os.mkdir(self.homeDir+'/.jgames')
			self.config=ConfigObj(self.homeDir+'/.jgames/config',encoding='UTF8')
			for i in configs:
				self.config[i]=""
			self.config.write()
		rewrite=False
		for i in configs:
			try:
				self.config[i]
			except:
				self.config[i]=""
				rewrite=True
		if rewrite==True:
			self.config.write()

	def getHomeDir(self):
		# gets homedir on win32 or linux
		if sys.platform != 'win32' :
			return os.path.expanduser( '~' )
		def valid(path):
			if path and os.path.isdir(path):
				return True
			return False
		def env(name):
			return os.environ.get( name, '' )
		homeDir = env( 'USERPROFILE' )
		if not valid(homeDir):
			homeDir = env( 'HOME' )
			if not valid(homeDir):
				homeDir = '%s%s' % (env('HOMEDRIVE'),env('HOMEPATH'))
				if not valid(homeDir):
					homeDir = env( 'SYSTEMDRIVE' )
					if homeDir and (not homeDir.endswith('\\')):
						homeDir += '\\'
					if not valid(homeDir):
						homeDir = 'C:\\'
		return homeDir

	def hideOffline(self,bool):
		self.offline=not bool
		for group,v in self.groups.iteritems():
			for k,user in self.groups[group]["users"].iteritems():
				if int(user.text(1)[0])==9:
					self.ui.roster.setItemHidden(user, not bool)

	def now(self):
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def jabberCommandHandler(self,e):
		if e[0] == "con_ready":
			MainWindow.show()
			login.done(1)
			jab.setStatus()

		elif e[0] == "groupchat_message":
			jid=str(e[1])
			user=unicode(e[2])
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					if unicode(w.name)==unicode(user):
						message=self.skin["my_message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
					else:
						message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))

					w.chat.textEditWrite(message)
					return

		elif e[0] == "chat_message":
			jid=str(e[1])
			if len(self.ui.roster.getUsers(jid))!=0:
				user=self.ui.roster.getUsers(jid)[0].text(2)
			else:
				user=jid
			message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					w.chat.textEditWrite(message)
					return
			self.chat.show()
			#tab=QtGui.QWidget(self.chat)
			#tab.jid=jid
			#layout=QtGui.QHBoxLayout(tab)
			#tab.chat=chatWidget(self,jid,tab)
			#layout.addWidget(tab.chat)
			#self.chat.ui.chatTab.addTab(tab,str(jid))
			self.chat.addChatTab(jid,unicode(user),message)
		elif e[0] == "subscribe":
			jab.roster.Authorize(str(e[1]))
		elif e[0] == "nick_update":
			jid=str(e[1])
			#print "nick_update",jid
			if self.ui.roster.isUser(jid):
				for user in self.ui.roster.getUsers(jid):
					if str(e[2].getType())!="unavailable":
						if str(e[2].getShow())!="None":
							user.setIcon(0,self.statuses[str(e[2].getShow())])
							user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
						else:
							user.setIcon(0,self.statuses["online"])
							user.setText(1,self.nickSort["online"]+unicode(user.text(2)))
						user.setToolTip(0,'<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
						if unicode(e[2].getStatus())=="None":
							user.setText(0,unicode(self.ui.roster.getUsers(jid)[0].text(2)))
						else:
							text=[word for word in unicode(e[2].getStatus()).split('\n') if word != ''][0]
							user.setText(0,unicode(self.ui.roster.getUsers(jid)[0].text(2))+"\n"+text)
						self.ui.roster.setItemHidden(user,False)
				for k,v in MainWindow.groups.iteritems():
					if k!="Unknown":
						online,offline,count=self.ui.roster.getStats(unicode(k))
						self.groups[k]["item"].setText(0,unicode(self.groups[k]["item"].text(2))+" ("+str(online)+"/"+str(count)+")")
				self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			elif jid in self.groupchat:
				nick=unicode(e[3])
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if str(w.jid)==jid:
						user=QtGui.QListWidgetItem(unicode(nick))
						if str(e[2].getShow())!="None":
							user.setIcon(self.statuses[str(e[2].getShow())])
							#user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
						else:
							user.setIcon(self.statuses["online"])
							#user.setText(1,self.nickSort["online"]+unicode(user.text(2)))
						#user.setToolTip('<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
						w.chat.ui.listWidget.addItem(user)
						w.chat.ui.listWidget.sortItems()
						return
		elif e[0] == "roster_update":
			print "roster update"
			items=e[1].getItems()
			#self.groups={}
			for jid in items:
				groups=e[1].getGroups(jid)
				print groups
				if groups==None or groups==[]:
					groups=[]
					name=e[1].getName(jid)
					self.groups["Unknown"]["users"][str(jid)]=self.ui.roster.addUser(jid,name,None,self.offline,self.statuses["offline"])
				for group in groups:
					if self.groups.has_key(group)==False:
						self.groups[group]={"item":self.ui.roster.addGroup(group),"users":{}}
					name=e[1].getName(jid)
					self.groups[group]["users"][str(jid)]=self.ui.roster.addUser(jid,name,self.groups[group]["item"],self.offline,self.statuses["offline"])
						
			self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
				

	def tick(self):
		# new chat lines handler
		lines = None#jab.newChatLines(self.actualRoom)
		if lines!=None and len(lines)!=0:
			for line in lines:
				self.widget.textEditWrite(line)

		# we must use try as forced reading of empty queue raises an error
		try:
			e = jab.inc.get(timeout = 0)
		except:
			e=None
		if e!=None:
			self.jabberCommandHandler(e)
		try:
			e = jab.err.get(timeout = 0)
			self.jabberErrorHandler(e)
		except:
			pass

	def jabberErrorHandler(self,error):
		if error == "con":
			self.jabberError(self.tr("Totaly unable to connect to server."))
			login.ui.connect.setEnabled(True)
		elif error == "auth":
			self.jabberError(self.tr("Don't try anything hax0r here, and type your username and password right!"))
			login.ui.connect.setEnabled(True)

	def jabberError(self,error):
		QtGui.QMessageBox.warning(self,"Jabber Error",unicode(error),0,1)

class statusWindow(QtGui.QDialog):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_status()
		self.ui.setupUi(self)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.timeout)
		app.connect(self.ui.status, QtCore.SIGNAL("cursorPositionChanged ()"),self.timerStop)
		app.connect(self.ui.status, QtCore.SIGNAL("textChanged ()"),self.timerStop)
		
		self.timer.start(1000)
		self.i=4
		self.data=data
		self.timeout()
	
	def timerStop(self):
		self.timer.stop()
		self.ui.time.setText("")
	
	def timeout(self):
		if self.i!=0:
			self.ui.time.setText(self.tr("Window will be closed in ")+unicode(self.i)+self.tr(" seconds."))
			self.i-=1
		else:
			self.accept()
	def accept(self):
		jab.setStatus(self.data,unicode(self.ui.status.toPlainText ()))
		self.done(1)


app = QtGui.QApplication(sys.argv)
jab = Jabber()
translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()

login=loginWindow(MainWindow,jab,MainWindow)
ref=login.show()
sys.exit(app.exec_())
