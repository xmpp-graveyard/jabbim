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
#from preferences import *
from roster import *
from status import *
from chat import *
from chatwidget import *
from addcontact import *
#from game import *

#import games

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=Ui_mainWindow()
		self.ui.setupUi(self)
		self.loadRoster()
		# Signals
		app.connect(self.ui.roster, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.contactClicked)
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.addContact, QtCore.SIGNAL("clicked(bool)"),self.addContact)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tick)
		self.timer.start(50)
		self.homeDir=self.getHomeDir()
		self.loadConfig()
		self.loadSkin()
		self.loadStatus()
		self.users={}
		self.groups={}
		self.groups["Unknown"]={"item":self.ui.roster,"users":{}}
		self.ui.roster.hideColumn (1)
		self.chat=chatWindow(parent=self)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)

	def loadSkin(self):
		# loads config and repairs config file
		self.skin=ConfigObj('skins/default.conf',encoding='UTF8')

	def addContact(self,bool):
		contact=addContactWindow()
		contact.exec_()

	def loadRoster(self):
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=rosterWidget(self.ui.rosterWidget)
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

	def contactClicked(self,item,column):
		if self.groups.has_key(unicode(item.text(0))):
			return
		data=item.data(32,0)
		data=str(data.toString())
		for i in range(self.chat.ui.chatTab.count()):
			w=self.chat.ui.chatTab.widget(i)
			try:
				if w.jid==data:
					self.chat.show()
					return
			except:
				pass
		self.chat.show()
		tab=QtGui.QWidget(self.chat)
		tab.jid=data
		layout=QtGui.QHBoxLayout(tab)
		tab.chat=chatWidget(self,data,tab)
		layout.addWidget(tab.chat)
		self.chat.ui.chatTab.addTab(tab,unicode(item.text(0)))

	def statusChanged(self,action):
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.statuses[str(data)])
		setstatus=statusWindow(data)
		setstatus.exec_()

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


	def isUser(self,jid):
		for k,v in self.groups.iteritems():
			if self.groups[k]["users"].has_key(str(jid)):
				return True
		return False

	def getUsers(self,jid):
		users=[]
		for k,v in self.groups.iteritems():
			if self.groups[k]["users"].has_key(jid):
				users.append(self.groups[k]["users"][str(jid)])
		return users

	def jabberCommandHandler(self,e):
		if e[0] == "con_ready":
			MainWindow.show()
			login.done(1)
			jab.setStatus()
		elif e[0] == "chat_message":
			jid=str(e[1])
			if len(self.ui.roster.getUsers(jid))!=0:
				user=self.ui.roster.getUsers(jid)[0].text(0)
			else:
				user=jid
			message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					w.chat.textEditWrite(message)
					return
			self.chat.show()
			tab=QtGui.QWidget(self.chat)
			tab.jid=jid
			layout=QtGui.QHBoxLayout(tab)
			tab.chat=chatWidget(self,jid,tab)
			layout.addWidget(tab.chat)
			self.chat.ui.chatTab.addTab(tab,str(jid))
			tab.chat.textEditWrite(message)
		elif e[0] == "subscribe":
			jab.roster.Authorize(str(e[1]))
		elif e[0] == "nick_update":
			jid=str(e[1])
			#print "nick_update",jid
			if self.isUser(jid):
				for user in self.getUsers(jid):
					if str(e[2].getType())!="unavailable":
						if str(e[2].getShow())!="None":
							user.setIcon(0,self.statuses[str(e[2].getShow())])
							user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(0)))
						else:
							user.setIcon(0,self.statuses["online"])
							user.setText(1,self.nickSort["online"]+unicode(user.text(0)))
						self.ui.roster.setItemHidden(user,False)
				self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
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

