"""
Jabbim.
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
from gameslist import *
from addcontact import *
from grouped_events import *
from discovery_register import *
from vcard import *
from discovery_ui import *
#from palette import *
from dataforms import *
import notification

import games


class discoveryWindow(QtGui.QDialog):
	def __init__(self,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_discovery()
		self.ui.setupUi(self)
		QtCore.QObject.connect(self.ui.services, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.clicked)
		QtCore.QObject.connect(self.ui.services, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.menu)
		self.ui.services.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.items={}
		self.nodes={}

	def menuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="register":
			jid=action.data()
			jid=str(jid.toString())
			jab.getRegInfo(jid)
		elif cmd=="add":
			data=action.data()
			data=data.toList()
			jid=str(data[0].toString())
			name=unicode(data[1].toString())
			contact=addContactWindow(MainWindow,jab,self,jid,name)
			contact.exec_()

	def menu(self,pos):
		item=self.ui.services.itemFromIndex(self.ui.services.indexAt(pos))
		jid=str(item.text(1))
		menu=QtGui.QMenu(self.ui.services)
		if item.parent()==None:
			for feature in item.features:
				if feature=="jabber:iq:register":
					action=menu.addAction(self.tr("Register / Unregister"))
					action.setData(QtCore.QVariant(jid))
					action.setObjectName("register")
		else:
			action=menu.addAction(self.tr("Add to roster"))
			action.setData(QtCore.QVariant([unicode(jid),unicode(item.text(0))]))
			action.setObjectName("add")

		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.menuTriggered)
		menu.move(self.ui.services.mapToGlobal(pos))
		menu.show()


	def addItem(self,jid,name="",parent=None,node="",features=[]):
		if parent==None:
			parent=self.ui.services
		if name=="":
			name=jid
		if node=="":
			self.items[jid]=QtGui.QTreeWidgetItem(parent)
			self.items[jid].setText(1,jid)
			self.items[jid].setText(0,name)
			self.items[jid].node=False
			self.items[jid].features=[]
		else:
			if not self.nodes.has_key(jid+node):
				self.nodes[jid+node]=QtGui.QTreeWidgetItem(parent)
			self.nodes[jid+node].setText(0,name)
			self.nodes[jid+node].setText(1,jid)
			self.nodes[jid+node].node=node
			self.nodes[jid+node].features=[]
		self.ui.services.sortItems(0,QtCore.Qt.AscendingOrder)

	def clicked(self,item,i):
		if item.parent()==None and int(item.childCount())==0:
			jab.discoveryItems(unicode(item.text(1)))
		if item.node!=False and int(item.childCount())==0:
			jab.discoveryItems(unicode(item.text(1)),node=item.node)


class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		jab.main=self
		self.ui=Ui_mainWindow()
		self.ui.setupUi(self)
		self.homeDir=self.getHomeDir() # get home dir
		self.loadConfig() # load config files
		self.loadPaletteSkin() # load palette file
		self.loadRoster() # load roster widget
		# Signals
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		#app.connect(self.ui.addContact, QtCore.SIGNAL("clicked(bool)"),self.addContact)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		app.connect(self.ui.actionAdd_contact, QtCore.SIGNAL("triggered ( bool )"),self.addContact)
		app.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered ( bool )"),self.trayQuit)
		app.connect(self.ui.actionEvents, QtCore.SIGNAL("triggered ( bool )"),self.actionEvents)
		app.connect(self.ui.actionService_discovery, QtCore.SIGNAL("triggered ( bool )"),self.discovery)
		app.connect(self.ui.addContact, QtCore.SIGNAL("clicked ()"),self.addContactMainWindow)
		app.connect(self.ui.getGroupchatList, QtCore.SIGNAL("clicked ()"),self.getGroupchatList)
		app.connect(self.ui.manageBookmarks, QtCore.SIGNAL("clicked ()"),self.manageBookmarks)
		QtCore.QObject.connect(self.ui.groupchat, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.groupchatClicked)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.bookmarksClicked)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.bookmarksContextMenu)
		QtCore.QObject.connect(self.ui.groupchat, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.groupchatContextMenu)
		# Set menu policy for QTreeWidgets
		self.ui.groupchat.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.bookmarks.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		# set tab text for main tab widget
		self.ui.tabWidget.setTabText(1,"")
		self.ui.tabWidget.setTabText(2,"")
		self.ui.tabWidget.setTabText(3,"")

		self.loadSkin() # load chat skin
		self.loadStatus() # load status icons
		self.bookmarks={} # bookmarks storage
		self.loadGroupchat() # load groupchat bookmarks
		self.groupchat={} # opened groupchats storage
		self.discoInfo={} # transport informations storage
		self.groups={} # roster items storage
		# add default group in roster
		self.groups["Unknown"]={"item":self.ui.roster.addGroup(self.tr("Unknown")),"users":{}}

		self.chat=chatWindow(self,self,jab) # make chat window
		self.events=groupedEventWindow(None,self,jab) # make grouped events menu
		self.disco=discoveryWindow(self) # discovery window

		# Tray icon and tray menu
		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
		menu=QtGui.QMenu(self)
		menu.addMenu(self.statusMenu)
		menu.addSeparator()
		menu.addAction(self.tr("Close"),self.trayQuit)
		app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.setContextMenu(menu)
		self.tray.show()

		# jGames mess :-)
		self.games=[]
		self.gameslist=gamesListWindow(self,self,jab)
		self.preparedGames=[]
		self.jgamesLoadPlugins()
		self.gameServer="@games.jabbim.cz"

		# main window design
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		self.ui.groupchat.header().hide()
		self.ui.groupchat.hideColumn(1)
		self.ui.bookmarks.header().hide()
		self.ui.bookmarks.hideColumn(1)

		# timer config
		self.timer=QtCore.QTimer()
		#app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tick)
		#self.timer.start(20)

		#self.chat.addHeadlineTab()

	def manageBookmarks(self):
		# open "manage bookmarks" window
		win=preferencesWindow(self,self,1,jab=jab)
		win.show()

	def bookmarksContextMenu(self,pos):
		# make groupchat bookmarks menu
		item=self.ui.bookmarks.itemFromIndex(self.ui.bookmarks.indexAt(pos)) # get selected item
		jid=str(item.text(1)) # get item jid
		menu=QtGui.QMenu(self.ui.bookmarks) # make menu
		if item.parent()==None:
			# Join bookmarked groupchat
			action=menu.addAction(self.tr("Join"))
			action.setData(item.data(0,32))
			action.setObjectName("join_bookmark")
		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.groupchatContextMenuTriggered)
		# set menu position and show
		menu.move(self.ui.bookmarks.mapToGlobal(pos))
		menu.show()

	def groupchatContextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="join":
			# join groupchat from Groupchats list
			jid=action.data() # get jid
			jid=str(jid.toString())
			room=jid.split("@")[0] # get room
			server=jid.split("@")[1] # get server
			# show join groupchat dialog
			newchat=joinGroupChatWindow(self,jab,room=room,server=server)
			ret=newchat.exec_()
		elif cmd=="join_bookmark":
			# join bookmarked groupchat
			data=action.data()
			lst=data.toList()
			jid=unicode(lst[0].toString()) # get jid
			nickname=unicode(lst[1].toString()) # get nickname
			# send jabber command
			jab.getIntoRoom(jid,nickname)

	def groupchatContextMenu(self,pos):
		# make groupchat context menu
		item=self.ui.groupchat.itemFromIndex(self.ui.groupchat.indexAt(pos)) # get item
		jid=str(item.text(1)) # get jid
		menu=QtGui.QMenu(self.ui.groupchat) # make menu
		if item.parent()==None:
			# Join groupchat
			action=menu.addAction(self.tr("Join"))
			action.setData(QtCore.QVariant(jid))
			action.setObjectName("join")
		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.groupchatContextMenuTriggered)
		# set menu position and show
		menu.move(self.ui.groupchat.mapToGlobal(pos))
		menu.show()

	def getGroupchatList(self):
		# get groupchat list
		jid=""
		# get groupchat server from discoInfo
		for k,v in self.discoInfo.iteritems():
			if v=="conf":
				jid=k
		# if we had some server, we can get items
		if jid!="":
			self.ui.groupchat.clear()
			jab.discoveryItems(jid)

	def groupchatClicked(self,item,i):
		# get users in groupchat
		if int(item.childCount())!=0:
			# delete all users in groupchat
			for i in range(item.childCount()):
				item.takeChild(0)
		# set item expanded
		self.ui.groupchat.setItemExpanded(item,True)
		# send jabber command
		jab.discoveryItems(unicode(item.text(1)),back="muc_items")

	def bookmarksClicked(self,item,i):
		# get users in bookmarked groupchat
		if int(item.childCount())!=0:
			# delete all users in groupchat
			for i in range(item.childCount()):
				item.takeChild(0)
		# set item expanded
		self.ui.bookmarks.setItemExpanded(item,True)
		# send jabber command
		jab.discoveryItems(unicode(item.text(1)),back="bookmarks_items")

	def jgamesClicked(self,action):
		data=action.data()
		lst=data.toList()
		cmd=unicode(lst[0].toString())
		if cmd=="game_list":
			self.gameslist.show()
			self.gameslist.refreshList(int(lst[1].toString()))
		else:
			gameid=int(cmd)
			for plugin in self.plugins:
				if plugin.config.id==gameid:
					#self.preparedGames.append([plugin.prepareGameWindow(name,self,jab),plugin.config.id])
					#self.preparedGames[-1][0].show()
					#print self.preparedGames[-1]
					muc=str("%02d%f%d"%(plugin.config.id,time.time(),random.randint(1000,9999))).replace('.','')
					#self.chat.addGameChatTab(muc+self.gameServer,muc)
					#self.groupchat[muc+self.gameServer]=[jab.user,[]]
					self.groupchat[room]=[nickname,[]]
					jab.getIntoRoom(muc+self.gameServer,jab.user)
					#jab.getGroupchatConfig(muc+self.gameServer)
					#self.preparedGames.append([plugin.prepareGameWindow(name,self,jab,self.main.widgets[str(muc)].ui.gameFrame),plugin.config.id])
					break

	def jgamesLoadPlugins(self):
		# loads plugins
		temp=dir(games)
		self.plugins=[]
		for i in temp:
			if not i.startswith("__"):
				self.plugins.append(getattr(games,i))
				print "Loading plugin",self.plugins[-1]
		for plugin in self.plugins:
			menu=QtGui.QMenu(unicode(plugin.config.name),self.ui.menuJGames)
			action=menu.addAction(self.tr("New game"))
			action.setData(QtCore.QVariant([unicode(plugin.config.id)]))
			action=menu.addAction(self.tr("Game list"))
			action.setData(QtCore.QVariant(["game_list",unicode(plugin.config.id)]))
			self.ui.menuJGames.addMenu(menu)
			app.connect(menu, QtCore.SIGNAL("triggered ( QAction *)"),self.jgamesClicked)
#			self.addGame(plugin.config.icon,plugin.config.name,plugin.config.id)

	def actionEvents(self,bool=None):
		# show grouped events
		self.events.show()

	def discovery(self):
		# show discovery window
		self.disco.show()
		self.disco.ui.services.clear()
		self.disco.nodes={}
		self.disco.items={}
		jab.discoveryItems()

	def trayQuit(self):
		# turn off jabbim
		self.tray.hide()
		self.timer.stop()
		app.closeAllWindows()
		jab.disconnect()
		sys.exit(0)

	def trayActivated(self,reason):
		# show or hide main window
		if reason==QtGui.QSystemTrayIcon.Trigger:
			if self.isHidden():
				self.show()
			else:
				self.hide()

	def preferencesClicked(self,bool):
		# shows preferences
		w=preferencesWindow(self,self,jab=jab)
		w.show()

	def loadPaletteSkin(self):
		# loads config and repairs config file
		self.palette=ConfigObj("palettes/"+self.config["palette"],encoding='UTF8')

	def loadSkin(self):
		# loads config and repairs config file
		self.skin=ConfigObj("skins/"+self.config["chat_skin"],encoding='UTF8')

	def addContactMainWindow(self):
		# add contact
		jid=unicode(self.ui.jid.text())
		nickname=unicode(self.ui.nickname.text())
		group=unicode(self.ui.group.currentText())
		print "adding",jid,nickname,group
		addContact(jid,nickname,group,self,jab)
		self.ui.jid.setText("")
		self.ui.nickname.setText("")

	def addContact(self,bool=None):
		# show add contact window
		contact=addContactWindow(self,jab)
		contact.exec_()

	def buildGroupchatMenu(self):
		# build bookmarked groupchat menu and show bookmarked groupchat in Bookmarks tab
		self.ui.bookmarks.clear() # clear tab
		self.groupchatMenu.clear() # clear menu
		# Join new groupchat action
		action=self.groupchatMenu.addAction(self.tr("Join new groupchat"))
		action.setData(QtCore.QVariant(["new"]))
		# separator
		self.groupchatMenu.addSeparator()
		for k,v in self.bookmarks.iteritems():
			# add bookmark to the menu
			action=self.groupchatMenu.addAction(unicode(v["name"]))
			action.setData(QtCore.QVariant([unicode(k),unicode(v["nick"]),unicode(v["password"])]))
			# add bookmark to the bookmarks list
			item=QtGui.QTreeWidgetItem(self.ui.bookmarks)
			item.setText(0,unicode(v["name"]))
			item.setText(1,unicode(k))
			item.setData(0,32,QtCore.QVariant([unicode(k),unicode(v["nick"]),unicode(v["password"])]))
			item.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))
		# separator
		self.groupchatMenu.addSeparator()
		# manage bookmarks
		action=self.groupchatMenu.addAction(self.tr("Manage bookmarks"))
		action.setData(QtCore.QVariant(["manage"]))

	def loadGroupchat(self):
		# load bookmarks menu
		self.groupchatMenu=QtGui.QMenu(self.tr("Group Chat"),self.ui.toolBar)
		self.ui.toolBar.hide() # hide toolbar... we can delete him.. it's in TODO
		self.buildGroupchatMenu()
		self.ui.actionGroup_Chat.setMenu(self.groupchatMenu)
		app.connect(self.groupchatMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.groupchatChanged)

	def loadRoster(self):
		# load roster widget
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=rosterWidget(self.ui.rosterWidget,self,jab)
		layout.addWidget(self.ui.roster)

	def loadStatus(self):
		# load status icons and images + make status menu + sorting rules
		self.statusPath="images/xxxxx/status/"
		self.nickSort={"online":"1",
						"available":"1",
						"chat":"2",
						"away":"3",
						"xa":"4",
						"dnd":"5",
						"None":"9",
						"offline":"9"
						}
		self.iconSort={"1":"online",
						"2":"chat",
						"3":"away",
						"4":"xa",
						"5":"dnd",
						"9":"offline"
						}
		self.status={"online":self.tr("Online"),
					"available":self.tr("Online"),
					"chat":self.tr("Chatty"),
					"away":self.tr("Away"),
					"xa":self.tr("Extended away"),
					"dnd":self.tr("DND"),
					"None":self.tr("Online"),
					"offline":self.tr("Offline")
					}
		# 'change status' menu
		self.statusMenu=QtGui.QMenu(self.tr("Status"),self.ui.statusButton)
		action=self.statusMenu.addAction(self.getIcon(status="online",size="16x16"),self.status["online"])
		action.setData(QtCore.QVariant("online"))
		action=self.statusMenu.addAction(self.getIcon(status="chat",size="16x16"),self.status["chat"])
		action.setData(QtCore.QVariant("chat"))
		action=self.statusMenu.addAction(self.getIcon(status="away",size="16x16"),self.status["away"])
		action.setData(QtCore.QVariant("away"))
		action=self.statusMenu.addAction(self.getIcon(status="xa",size="16x16"),self.status["xa"])
		action.setData(QtCore.QVariant("xa"))
		action=self.statusMenu.addAction(self.getIcon(status="dnd",size="16x16"),self.status["dnd"])
		action.setData(QtCore.QVariant("dnd"))
		self.ui.statusButton.setMenu(self.statusMenu)
		app.connect(self.statusMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusChanged)
		self.offline=True

	def groupchatChanged(self,action):
		# Groupchat menu changed
		data=action.data()
		lst=data.toList()
		cmd=unicode(lst[0].toString()) # get command
		if cmd=="new":
			# join new groupchat
			newchat=joinGroupChatWindow(self,jab)
			ret=newchat.exec_()
		elif cmd=="manage":
			# manage groupchats
			win=preferencesWindow(self,self,1,jab=jab)
			win.show()
		else:
			# format : [unicode(k),unicode(v["nick"]),unicode(v["password"])]
			# get into bookmarked room
			room=unicode(cmd)
			nickname=unicode(lst[1].toString())
			self.groupchat[room]=[nickname,[]]
			jab.getIntoRoom(room,nickname)

	def statusChanged(self,action):
		# status changed
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.getIcon(status=data,size="16x16"))
		setstatus=statusWindow(data)
		setstatus.exec_()

	def loadConfig(self):
		# loads config and repairs config file
		configs={"jid":"",
				"passwd":"",
				"savePasswd":"",
				"chat_skin":"default.conf",
				"tray_message_view_connect":"logged_in",
				"tray_message_view_disconnect":"all",
				"proxy_type":"none",
				"proxy_server":"",
				"proxy_port":"",
				"proxy_user":"",
				"proxy_passwd":"",
				"resource":"Jabbim",
				"palette":"default.conf",
				"tray_message_view_new_message":"not_chat"
				}
		self.config=ConfigObj(self.homeDir+'/.jabbim/config',encoding='UTF8')
		if len(self.config)==0:
			if not os.path.isdir(self.homeDir+'/.jabbim'):
				os.mkdir(self.homeDir+'/.jabbim')
			self.config=ConfigObj(self.homeDir+'/.jabbim/config',encoding='UTF8')
			for k,v in configs.iteritems():
				self.config[k]=v
			self.config.write()
		rewrite=False
		for k,v in configs.iteritems():
			try:
				self.config[k]
			except:
				self.config[k]=v
				rewrite=True
		if rewrite==True:
			self.config.write()
		if not os.path.isdir(self.homeDir+'/.jabbim/avatars'):
				os.mkdir(self.homeDir+'/.jabbim/avatars')

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
		# hide or show offline users
		self.offline=not bool
		for group,v in self.groups.iteritems():
			for k,user in self.groups[group]["users"].iteritems():
				# if user is offline
				if int(user["item"].text(1)[0])==9:
					self.ui.roster.setItemHidden(user["item"], not bool)
			self.ui.roster.hidden(not bool)

	def now(self):
		# get time
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def isGroupChat(self,jid):
		# return True, if is 'jid' groupchat
		for k,v in self.groupchat.iteritems():
			if k==jid:
				return True
		return False

	def isGroupChatMember(self,chat,name):
		# return True if is user called 'name' in groupchat with JID 'chat'
		for user in self.groupchat[chat][1]:
			if unicode(user.text(0))==unicode(name):
				return True
		return False

	def getGroupChatMember(self,chat,name):
		# get QTreeWidgetItem of user called 'name' in groupchat with JID 'chat'
		for user in self.groupchat[chat][1]:
			if unicode(user.text(0))==unicode(name):
				return user
		return None

	def getIcon(self,jid=None,typ=None,size="32x32",status=None):
		# return status icon
		path=self.statusPath.replace("xxxxx",size)
		if jid!=None:
			file=path+self.getUserType(jid)+"-"+self.iconSort[self.nickSort[typ]]+".png"
			if os.path.exists(file):
				icon=QtGui.QIcon(file)
			else:
				print "File not exist",file," <-",jid,typ
				print "using",path+"jabber-"+self.iconSort[self.nickSort[typ]]+".png"
				icon=QtGui.QIcon(path+"jabber-"+self.iconSort[self.nickSort[typ]]+".png")
		else:
			if status==None:
				icon=QtGui.QIcon(path+"jabber-online.png")
			else:
				icon=QtGui.QIcon(path+"jabber-"+status+".png")
		return icon

	def getUserType(self,jid):
		# get type of jid (rss,disk,jabber, etc.)
		if len(jid.split("@"))!=1:
			if self.discoInfo.has_key(jid.split("@")[1]):
				typ=self.discoInfo[jid.split("@")[1]]
				if typ=="pep" or typ=="im":
					typ="jabber"
				elif typ=="file":
					typ="disk"
				return typ
		else:
			print jid
		return "jabber"

	def customEvent(self,event):
		if event.typ=="inc":
			self.jabberCommandHandler(event.data)
		elif event.typ=="err":
			self.jabberErrorHandler(event.data)
		else:
			e=event.data
			if e[0]=="muc_items":
				item=e[2]
				jid=e[3]
				name=unicode(item["jid"]).split("/")[1]
				for i in self.ui.groupchat.findItems(jid,QtCore.Qt.MatchExactly,1):
					user=QtGui.QTreeWidgetItem(i)
					user.setText(0,unicode(name))
					user.setText(1,unicode(name))
					user.setIcon(0,self.getIcon(size="16x16"))
			elif e[0]=="bookmarks_items":
				item=e[2]
				jid=e[3]
				name=unicode(item["jid"]).split("/")[1]
				for i in self.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1):
					user=QtGui.QTreeWidgetItem(i)
					user.setText(0,unicode(name))
					user.setText(1,unicode(name))
					user.setIcon(0,self.getIcon(size="16x16"))
			elif e[0]==None:
				typ=e[1]
				if typ=="items":
					item=e[2]
					jid=e[3]
					parentNode=e[4]
					if item.has_key("jid") and jid==jab.server:
						self.disco.addItem(unicode(item["jid"]))
						jab.discoveryInfo(item["jid"])
					if jid!=jab.server:
						name=""
						if item.has_key("name"):
							name=item["name"]
						node=""
						if self.discoInfo.has_key(jid):
							if self.discoInfo[jid]=="conf":
								groupchat=QtGui.QTreeWidgetItem(self.ui.groupchat)
								groupchat.setText(0,unicode(name))
								groupchat.setText(1,unicode(item["jid"]))
								groupchat.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))
								self.ui.groupchat.sortItems(0,QtCore.Qt.AscendingOrder)
						parent=self.disco.items[jid]
						if self.disco.nodes.has_key(jid+str(parentNode)):
							parent=self.disco.nodes[jid+str(parentNode)]
						if item.has_key("node"):
							node=item["node"]
						self.disco.addItem(unicode(item["jid"]),unicode(name),parent,node=node)
				else:
					ident=e[2]
					features=e[3]
					jid=e[4]
					if not self.discoInfo.has_key(jid) and ident[0].has_key("type"):
						if "http://jabber.org/protocol/muc" in features and ident[0]["type"]=="text":
							self.discoInfo[jid]="conf"
							self.ui.getGroupchatList.setEnabled(True)
						elif ident[0]["type"]=="bytestreams" and ident[0]["category"]=="proxy":
							jab.conn.S5B.addProxy(str(jid))
							#jab.conn.S5B.addProxy(str('proxy.jabberfr.org'))
							print "adding proxy",jid
						else:
							self.discoInfo[jid]=ident[0]["type"]
							users=self.ui.roster.getServerUsers(jid)
							for user in users:
								data=user.data(32,0)
								data=str(data.toString())
								#user.setIcon(0,QtGui.QIcon(self.statusPath+self.getUserType(data)+"-"+self.iconSort[unicode(user.text(1))[0]]+".png"))
								user.setIcon(0,self.getIcon(data,self.iconSort[unicode(user.text(1))[0]]))
						
	
					if self.disco.items.has_key(jid):
						for feature in features:
							if not feature in self.disco.items[jid].features:
								self.disco.items[jid].features.append(feature)
						if self.disco.items.has_key(jid):
							self.disco.items[jid].setText(0,ident[0]["name"])


	def jabberCommandHandler(self,e):
		# handler for all commands from jabber.py
		if e[0] == "con_ready":
			# we are connected
			# e=[command]
			MainWindow.show() # show main window
			login.done(1) # close login window
			jab.setStatus(self.groupchat) # set status
			jab.getBookmarks() # get bookmarks

		elif e[0]=="bookmarks":
			# we get bookmarks
			# e=[command,bookmarks_list]
			self.bookmarks=e[1]
			self.buildGroupchatMenu()

		elif e[0]=="group_chat_admin_list_setted":
			# user set muc#admin list in room
			# e=[command,jid,role,affiliation,toDel,items]
			jid=e[1]
			role=e[2]
			affiliation=e[3]
			toDel=e[4]
			items=e[5]
			if role==None:
				role=affiliation
			# find room
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					# adding items
					for item in items:
						if role=="moderator":
							w.chat.chatadmin.ui.moderatorlist.addItem(item)
						elif role=="owner":
							w.chat.chatadmin.ui.ownerlist.addItem(item)
						elif role=="member":
							w.chat.chatadmin.ui.memberlist.addItem(item)
						elif role=="outcast":
							w.chat.chatadmin.ui.banlist.addItem(item)
						elif role=="admin":
							w.chat.chatadmin.ui.adminlist.addItem(item)
					# delete item
					if toDel!=None:
						if role=="moderator":
							w.chat.chatadmin.ui.moderatorlist.takeItem(w.chat.chatadmin.ui.moderatorlist.row(w.chat.chatadmin.ui.moderatorlist.findItems(toDel[0],QtCore.Qt.MatchExactly)[0]))
						elif role=="owner":
							w.chat.chatadmin.ui.ownerlist.takeItem(w.chat.chatadmin.ui.ownerlist.row(w.chat.chatadmin.ui.ownerlist.findItems(toDel[0],QtCore.Qt.MatchExactly)[0]))
						elif role=="member":
							w.chat.chatadmin.ui.memberlist.takeItem(w.chat.chatadmin.ui.memberlist.row(w.chat.chatadmin.ui.memberlist.findItems(toDel[0],QtCore.Qt.MatchExactly)[0]))
						elif role=="outcast":
							w.chat.chatadmin.ui.banlist.takeItem(w.chat.chatadmin.ui.banlist.row(w.chat.chatadmin.ui.banlist.findItems(toDel[0],QtCore.Qt.MatchExactly)[0]))
						elif role=="admin":
							w.chat.chatadmin.ui.adminlist.takeItem(w.chat.chatadmin.ui.adminlist.row(w.chat.chatadmin.ui.adminlist.findItems(toDel[0],QtCore.Qt.MatchExactly)[0]))
					return

		elif e[0]=="group_chat_admin_list":
			items=e[1]
			jid=e[2]
			role=e[3]
			affiliation=e[4]
			if role==None:
				role=affiliation
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					print items
					for item in items:
						if role=="moderator":
							w.chat.chatadmin.ui.moderatorlist.addItem(item)
						elif role=="owner":
							w.chat.chatadmin.ui.ownerlist.addItem(item)
						elif role=="member":
							w.chat.chatadmin.ui.memberlist.addItem(item)
						elif role=="outcast":
							w.chat.chatadmin.ui.banlist.addItem(item)
						elif role=="admin":
							w.chat.chatadmin.ui.adminlist.addItem(item)
					return

		elif e[0]=="room_opened":
			# room is opened => add room tab and getStoreQueue
			# e=[command,room,nickname,affiliation]
			room=unicode(e[1])
			nickname=unicode(e[2])
			affiliation=unicode(e[3])
			self.groupchat[room]=[nickname,[]] # initialize room storage
			self.chat.addGroupChatTab(room,nickname,affiliation) # add room tab
			jab.getStoreQueue(room) # getStoreQueue

		elif e[0] == "avatar_show":
			# show contact avatar
			# e=[command,vcard,jid]
			vcard=e[1]
			jid=str(e[2])
			if vcard.has_key("PHOTO"):
				v=vcard["PHOTO"]
				if v.has_key("BINVAL"):
					pixmap=QtGui.QPixmap()
					image=base64.decodestring(str(v["BINVAL"]))
					f=open(self.homeDir+'/.jabbim/avatars/'+jid,"w")
					f.write(image)
					f.close()
					pixmap.loadFromData(image)
					for user,group in self.ui.roster.getUsers(jid,True).iteritems():
						user.setIcon(3,QtGui.QIcon(pixmap))

		elif e[0] == "game_list":
			self.gameslist.ui.treeWidget.clear()
			for game in e[1]:
				jid,name,status=game
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if str(w.jid)==jid:
						self.chat.ui.chatTab.setTabText(i,name)
				item=QtGui.QTreeWidgetItem(self.gameslist.ui.treeWidget)
				item.setText(0,name)
				if status=="pre":
					item.setText(2,self.tr("Yes"))
				else:
					item.setText(2,self.tr("No"))
				item.setData(32,0,QtCore.QVariant(jid))
				item.setData(32,1,QtCore.QVariant(jid))
				item.setData(32,2,QtCore.QVariant(jid))
			self.gameslist.ui.treeWidget.resizeColumnToContents(0)
			self.gameslist.ui.treeWidget.resizeColumnToContents(2)

		elif e[0] == "group_chat_config":
			form=e[1]
			jid=e[2]
			self.mucconfig=dataFormsWindow(self,jab,form,jid)
			self.mucconfig.show()

		elif e[0] == "discovery_register":
			form=e[1]
			jid=e[2]
			self.discovery_register=discoveryRegisterWindow(self,jab,form,jid)
			self.discovery_register.show()

		elif e[0] == "vcard_show":
			vcard=e[1]
			self.vcard=vcardWindow(self,vcard)
			self.vcard.show()
			
		elif e[0] == "groupchat_server_message":
			jid=str(e[1])
			text=unicode(e[2])
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					message=self.skin["status_message"].replace("[time]",self.now()).replace("[message]",unicode(text))
					w.chat.ui.info.setText(unicode(e[3]))
					w.chat.ui.info.setCursorPosition(0)
					w.chat.textEditWrite(message)
					return

		elif e[0] == "headline_message":
			#self.message_queue.append(["headline_message",jid,text,subject,urls,descs])
			jid=unicode(e[1])
			text=unicode(e[2])
			subject=e[3]
			urls=e[4]
			descs=e[5]
			timestamp=e[6]
			timestamp="%s-%s-%s %s:%s:%s" % (timestamp[0:4],timestamp[4:6],timestamp[6:8],timestamp[9:11],timestamp[12:14],timestamp[15:17])
			tab=None
			tabIndex=0
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if w.typ=="headline":
					tab=w
					tabIndex=i
			if tab!=None:
				if int(self.chat.ui.chatTab.currentIndex())!=tabIndex:
					self.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
				#yyyymmddThhmmss
				tab.chat.addMessage(jid,subject,text,urls,descs,timestamp)
				return
			tab=self.chat.addHeadlineTab()
			tab.addMessage(jid,subject,text,urls,descs,timestamp)

		elif e[0] == "groupchat_message":
			jid=str(e[1])
			user=unicode(e[2])
			timestamp=e[4]
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid:
					if timestamp==None or len(timestamp)==0:
						if unicode(w.name)==unicode(user):
							message=self.skin["my_message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
						else:
							if unicode(e[3]).lower().find(unicode(w.name).lower())!=-1:
								message=self.skin["message_for_me"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
							else:
								message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
						w.chat.textEditWrite(message)
						return
					else:
						timestamp=unicode(timestamp)
						timestamp="%s-%s-%s %s:%s:%s" % (timestamp[0:4],timestamp[4:6],timestamp[6:8],timestamp[9:11],timestamp[12:14],timestamp[15:17])
						if unicode(w.name)==unicode(user):
							message=self.skin["my_message_history"].replace("[time]",timestamp).replace("[user]",user).replace("[message]",unicode(e[3]))
						else:
							if unicode(e[3]).lower().find(unicode(w.name).lower())!=-1:
								message=self.skin["message_for_me_history"].replace("[time]",timestamp).replace("[user]",user).replace("[message]",unicode(e[3]))
							else:
								message=self.skin["message_history"].replace("[time]",timestamp).replace("[user]",user).replace("[message]",unicode(e[3]))
						w.chat.textEditWrite(message)

		elif e[0] == "chat_message":
			jid=str(e[1])
			if len(self.ui.roster.getUsers(jid))!=0:
				user=self.ui.roster.getUsers(jid)[0]
				icon=user.icon(0)
				user=user.text(2)
			else:
				icon=self.status["offline"]
				user=jid
				
			message=self.skin["message"].replace("[time]",self.now()).replace("[user]",unicode(user)).replace("[message]",unicode(e[3]))
			tab=None
			tabIndex=0
			for i in range(self.chat.ui.chatTab.count()):
				w=self.chat.ui.chatTab.widget(i)
				if str(w.jid)==jid+"/"+str(e[4]):
					tab=w
					tabIndex=i
					break
				if str(w.jid).rsplit("/")[0]==jid:
					tab=w
					tabIndex=i
			if self.config["tray_message_view_new_message"]=="all":
				notification.onNewChatMessage(self,user,unicode(e[3]))
			if tab!=None:
				if int(self.chat.ui.chatTab.currentIndex())!=tabIndex:
					self.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
				tab.chat.textEditWrite(message)
			else:
				if self.config["tray_message_view_new_message"]=="not_chat":
					notification.onNewChatMessage(self,user,unicode(e[3]))
				self.chat.addChatTab(jid,unicode(user),icon,message)

		elif e[0] == "subscribed":
			jid=str(e[1])
			self.events.show()
			self.events.addEvent("subscribed",{"jid":str(jid)})
			if not self.ui.roster.isUser(jid):
				self.groups["Unknown"]["users"][str(jid)]={"item":self.ui.roster.addUser(jid,jid,self.groups["Unknown"]["item"],self.offline,self.getIcon(jid,"offline")),"resources":[]}

		elif e[0] == "subscribe":
			jid=str(e[1])
			if not self.ui.roster.isUser(jid):
				if jid.startswith("@"):
					jab.roster.Authorize(str(jid))
				else:
					#if not self.ui.roster.isUser(jid):
					self.events.show()
					self.events.addEvent("subscribe",{"jid":str(jid)})
			else:
				jab.roster.Authorize(str(jid))
		
		elif e[0] == "nick_update":
			# Prisla presence
			jid=str(e[1])
			# Pokud je jid v rosteru:
			if self.ui.roster.isUser(jid):
				# Prochazeni vsech uzivatelu v rosteru, kteri maji shodne jid
				for user,group in self.ui.roster.getUsers(jid,True).iteritems():
					# Pokud se nejedna o odhlaseni uzivatele
					if str(e[2].getType())!="unavailable":
						# Pridani resource k uzivateli, pokud uz tam neni
						if not e[3] in self.groups[group]["users"][jid]["resources"]:
							self.groups[group]["users"][jid]["resources"].append(e[3])
							resources=self.groups[group]["users"][jid]["resources"]
							try:
								resources.remove('')
							except:
								pass
							# Pokud je resourcu vic, pridavaji se polozky do rosteru
							if len(resources)>1:
								# Zjisteni jid+"/"+resource v rosteru
								res=[]
								for i in range(user.childCount()):
									j=user.child(i)
									j=j.data(32,0)
									j=str(j.toString())
									res.append(j)
								for resource in resources:
									# Pokud uz neni resource v rosteru, pridame ho
									if not jid+'/'+resource in res and len(resource)!=0:
										item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)
						# Zmena stavu
						#if self.config["tray_message_view_connect"]=="all":
						notification.onRosterPresence(self,unicode(user.text(2)),str(e[2].getShow()),unicode(e[2].getStatus()),int(unicode(user.text(1)[0])))
						#elif self.config["tray_message_view_connect"]=="online" and str(e[2].getShow())=="None":
							#notification.onRosterPresence(self,unicode(user.text(2)),self.status[str(e[2].getShow())],unicode(e[2].getStatus()))
						#elif self.config["tray_message_view_connect"]=="logged_in" and int(unicode(user.text(1)[0]))==9:
							#notification.onRosterPresence(self,unicode(user.text(2)),self.status[str(e[2].getShow())],unicode(e[2].getStatus()))
						if str(e[2].getShow())!="None":
							user.setIcon(0,self.getIcon(jid,str(e[2].getShow())))
							#user.setIcon(0,self.statuses[str(e[2].getShow())])
							user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
						else:
							user.setIcon(0,self.getIcon(jid,"online"))
							user.setText(1,self.nickSort["online"]+unicode(user.text(2)))
						for i in range(self.chat.ui.chatTab.count()):
							w=self.chat.ui.chatTab.widget(i)
							if str(w.jid)==jid or str(w.jid).rsplit("/")[0]==jid:
								if str(e[2].getShow())!="None":
									self.chat.ui.chatTab.setTabIcon(i,self.getIcon(jid,str(e[2].getShow()),size="16x16"))
								else:
									self.chat.ui.chatTab.setTabIcon(i,self.getIcon(jid,'online',size="16x16"))
						# Nastaveni tooltip
						user.setToolTip(0,'<font color="blue"><b>'+unicode(user.text(2))+'</b> - '+str(e[2].getShow())+'</font><hr>'+unicode(e[2].getStatus())+'<br/><b>'+self.tr("Jabber ID:")+' </b>'+str(jid)+'')
						# Nastaveni stavove zpravy pod nick v rosteru. Pokud neni zprava nastavena, vytvori se jen nick bez zpravy.
						user.setText(0,unicode(user.text(2)))
						#if unicode(e[2].getStatus())=="None" or len(e[2].getStatus())==0:
							#user.label.setText(unicode(user.text(2)))
						#else:
							#text=[word for word in unicode(e[2].getStatus()).split('\n') if word != ''][0]
							#user.label.setText(unicode(self.ui.roster.getUsers(jid)[0].text(2))+'<br/><font size="-1"><i>'+text+"</i></font>")
						# Zobrazeni polozky v rosteru
						self.ui.roster.setItemHidden(user,False)
					# Jedna se o odhlaseni
					elif str(e[2].getType())=="unavailable":
						# Pokud byl user predtim prihlaseny
						if int(unicode(user.text(1))[0])!=9:
							# Odebrani resource z databaze
							try:
								self.groups[group]["users"][jid]["resources"].remove(e[3])
							except:
								print self.groups[group]["users"][jid]["resources"]
							# pokud by po smazani zbyla jen jedina resource, smaze se z rosteru
							if int(user.childCount())==2:
								for i in range(user.childCount()):
									user.takeChild(0)
							else:
								# pokud po smazani nezbude ani jedna resource, je kontakt offline
								if int(user.childCount())<=1:
									user.setIcon(0,self.getIcon(jid,"offline"))
									user.setText(1,self.nickSort["offline"]+unicode(user.text(2)))
									self.ui.roster.setItemHidden(user,self.offline)
								# smazani resource
								for i in range(user.childCount()):
									item=user.child(i)
									j=item.data(32,0)
									j=str(j.toString())
									if str(j)==jid+"/"+e[3]:
										user.takeChild(i)
										break
							for i in range(self.chat.ui.chatTab.count()):
								w=self.chat.ui.chatTab.widget(i)
								if str(w.jid)==jid or str(w.jid).rsplit("/")[0]==jid:
									self.chat.ui.chatTab.setTabIcon(i,self.getIcon(jid,'offline',size="16x16"))
				# aktualizace cisel skupin
				self.ui.roster.refreshStats()
				# serazeni polozek v rosteru
				self.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
			# Pokud je jid groupchat
			elif self.isGroupChat(jid):
				if str(e[2].getType())!="unavailable":
					nick=unicode(e[3])
					# Nalezeni spravneho groupchatu
					for i in range(self.chat.ui.chatTab.count()):
						w=self.chat.ui.chatTab.widget(i)
						if str(w.jid)==jid:
							# aktualizace uzivatele v seznamu
							if nick==self.groupchat[jid][0]:
								w.chat.changeAffiliation(e[2].getAffiliation())
							w.chat.editUser(jid,nick,str(e[2].getShow()),e[2].getRole(),e[2].getAffiliation())
							return
				elif str(e[2].getType())=="unavailable":
					nick=unicode(e[3])
					for i in range(self.chat.ui.chatTab.count()):
						w=self.chat.ui.chatTab.widget(i)
						if str(w.jid)==jid:
							w.chat.deleteUser(jid,nick)
							

		elif e[0] == "roster_update":
			print "roster update"
			items=e[1].getItems()
			for jid in items:
				if len(jid.split("@"))!=1:
					if not self.discoInfo.has_key(jid.split("@")[1]):
						jab.discoveryInfo(jid.split("@")[1])
				try:
					jid=str(jid).lower()
					groups=e[1].getGroups(jid)
					if groups==None or groups==[]:
						groups=["Unknown"]
					for group in groups:
						if self.groups.has_key(group)==False:
							self.groups[group]={"item":self.ui.roster.addGroup(group),"users":{}}
						name=e[1].getName(jid)
						self.groups[group]["users"][str(jid)]={"item":self.ui.roster.addUser(jid,name,self.groups[group]["item"],self.offline,self.getIcon(jid,"offline")),"resources":[]}
						if os.path.isfile(self.homeDir+'/.jabbim/avatars/'+jid):
							pixmap=QtGui.QPixmap()
							f=open(self.homeDir+'/.jabbim/avatars/'+jid,"r")
							image=f.read()
							f.close()
							pixmap.loadFromData(image)
							self.groups[group]["users"][str(jid)]['item'].setIcon(3,QtGui.QIcon(pixmap))
				except:
					pass
			self.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
			jab.outc.put(True)
			for k,v in self.groups.iteritems():
				self.ui.group.addItem(unicode(k))

	def tick(self):
		try:
			e=jab.discoveryQueue.get( timeout = 0 )
		except:
			e=None
		if e!=None:
			if e[0]=="muc_items":
				item=e[2]
				jid=e[3]
				name=unicode(item["jid"]).split("/")[1]
				for i in self.ui.groupchat.findItems(jid,QtCore.Qt.MatchExactly,1):
					user=QtGui.QTreeWidgetItem(i)
					user.setText(0,unicode(name))
					user.setText(1,unicode(name))
					user.setIcon(0,self.getIcon(size="16x16"))
			elif e[0]=="bookmarks_items":
				item=e[2]
				jid=e[3]
				name=unicode(item["jid"]).split("/")[1]
				for i in self.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1):
					user=QtGui.QTreeWidgetItem(i)
					user.setText(0,unicode(name))
					user.setText(1,unicode(name))
					user.setIcon(0,self.getIcon(size="16x16"))
			elif e[0]==None:
				typ=e[1]
				if typ=="items":
					item=e[2]
					jid=e[3]
					parentNode=e[4]
					if item.has_key("jid") and jid==jab.server:
						self.disco.addItem(unicode(item["jid"]))
						jab.discoveryInfo(item["jid"])
					if jid!=jab.server:
						name=""
						if item.has_key("name"):
							name=item["name"]
						node=""
						if self.discoInfo.has_key(jid):
							if self.discoInfo[jid]=="conf":
								groupchat=QtGui.QTreeWidgetItem(self.ui.groupchat)
								groupchat.setText(0,unicode(name))
								groupchat.setText(1,unicode(item["jid"]))
								groupchat.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))
								self.ui.groupchat.sortItems(0,QtCore.Qt.AscendingOrder)
						parent=self.disco.items[jid]
						if self.disco.nodes.has_key(jid+str(parentNode)):
							parent=self.disco.nodes[jid+str(parentNode)]
						if item.has_key("node"):
							node=item["node"]
						self.disco.addItem(unicode(item["jid"]),unicode(name),parent,node=node)
				else:
					ident=e[2]
					features=e[3]
					jid=e[4]
					if not self.discoInfo.has_key(jid) and ident[0].has_key("type"):
						if "http://jabber.org/protocol/muc" in features and ident[0]["type"]=="text":
							self.discoInfo[jid]="conf"
							self.ui.getGroupchatList.setEnabled(True)
						elif ident[0]["type"]=="bytestreams" and ident[0]["category"]=="proxy":
							jab.conn.S5B.addProxy(str(jid))
							#jab.conn.S5B.addProxy(str('proxy.jabberfr.org'))
							print "adding proxy",jid
						else:
							self.discoInfo[jid]=ident[0]["type"]
							users=self.ui.roster.getServerUsers(jid)
							for user in users:
								data=user.data(32,0)
								data=str(data.toString())
								#user.setIcon(0,QtGui.QIcon(self.statusPath+self.getUserType(data)+"-"+self.iconSort[unicode(user.text(1))[0]]+".png"))
								user.setIcon(0,self.getIcon(data,self.iconSort[unicode(user.text(1))[0]]))
						
	
					if self.disco.items.has_key(jid):
						for feature in features:
							if not feature in self.disco.items[jid].features:
								self.disco.items[jid].features.append(feature)
						if self.disco.items.has_key(jid):
							self.disco.items[jid].setText(0,ident[0]["name"])
						

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
			self.jabberError(self.tr("Bad username or password."))
			login.ui.connect.setEnabled(True)
		elif error == "muc-401":
			self.jabberError(self.tr("Password is required."))
		elif error == "muc-404":
			self.jabberError(self.tr("The room or server does not exist."))
		elif error == "muc-405":
			self.jabberError(self.tr("Room creation is restricted."))
		elif error == "muc-407":
			self.jabberError(self.tr("Your are not on the member list."))
		elif error == "muc-409":
			self.jabberError(self.tr("Your nickname is in use or registered by another user."))
		else:
			self.jabberError(self.tr("Unknown error ")+unicode(error))
	def jabberError(self,error):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(error),0,1)

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
		jab.setStatus(MainWindow.groupchat,self.data,unicode(self.ui.status.toPlainText ()))
		self.done(1)


app = QtGui.QApplication(sys.argv)

jab = Jabber(app)
translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()

login=loginWindow(MainWindow,jab,MainWindow)
ref=login.show()
sys.exit(app.exec_())

