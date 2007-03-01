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
from palette import *
from dataforms import *

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
				print feature
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
			print item.node
			jab.discoveryItems(unicode(item.text(1)),node=item.node)


class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=Ui_mainWindow()
		self.ui.setupUi(self)
		self.homeDir=self.getHomeDir()
		self.loadConfig()
		self.loadPaletteSkin()
		self.loadRoster()
		# Signals
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		#app.connect(self.ui.addContact, QtCore.SIGNAL("clicked(bool)"),self.addContact)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		app.connect(self.ui.actionAdd_contact, QtCore.SIGNAL("triggered ( bool )"),self.addContact)
		app.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered ( bool )"),self.trayQuit)
		app.connect(self.ui.actionService_discovery, QtCore.SIGNAL("triggered ( bool )"),self.discovery)
		self.timer=QtCore.QTimer()
		app.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tick)
		self.timer.start(20)
		self.loadSkin()
		self.loadStatus()
		self.bookmarks={}
		#self.loadBookmarks()
		self.loadGroupchat()
		self.groupchat={}
		#self.users={}
		self.groups={}
		self.groups["Unknown"]={"item":self.ui.roster.addGroup(self.tr("Unknown")),"users":{}}
		self.chat=chatWindow(self,self,jab)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		self.ready=False
		#self.log.show()
		
		self.games=[]
		self.gameslist=gamesListWindow(self,self,jab)
		self.preparedGames=[]
		
		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon("images/status/online.png"))
		menu=QtGui.QMenu(self)
		menu.addMenu(self.statusMenu)
		menu.addSeparator()
		menu.addAction(self.tr("Close"),self.trayQuit)
		
		app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.setContextMenu(menu)
		self.tray.show()
		self.events=groupedEventWindow(None,self,jab)
		self.jgamesLoadPlugins()
		self.gameServer="@games.jabbim.cz"

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
					self.chat.addGameChatTab(muc+self.gameServer,muc)
					self.groupchat[muc+self.gameServer]=[jab.user,[]]
					jab.getIntoRoom(muc+self.gameServer,jab.user)
					jab.getGroupchatConfig(muc+self.gameServer)
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

	def discovery(self):
		self.disco=discoveryWindow(self)
		self.disco.show()
		jab.discoveryItems()

	def trayQuit(self):
		self.tray.hide()
		self.timer.stop()
		app.closeAllWindows()
		jab.disconnect()
		sys.exit(0)

	def trayActivated(self,reason):
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

	def addContact(self,bool=None):
		contact=addContactWindow(self,jab)
		contact.exec_()

	def buildGroupchatMenu(self):
		self.groupchatMenu.clear()
		action=self.groupchatMenu.addAction(self.tr("Join new groupchat"))
		action.setData(QtCore.QVariant(["new"]))

		self.groupchatMenu.addSeparator()
		for k,v in self.bookmarks.iteritems():
			action=self.groupchatMenu.addAction(unicode(v["name"]))

			action.setData(QtCore.QVariant([unicode(k),unicode(v["nick"]),unicode(v["password"])]))
		self.groupchatMenu.addSeparator()
		action=self.groupchatMenu.addAction(self.tr("Manage bookmarks"))
		action.setData(QtCore.QVariant(["manage"]))

	def loadGroupchat(self):
		self.groupchatMenu=QtGui.QMenu(self.tr("Group Chat"),self.ui.toolBar)
		self.buildGroupchatMenu()
		self.ui.actionGroup_Chat.setMenu(self.groupchatMenu)
		self.ui.toolBar.addAction(self.groupchatMenu.menuAction())
		actionRect = self.ui.toolBar.actionGeometry(self.groupchatMenu.menuAction())
		toolButton = self.ui.toolBar.childAt(actionRect.center())
		toolButton.setPopupMode(QtGui.QToolButton.InstantPopup)
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
		self.status={"online":self.tr("Online"),
					"available":self.tr("Online"),
					"chat":self.tr("Chatty"),
					"away":self.tr("Away"),
					"xa":self.tr("Extended away"),
					"dnd":self.tr("DND"),
					"None":self.tr("Online"),
					"offline":self.tr("Offline")
					}
		self.statusMenu=QtGui.QMenu(self.tr("Status"),self.ui.statusButton)
		action=self.statusMenu.addAction(self.statuses['online'],self.status["online"])
		action.setData(QtCore.QVariant("online"))
		action=self.statusMenu.addAction(self.statuses['chat'],self.status["chat"])
		action.setData(QtCore.QVariant("chat"))
		action=self.statusMenu.addAction(self.statuses['away'],self.status["away"])
		action.setData(QtCore.QVariant("away"))
		action=self.statusMenu.addAction(self.statuses['xa'],self.status["xa"])
		action.setData(QtCore.QVariant("xa"))
		action=self.statusMenu.addAction(self.statuses['dnd'],self.status["dnd"])
		action.setData(QtCore.QVariant("dnd"))
		self.ui.statusButton.setMenu(self.statusMenu)
		app.connect(self.statusMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusChanged)
		self.offline=True


	def groupchatChanged(self,action):
		data=action.data()
		lst=data.toList()
		cmd=unicode(lst[0].toString())
		if cmd=="new":
			newchat=joinGroupChatWindow(self,jab)
			ret=newchat.exec_()
			if ret==1:
				self.chat.show()
		elif cmd=="manage":
			win=preferencesWindow(self,self,1,jab=jab)
			win.show()
		else:
			#action.setData(QtCore.QVariant([unicode(k),unicode(v["nick"]),unicode(v["password"])]))
			room=unicode(cmd)
			nickname=unicode(lst[1].toString())
			jab.getIntoRoom(room,nickname)
			self.groupchat[room]=[nickname,[]]
			self.chat.addGroupChatTab(room,nickname)

	def statusChanged(self,action):
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.statuses[str(data)])
		setstatus=statusWindow(data)
		setstatus.exec_()


	#def loadBookmarks(self):
		# loads config and repairs config file
		#self.bookmarks=ConfigObj(self.homeDir+'/.jabbim/bookmarks',encoding='UTF8')
		#if len(self.bookmarks)==0:
			#if not os.path.isdir(self.homeDir+'/.jabbim'):
				#os.mkdir(self.homeDir+'/.jabbim')
			#self.bookmarks=ConfigObj(self.homeDir+'/.jabbim/bookmarks',encoding='UTF8')
			#self.bookmarks.write()


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
				if int(user["item"].text(1)[0])==9:
					self.ui.roster.setItemHidden(user["item"], not bool)
			self.ui.roster.hidden(not bool)

	def now(self):
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def isGroupChat(self,jid):
		for k,v in self.groupchat.iteritems():
			if k==jid:
				return True
		return False

	def isGroupChatMember(self,chat,name):
		for user in self.groupchat[chat][1]:
			if unicode(user.text())==unicode(name):
				return True
		return False

	def getGroupChatMember(self,chat,name):
		for user in self.groupchat[chat][1]:
			if unicode(user.text())==unicode(name):
				return user
		return None


	def jabberCommandHandler(self,e):
		if e[0] == "con_ready":
			MainWindow.show()
			login.done(1)
			jab.setStatus(self.groupchat)
			jab.getBookmarks()
		elif e[0]=="bookmarks":
			self.bookmarks=e[1]
			self.buildGroupchatMenu()

		elif e[0] == "avatar_show":
			vcard=e[1]
			jid=str(e[2])
			if vcard.has_key("PHOTO"):
				v=vcard["PHOTO"]
				if v.has_key("BINVAL"):
					pixmap=QtGui.QPixmap()
					image=base64.decodestring(str(v["BINVAL"]))
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
					w.chat.textEditWrite(message)
					return

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
				user=self.ui.roster.getUsers(jid)[0]
				icon=user.icon(0)
				user=user.text(2)
			else:
				icon=self.status["offline"]
				user=jid
				
			message=self.skin["message"].replace("[time]",self.now()).replace("[user]",user).replace("[message]",unicode(e[3]))
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
				self.tray.showMessage(self.tr("New message from ")+unicode(user), unicode(e[3]), QtGui.QSystemTrayIcon.Information, 5000)
			if tab!=None:
				if int(self.chat.ui.chatTab.currentIndex())!=tabIndex:
					self.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/status/message.png"))
				tab.chat.textEditWrite(message)
				return
			if self.config["tray_message_view_new_message"]=="not_chat":
				self.tray.showMessage(self.tr("New message from ")+unicode(user), unicode(e[3]), QtGui.QSystemTrayIcon.Information, 5000)
			self.chat.show()
			self.chat.addChatTab(jid,unicode(user),icon,message)

		elif e[0] == "subscribed":
			jid=str(e[1])
			self.events.show()
			self.events.addEvent("subscribed",{"jid":str(jid)})
			if not self.ui.roster.isUser(jid):
				self.groups["Unknown"]["users"][str(jid)]={"item":self.ui.roster.addUser(jid,jid,self.groups["Unknown"]["item"],self.offline,self.statuses["offline"]),"resources":[]}

		elif e[0] == "subscribe":
			jid=str(e[1])
			if jid.startswith("@"):
				jab.roster.Authorize(str(jid))
			else:
				#if not self.ui.roster.isUser(jid):
				self.events.show()
				self.events.addEvent("subscribe",{"jid":str(jid)})

		
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
						if self.config["tray_message_view_connect"]=="all":
							self.tray.showMessage(self.tr("User status"), self.tr("User ")+unicode(user.text(2))+self.tr(" is now ")+self.status[str(e[2].getShow())]+"\n"+unicode(e[2].getStatus()), QtGui.QSystemTrayIcon.Information, 5000)
						elif self.config["tray_message_view_connect"]=="online" and str(e[2].getShow())=="None":
							self.tray.showMessage(self.tr("User status"), self.tr("User ")+unicode(user.text(2))+self.tr(" is now ")+self.status[str(e[2].getShow())]+"\n"+unicode(e[2].getStatus()), QtGui.QSystemTrayIcon.Information, 5000)
						elif self.config["tray_message_view_connect"]=="logged_in" and int(unicode(user.text(1)[0]))==9:
							self.tray.showMessage(self.tr("User status"), self.tr("User ")+unicode(user.text(2))+self.tr(" is now ")+self.status[str(e[2].getShow())]+"\n"+unicode(e[2].getStatus()), QtGui.QSystemTrayIcon.Information, 5000)
						if str(e[2].getShow())!="None":
							user.setIcon(0,self.statuses[str(e[2].getShow())])
							user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
						else:
							user.setIcon(0,self.statuses["online"])
							user.setText(1,self.nickSort["online"]+unicode(user.text(2)))
						for i in range(self.chat.ui.chatTab.count()):
							w=self.chat.ui.chatTab.widget(i)
							if str(w.jid)==jid or str(w.jid).rsplit("/")[0]==jid:
								self.chat.ui.chatTab.setTabIcon(i,user.icon(0))
						# Nastaveni tooltip
						user.setToolTip(0,'<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>'+self.tr("Jabber ID:")+' </b>'+str(jid)+'')
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
						print unicode(user.text(1))
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
									user.setIcon(0,self.statuses["offline"])
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
									self.chat.ui.chatTab.setTabIcon(i,user.icon(0))
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
							# Pokud je uzivatel jiz v mistnosti, nacteme jej od tam
							print jid,e[2].getAffiliation()
							if self.isGroupChatMember(jid,unicode(nick)):
								user=self.getGroupChatMember(jid,unicode(nick))
							# Pokud neni v mistnosti, vytvorime jej
							else:
								user=QtGui.QListWidgetItem(unicode(nick))
								self.groupchat[jid][1].append(user)
							# Nastaveni stavu
							if str(e[2].getShow())!="None":
								user.setIcon(self.statuses[str(e[2].getShow())])
								#user.setText(1,self.nickSort[str(e[2].getShow())]+unicode(user.text(2)))
							else:
								user.setIcon(self.statuses["online"])
							# Tooltip
							#user.setToolTip('<font color="blue"><b>'+unicode(user.text(2))+'</b></font><hr>'+unicode(e[2].getStatus())+'<br/><b>Jabber ID: </b>'+str(jid)+'')
							# Pridani do seznamu uzivatelu v mistnosti
							w.chat.ui.listWidget.addItem(user)
							# serazeni
							w.chat.ui.listWidget.sortItems()
							return
				elif str(e[2].getType())=="unavailable":
					nick=unicode(e[3])
					for i in range(self.chat.ui.chatTab.count()):
						w=self.chat.ui.chatTab.widget(i)
						if str(w.jid)==jid:
							user=self.getGroupChatMember(jid,unicode(nick))
							w.chat.ui.listWidget.takeItem(int(w.chat.ui.listWidget.row(user)))

		elif e[0] == "roster_update":
			print " roster update"
			items=e[1].getItems()
			for jid in items:
				try:
					jid=str(jid).lower()
					groups=e[1].getGroups(jid)
					if groups==None or groups==[]:
						groups=["Unknown"]
					for group in groups:
						if self.groups.has_key(group)==False:
							self.groups[group]={"item":self.ui.roster.addGroup(group),"users":{}}
						name=e[1].getName(jid)
						self.groups[group]["users"][str(jid)]={"item":self.ui.roster.addUser(jid,name,self.groups[group]["item"],self.offline,self.statuses["offline"]),"resources":[]}
				except:
					pass
			self.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
			jab.outc.put(True)
				

	def tick(self):
		# new chat lines handler
		lines = None#jab.newChatLines(self.actualRoom)
		if lines!=None and len(lines)!=0:
			for line in lines:
				self.widget.textEditWrite(line)
		try:
			e=jab.discoveryQueue.get( timeout = 0 )
		except:
			e=None
		if e!=None:
			typ=e[0]
			if typ=="items":
				item=e[1]
				jid=e[2]
				parentNode=e[3]
				if item.has_key("jid") and jid==jab.server:
					self.disco.addItem(unicode(item["jid"]))
					jab.discoveryInfo(item["jid"])
				if jid!=jab.server:
					name=""
					if item.has_key("name"):
						name=item["name"]
					node=""
					parent=self.disco.items[jid]
					if self.disco.nodes.has_key(jid+str(parentNode)):
						parent=self.disco.nodes[jid+str(parentNode)]
					if item.has_key("node"):
						node=item["node"]
					self.disco.addItem(unicode(item["jid"]),unicode(name),parent,node=node)
			else:
				ident=e[1]
				features=e[2]
				jid=e[3]
				#print "*",jid
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

jab = Jabber()
translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+str(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()

login=loginWindow(MainWindow,jab,MainWindow)
ref=login.show()
sys.exit(app.exec_())