class chatWidget(QtGui.QWidget):
	def __init__(self,main,jid,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_chatwidget()
		self.ui.setupUi(self)
		self.main=main
		app.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		app.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		app.connect(self.ui.smileys, QtCore.SIGNAL("clicked (bool)"),self.smileysClicked)
		#short=QtGui.QShortcut("tab",self.ui.line)
		#app.connect(short, QtCore.SIGNAL("activated ()"),self.tabPressed)
		self.loadSmileys()
		self.jid=jid
		self.name_id=-1 # for tabPressed


	def loadSmileys(self):
		# loads smileys.conf and makes buttons
		self.smileys=ConfigObj("smileys.conf",encoding='UTF8')
		self.s=QtGui.QFrame(self)
		self.s.hide()
		layout=QtGui.QGridLayout(self.s)
		layout.setMargin(0)
		layout.setSpacing(0)
		added=[]
		x=0
		y=0
		for k,v in self.smileys.iteritems():
			if added.count(v)==0:
				added.append(v)
				button=QtGui.QToolButton(self)
				action=QtGui.QAction(QtGui.QIcon("images/smileys/"+v),"",self.s)
				action.setData(QtCore.QVariant(k))
				button.setDefaultAction(action)
				button.setToolTip(str(k))
				app.connect(button, QtCore.SIGNAL("triggered ( QAction *)"),self.addEmoticon)
				layout.addWidget(button,x,y)
				y+=1
				if y==5:
					y=0
					x+=1
	
	def smileysClicked(self,bool):
		self.s.setGeometry ( self.ui.smileys.x()-60, self.ui.smileys.y()-120, 120, 120)
		self.s.setShown(bool)
	
	def textEditWrite(self,text):
		cur=self.ui.textEdit.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.textEdit.setTextCursor(cur)
		# emoticons
		for k,v in self.smileys.iteritems():
			text=text.replace(k,'<img src="images/smileys/'+v+'"/>')
		self.ui.textEdit.insertHtml(text)
		cur=self.ui.textEdit.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.textEdit.setTextCursor(cur)
	
	def addEmoticon(self,action):
		# add emoticon to the self.ui.line
		data=action.data()
		data=data.toString()
		self.ui.line.insert(data)
		self.ui.smileys.setChecked(False)
		self.s.hide()
	
	def sendButtonClicked(self):
		# sends message
		if len(unicode(self.ui.line.text()))!=0:
			jab.sendToConf(str(self.jid),unicode(self.ui.line.text()))
			message=MainWindow.skin["my_message"].replace("[time]",MainWindow.now()).replace("[user]",jab.user).replace("[message]",unicode(self.ui.line.text()))
			self.textEditWrite(message)
			self.ui.line.clear()
			MainWindow.loadSkin()

	def tabPressed(self):
		# nick completion
		text=unicode(self.ui.line.text()).lower()
		if len(text)==0:
			return
		text=text[0]
		repeat=False
		for i in range(self.ui.listWidget.count()):
			if unicode(self.ui.listWidget.item(i).text()).lower()[:len(text)]==text and i>self.name_id:
				self.ui.line.setText(self.ui.listWidget.item(i).text()+": ")
				self.name_id=i
				return
			if unicode(self.ui.listWidget.item(i).text()).lower()[:len(text)]==text:
				repeat=True
		self.name_id=-1
		if repeat==True:
			self.tabPressed()


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

class chatWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=Ui_chat()
		self.ui.setupUi(self)
		self.ui.tabCloseButton=QtGui.QPushButton(QtGui.QIcon("images/icons/close.png"),"",self.ui.chatTab)
		self.ui.chatTab.setCornerWidget(self.ui.tabCloseButton)
		app.connect(self.ui.tabCloseButton, QtCore.SIGNAL("clicked ()"),self.removeTab)
		self.ui.chatTab.removeTab(0)

	def closeEvent(self,e):
		for index in range(self.ui.chatTab.count()):
			self.ui.chatTab.removeTab(0)

	def removeTab(self):
		self.ui.chatTab.removeTab(self.ui.chatTab.currentIndex())
		if int(self.ui.chatTab.count())==0:
			self.close()

class rosterWidget(QtGui.QTreeWidget):
	def __init__(self,parent=None):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.setAlternatingRowColors(True)
		self.setIconSize(QtCore.QSize(16,16))
		self.setRootIsDecorated(False)
		self.setObjectName("roster")
		self.setDragEnabled(True)
		#self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		self.headerItem().setText(0,QtGui.QApplication.translate("roster", "Roster", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(1,QtGui.QApplication.translate("roster", "id", None, QtGui.QApplication.UnicodeUTF8))
		app.connect(self, QtCore.SIGNAL("itemChanged ( QTreeWidgetItem *, int )"),self.itemChange)
		self.edit=0
		self.setAcceptDrops(True)
		self.dragStartPosition=None
		self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed)
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

	def isUser(self,jid):
		for k,v in MainWindow.groups.iteritems():
			if MainWindow.groups[k]["users"].has_key(str(jid)):
				return True
		return False

	def isGroupItem(self,item):
		for k,v in MainWindow.groups.iteritems():
			if MainWindow.groups[k]["item"]==item:
				return True
		return False

	def getUsers(self,jid):
		users=[]
		for k,v in MainWindow.groups.iteritems():
			if MainWindow.groups[k]["users"].has_key(jid):
				users.append(MainWindow.groups[k]["users"][str(jid)])
		return users

	def delUser(self,jid,user):
		parent=user.parent()
		if parent==None:
			index=self.indexOfTopLevelItem(user)
			self.takeTopLevelItem(index)
			del MainWindow.groups["Unknown"]["users"][str(jid)]
		else:
			index=parent.indexOfChild(user)
			parent.takeChild(index)
			if int(parent.childCount())==0:
				self.takeTopLevelItem(self.indexOfTopLevelItem(parent))
			del MainWindow.groups[unicode(parent.text(0))]["users"][str(jid)]
			if len(MainWindow.groups[unicode(parent.text(0))]["users"])==0:
				del MainWindow.groups[unicode(parent.text(0))]

	def getGroups(self,jid):
		groups=[]
		for k,v in MainWindow.groups.iteritems():
			if MainWindow.groups[k]["users"].has_key(jid):
				groups.append(unicode(k))
		return groups

	def addGroup(self,name):
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"0"+unicode(name).lower())
		item.setBackgroundColor(0,QtGui.QColor(102,102,102))
		#self.groups[g].setFlags(self.users[str(item)].flags()|QtCore.Qt.ItemIsDragEnabled)
		item.setTextColor(0,QtGui.QColor(255,255,255))
		#self.groups[g].setIcon(0,QtGui.QIcon("images/status/closed.png"))
		return item

	def addUser(self,jid,name,group,offline,icon):
		if group==None:
			item=QtGui.QTreeWidgetItem(self)
		else:
			item=QtGui.QTreeWidgetItem(group)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setData(32,0,QtCore.QVariant(jid))
		item.setIcon(0,icon)
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		self.setItemHidden(item, offline)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		return item

	def itemChange(self,item,column):
		if item==self.currentItem():
			jid=item.data(32,0)
			jid=str(jid.toString())
			parent=item.parent()
			if parent==None:
				groups=[]
			else:
				groups=[unicode(parent.text(0))]
			jab.roster.setItem(jid,unicode(item.text(0)),groups)

	#def itemEdit(self):
		#self.edit=self.currentItem()
		#self.editItem(self.currentItem(),0)

	def buildContactMenu(self,jid,group):
		contactMenu=QtGui.QMenu(self)
		contactMenu.addAction(self.tr("Chat"))
		contactMenu.addSeparator()

		if group!=None:
			action=contactMenu.addAction(self.tr("Delete from group"))
			action.setData(QtCore.QVariant([unicode(jid),u"-"+group.text(0)]))
			action.setObjectName("check_group")
		elif len(self.getGroups(str(jid)))>1:
			action=contactMenu.addAction(self.tr("Delete from group"))
			action.setData(QtCore.QVariant([unicode(jid),u"-Unknown"]))
			action.setObjectName("check_group")
			
		action=contactMenu.addAction(self.tr("Delete from roster"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("delete_action")
		contactMenu.addSeparator()
		
		group=contactMenu.addMenu (self.tr("Groups"))
		
		#action=group.addAction(self.tr("None"))
		#action.setObjectName("no_group")
		#contactMenu.addSeparator()

		action=group.addAction(self.tr("New Group"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("new_group")
		group.addSeparator()

		g=self.getGroups(str(jid))
		for k,v in MainWindow.groups.iteritems():
			action=group.addAction(unicode(k))
			action.setObjectName("check_group")
			action.setCheckable(True)
			if k in g:
				action.setChecked(True)
				action.setData(QtCore.QVariant([unicode(jid),u"-"+unicode(k)]))
			else:
				action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))


		
		
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu

	#def dropEvent(self,event):
		#print "test"
		#event.accept()


	def mimeTypes(self):
		return QtCore.QStringList("text/plain")

	def startDrag(self,actions):
		item=self.currentItem()
		data=item.data(32,0)
		data=str(data.toString())
		self.drag=QtGui.QDrag(self)
		mimeData=QtCore.QMimeData()
		mimeData.setText(data)
		self.drag.setMimeData(mimeData)
		self.dropAction = self.drag.start(QtCore.Qt.CopyAction)

	def dropMimeData(self,parent, index, data, action ):
		jid=str(data.text())
		print parent,data.text()
		if self.isGroupItem(parent):
			name=unicode(self.getUsers(jid)[0].text(0))
			self.changeGroup(jid,name,"+",unicode(parent.text(0)))
			return True
		else:
			return False

	def changeGroup(self,jid,name,action,group):
		if action=="+":
			if not MainWindow.groups[group]["users"].has_key(str(jid)):
				item=self.getUsers(jid)[0].clone()
				if group!="Unknown":
					MainWindow.groups[group]["item"].addChild(item)
				else:
					MainWindow.groups[group]["item"].addTopLevelItem(item)
				MainWindow.groups[group]["users"][str(jid)]=item
				jab.roster.setItem(jid,name,self.getGroups(jid)+[unicode(group)])
		else:
			user=MainWindow.groups[group]["users"][str(jid)]
			self.delUser(jid,user)
			groups=self.getGroups(jid)
			print groups
			jab.roster.setItem(jid,name,groups)
		self.sortItems (1,QtCore.Qt.AscendingOrder)

	def contactMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="delete_action":
			jid=action.data()
			jid=str(jid.toString())
			print "roster_delete_action",jid
			for user in self.getUsers(jid):
				self.delUser(jid,user)
			jab.roster.delItem(jid)
		elif cmd=="new_group":
			jid=action.data()
			jid=str(jid.toString())
			name=unicode(self.getUsers(jid)[0].text(0))
			print "roster_new_group_action",jid,name
			group,b=QtGui.QInputDialog.getText(self,self.tr("New group"),"Add user to new group", QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			if b==True:
				MainWindow.groups[group]={"item":self.addGroup(group),"users":{}}
				item=self.getUsers(jid)[0].clone()
				MainWindow.groups[group]["item"].addChild(item)
				MainWindow.groups[group]["users"][str(jid)]=item
				
				self.sortItems (1,QtCore.Qt.AscendingOrder)
				jab.roster.setItem(jid,name,self.getGroups(jid)+[unicode(group)])
		elif cmd=="check_group":
			items=action.data()
			items=items.toList()
			jid=str(items[0].toString())
			name=unicode(self.getUsers(jid)[0].text(0))
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]
			print "roster_change_group_action",jid,group
			self.changeGroup(jid,name,action,group)

	def contextMenuEvent (self,event):
		item=self.itemFromIndex(self.indexAt(QtCore.QPoint(event.x(),event.y())))
		group=item.parent()
		data=item.data(32,0)
		data=data.toString()
		if self.isUser(data):
			contactMenu=self.buildContactMenu(str(data),group)
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()
			

			
	#def mouseReleaseEvent(self,event):
		#if event.button()==QtCore.Qt.RightButton:
			#item=self.itemFromIndex(self.indexAt(QtCore.QPoint(event.x(),event.y())))
			#group=item.parent()
			#data=item.data(32,0)
			#data=data.toString()
			#if self.isUser(data):
				#contactMenu=self.buildContactMenu(str(data),group)
				#contactMenu.show()
				#contactMenu.move(event.globalX(),event.globalY())


class loginWindow(QtGui.QDialog):
	def __init__(self,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_login()
		self.ui.setupUi(self)
		self.ui.password.setText(MainWindow.config['passwd'])
		self.ui.jid.setText(MainWindow.config['jid'])
		
		if MainWindow.config['savePasswd']=="True":
			self.ui.savePassword.setChecked(True)

	def accept(self):
		jid=unicode(self.ui.jid.text())
		password=unicode(self.ui.password.text())
		if len(jid)!=0 and len(jid.split("@"))==2 and len(unicode(self.ui.password.text()))!=0:
			if jid!=MainWindow.config['jid'] or (password!=MainWindow.config['passwd'] and MainWindow.config['savePasswd']=="True") or MainWindow.config['savePasswd']!=str(self.ui.savePassword.isChecked()):
				ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save actual login information?"),3,4)
				if ret==3:
					MainWindow.config['savePasswd']=self.ui.savePassword.isChecked()
					if self.ui.savePassword.isChecked()==True:
						MainWindow.config['passwd']=password
					else:
						MainWindow.config['passwd']=""
					MainWindow.config['jid']=jid
					MainWindow.config.write()
			jab.user=jid.split("@")[0]
			jab.server=jid.split("@")[1]
			jab.password=unicode(password)
			jab.connect()
			self.ui.connect.setEnabled(False)

	def reject(self):
		MainWindow.close()
		self.close()

class addContactWindow(QtGui.QDialog):
	def __init__(self,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_addContact()
		self.ui.setupUi(self)
		for k,v in MainWindow.groups.iteritems():
			self.ui.group.addItem(unicode(k))

	def accept(self):
		jid=unicode(self.ui.jid.text())
		nickname=unicode(self.ui.nickname.text())
		group=unicode(self.ui.group.currentText())
		print "adding",jid,nickname,group
		if len(group)!=0:
			if MainWindow.groups.has_key(group):
				MainWindow.groups[group]["users"][str(jid)]=MainWindow.ui.roster.addUser(jid,nickname,MainWindow.groups[group]["item"],MainWindow.offline,MainWindow.statuses["offline"])
			else:
				MainWindow.groups[group]={"item":MainWindow.ui.roster.addGroup(group),"users":{}}
				MainWindow.groups[group]["users"][str(jid)]=MainWindow.ui.roster.addUser(jid,nickname,MainWindow.groups[group]["item"],MainWindow.offline,MainWindow.statuses["offline"])
		else:
			MainWindow.groups["Unknown"]["users"][str(jid)]=MainWindow.ui.roster.addUser(jid,nickname,None,MainWindow.offline,MainWindow.statuses["offline"])
		jab.roster.setItem(jid,nickname,[group])
		jab.roster.Subscribe(jid)
		self.done(1)

	def reject(self):
		self.close()


app = QtGui.QApplication(sys.argv)

translator=QtCore.QTranslator()
translator.load("locales/pyjim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)
MainWindow = mainWindow()
jab = Jabber()
login=loginWindow(MainWindow)
ref=login.show()
sys.exit(app.exec_())