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
import sys,os
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

import qt4reactor as reactor
app = QtGui.QApplication(sys.argv)
reactor.install(app)
import time

from twisted.internet import reactor

import widgets
import pyxl

from configobj import ConfigObj
from include import utils
import urllib

class clientClass(pyxl.client.Client):

	def on_init(self):
		self.roster['groups']['Unknown']=self.main.ui.roster.addGroup('Unknown')
		self.temp_hosts=[]
		
	def on_discoInfoReceived(self, jid, node):
		# save type of host, it not exist
		if not self.main.hosts.has_key(jid):
			try:
				name=self.disco[jid][node]['identities'].keys()[0]
				typ=self.disco[jid][node]['identities'][name]['type']
			except:
				typ=None
			if typ!=None:
				if typ=="pep" or typ=="im":
					typ="jabber"
				elif typ=="file":
					typ="disk"
				self.main.hosts[jid]=typ

	def on_rosterAddUser(self, contact):
		# add user to the roster
		groups=contact.groups
		name=contact.name
		jid=contact.jid
		
		# get host info
		if len(unicode(jid).rsplit("@"))!=1:
			host=unicode(jid).rsplit("@")[1]
			if not self.disco.has_key(host) and not host in self.temp_hosts:
				#self.main.getUserType(host)
				self.temp_hosts.append(host)
				self.getDiscoInfo(host)

		# user is not in any group
		if len(groups)==0:
			# add user item to Unknown group
			self.roster['users'][jid].rosterItems.append(self.main.ui.roster.addUser(jid,name,self.roster['groups']['Unknown'],first=True))
		else:
			for group in groups:
				# add user item to the group
				self.roster['users'][jid].rosterItems.append(self.main.ui.roster.addUser(jid,name,self.roster['groups'][group],first=True))

	def on_discoItemsBookmarksReceived(self, jid):
		# make user list for bookmarked groupchat
		item=self.main.ui.bookmarks.findItems(jid,QtCore.Qt.MatchExactly,1)[0]
		for name in self.disco[jid][None]['items'].keys():
			user=QtGui.QTreeWidgetItem(item)
			user.setText(0,unicode(name))
			user.setText(1,unicode(name))
			user.setIcon(0,self.main.getIcon(size="16x16"))

	def on_rosterArrived(self):
		# build Bookmarks tab
		self.main.buildBookmarks()
		# hide Unknown group, if has not users
		if int(self.roster['groups']['Unknown'].childCount())==0:
			self.main.ui.roster.setItemHidden(self.roster['groups']['Unknown'],True)

		self.metaParents={}

		# get metacontacts
		meta={} # temp variable for metacontacts - {userTag:userJid}
		for jid,user in self.roster['users'].iteritems():
			if user.tag!=None:
				if not meta.has_key(user.tag):
					meta[user.tag]=[jid]
				else:
					meta[user.tag].append(jid)

		print "META:",meta
		# process metacontacts
		for tag,jids in meta.iteritems():
			# get main metacontact (first metacontact)
			mainJid=None # JID of main metacontact (parent of all other)
			for jid in jids:
				if jid!=tag:
					mainJid=jids[0]
					break
			#If we had some others metacontacts
			if mainJid!=None:
				self.metaParents[tag]=self.main.ui.roster.addMetaParent(tag,self.roster['users'][mainJid].rosterItems[0].parent())
				for jid in jids:
					toDel=[] # contacts to delete
					# add metacontat to the all items of mainJid in roster
					#for item in self.roster['users'][mainJid].rosterItems:
					self.roster['users'][jid].rosterItems.append(self.main.ui.roster.addMetaContact(jid,jid,self.metaParents[tag]))
					# Delete metacontacts' top level items from roster
					for contact in self.roster['users'][jid].rosterItems:
						it=contact.data(32,0)
						it=it.toList()
						if unicode(it[1].toString())=="contact":
							toDel.append(contact)
							parent=contact.parent()
							parent.takeChild(parent.indexOfChild(contact))
					# delete metacontacts top level items from pyxl
					for item in toDel:
						self.roster['users'][jid].rosterItems.remove(item)

		# sort roster items and refresh group stats
		self.main.ui.roster.sortItems (1,QtCore.Qt.AscendingOrder)
		self.main.ui.roster.refreshStats()
		print "METAPARENTS",self.metaParents

	def on_authFailed(self,xmlstream):
		# Authentication error
		QtGui.QMessageBox.warning(self.main,self.main.tr("Error"),unicode(self.main.tr("Bad Jabber ID or password.")),0,1)
	
	def on_firstpresence(self,  bulk):
		# process all first presences at once
		for presence in bulk:
			#print presence
			jid=presence[0]
			show=presence[1]
			self.on_presence(jid,show,True)
		# refresh group stats
		self.main.ui.roster.refreshStats()

	def on_GCpresence(self,  muc, nick,  show,  status,  codes = []):
		if show=="offline":
			pass
		else:
			# get user role
			role=self.groupchats[muc].users[nick].role
			# find good tab according to jid
			for i in range(self.main.chat.ui.chatTab.count()):
				w=self.main.chat.ui.chatTab.widget(i)
				if unicode(w.jid)==unicode(muc):
					# edit user item
					w.chat.editUser(nick,show,role)
					break

	def on_presence(self,jid,show,first=False):
		if show=="offline":
			jid=jid.full() # get jid
			# presence has resource
			if len(unicode(jid).rsplit("/"))!=1:
				resource=unicode(jid).rsplit("/")[1]
				jid=unicode(jid).rsplit("/")[0]
				# if user has this resource, we have to delete it in all r
				#print resource,jid,self.roster['users'][jid].resourcesItems
				#if self.roster['users'][jid].resourcesItems.has_key(resource):
					#print self.roster['users'][jid].rosterItems
					#for user in self.roster['users'][jid].rosterItems:
						##self.roster['users'][unicode(jid).rsplit("/")[0]].resourcesItems[resource]=self.main.ui.roster.addResource(jid,unicode(user.text(2))+" - "+k,user)
						#user.takeChild(user.indexOfChild(self.roster['users'][jid].resourcesItems[resource]))
					#del self.roster['users'][jid].resourcesItems[resource]
				print self.roster['users'][jid].resources,resource,jid
				if len(self.roster['users'][jid].resources)>1:
					highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
					self.main.ui.roster.setStatus(jid,highest.show,first=first)
				else:
					self.main.ui.roster.setStatus(jid,show,first=first)
			else:
				self.main.ui.roster.setStatus(jid,show,first=first)
		else:
			jid=jid.full()
			# Pridani resource
			if len(unicode(jid).rsplit("/"))!=1:
				resource=unicode(jid).rsplit("/")[1]
				jid=unicode(jid).rsplit("/")[0]
				#if len(self.roster['users'][jid].resources)>1:
					#for i,v in self.roster['users'][jid].resources.iteritems():
						#if not self.roster['users'][jid].resourcesItems.has_key(i):
							#if self.roster['users'][jid].resourcesItems.has_key(0):
								#add=False
							#else:
								#if self.roster['users'][jid].tag==None or self.roster['users'][jid].tag==jid:
									#add=False
								#else:
									#add=True
							#for user in self.roster['users'][jid].rosterItems:
								#if add:
									#self.roster['users'][jid].resourcesItems[0]=self.main.ui.roster.addSubGroup(self.main.tr("Resources:"),user,first="911")
								#try:
									#self.roster['users'][jid].resourcesItems[i]=self.main.ui.roster.addResource(jid + "/" + i,i,user)
								#except:
									#print "ERROR:",unicode(jid),unicode(show),unicode(resource),user
								#self.main.ui.roster.setResourceStatus(jid,i,v.show)
				highest=self.roster['users'][jid].resources[self.roster['users'][jid].getHighestResource()]
				status=None
				if highest.status!=None:
					status=highest.status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				self.main.ui.roster.setStatus(jid,highest.show,status=status,first=first)
				#self.main.ui.roster.setResourceStatus(jid,resource,show)
			else:
				status=self.roster['users'][jid].status[1]
				if status!=None:
					status=status.replace("\n"," ").replace("<","&lt;").replace(">","&gt;")
				self.main.ui.roster.setStatus(jid,show,status=status,first=first)
				
	def on_xml(self,xml):
		if self.main.xmlConsole.ui.enable.isChecked():
			text=unicode(xml)
			self.main.xmlConsole.ui.xml.append(text+"\n\n")
	
	def on_UpdateContact(self,jid):
		#print "update",unicode(jid),"groups:",self.roster['users'][jid].groups
		contact=self.roster['users'][jid]
		items=contact.getUserItems()
		toDel=[]
		for name,item in self.roster['groups'].iteritems():
			if name in contact.groups:
				add=True
				for i in items:
					parent=i.parent()
					if item==parent:
						add=False
						name=contact.name
						if name==None or len(name)==0:
							name=jid
						i.setText(0,unicode(name))
						i.setText(1,unicode(i.text(1))[0]+unicode(name).lower())
						i.setText(2,unicode(name))
						item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
						self.main.ui.roster.setStatus(jid,self.main.icons[unicode(i.text(1))[0]],i)
						self.main.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
						
				if add:
					if len(contact.getUserItems())!=0:
						i=contact.getUserItems()[0].clone() # clone contact item
						contact.rosterItems.append(i)
						for x in range(int(i.childCount())):
							child=i.child(x)
							
							it=child.data(32,0)
							it=it.toList()
							data=unicode(it[0].toString())
							typ=unicode(it[1].toString())
							
							if typ=="meta":

								#print "len",len(self.roster['users'][data].rosterItems)
								#print data,jid
								self.roster['users'][data].rosterItems.append(child)
								#print "len",len(contact.rosterItems)
						self.roster['groups'][name].addChild(i) # add item to the new group
						self.main.ui.roster.setStatus(contact.jid,None,i)
					else:
						contact.rosterItems.append(self.main.ui.roster.addUser(contact.jid,contact.name,self.roster['groups'][name]))
						self.main.ui.roster.sortItems(1,QtCore.Qt.AscendingOrder)
						self.main.ui.roster.setStatus(contact.jid,None)
						self.main.ui.roster.refreshStats()
			else:
				for i in items:
					parent=i.parent()
					if item==parent:
						self.roster['users'][unicode(jid)].rosterItems.remove(i)
						parent.takeChild(parent.indexOfChild(i))
						if int(parent.childCount())==0:
							toDel.append(unicode(parent.text(2)))
							self.main.ui.roster.takeTopLevelItem(self.main.ui.roster.indexOfTopLevelItem(parent))
						break
		for name in toDel:
			del self.roster['groups'][name]

	def on_DeleteContact(self,jid):
		#print "delete",unicode(jid)
		contact=self.roster['users'][jid]
		items=contact.getUserItems()
		for name,item in self.roster['groups'].iteritems():
			for i in items:
				parent=i.parent()
				if item==parent:
					parent.takeChild(parent.indexOfChild(i))
					break

	def on_subscribe(self, msg,t):
		#self.ui.infoDockWidget.show()
		pass



	def on_GCmessage(self, frm, typ, body, subject = None, xhtml = None,  chatstate = None,  delay = None):
		if len(unicode(frm).rsplit("/"))==2:
			user=unicode(frm).rsplit("/")[1]
			frm=unicode(frm).rsplit("/")[0]
		else:
			user=frm
		#print delay
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			if unicode(w.jid)==frm:
				for word in unicode(body).split(' '):
					if word.find("http://")!=-1:
						body=body.replace(word,'<a href="'+unicode(urllib.unquote(word))+'">'+word+'</a>')
				if delay==None or len(delay)==0:
					if unicode(w.name)==unicode(user):
						message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",user).replace("[message]",unicode(body))
					else:
						if unicode(body).lower().find(unicode(w.name).lower())!=-1:
							message=self.main.skin["message_for_me"].replace("[time]",self.main.now()).replace("[user]",user).replace("[message]",unicode(body))
						else:
							message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",user).replace("[message]",unicode(body))
					w.chat.textEditWrite(message)
					return
				else:
					delay=unicode(delay)
					delay="%s-%s-%s %s:%s:%s" % (delay[0:4],delay[4:6],delay[6:8],delay[9:11],delay[12:14],delay[15:17])
					if unicode(w.name)==unicode(user):
						message=self.main.skin["my_message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
					else:
						if unicode(body).lower().find(unicode(w.name).lower())!=-1:
							message=self.main.skin["message_for_me_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
						else:
							message=self.main.skin["message_history"].replace("[time]",delay).replace("[user]",user).replace("[message]",unicode(body))
					w.chat.textEditWrite(message)

	def on_message(self, frm, typ, body, subject = None, xhtml = None,chatstate = None,  delay = None):
		print chatstate
		#print "message",frm
		if self.roster['users'].has_key(unicode(frm).rsplit("/")[0]):
			user=self.roster['users'][unicode(frm).rsplit("/")[0]].rosterItems[0]
			icon=user.icon(0)
			user=user.text(2)
		else:
			icon=self.main.getIcon(status="offline",size="16x16")
			user=frm
		
		message=unicode(body).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
		message=self.main.skin["message"].replace("[time]",self.main.now()).replace("[user]",unicode(user)).replace("[message]",message)
		tab=None
		tabIndex=0
		for i in range(self.main.chat.ui.chatTab.count()):
			w=self.main.chat.ui.chatTab.widget(i)
			if unicode(w.jid)==unicode(frm):
				tab=w
				tabIndex=i
				break
			if unicode(w.jid).rsplit("/")[0]==unicode(frm).rsplit("/")[0]:
				tab=w
				tabIndex=i
		if tab!=None:
			if int(self.main.chat.ui.chatTab.currentIndex())!=tabIndex:
				self.main.chat.ui.chatTab.setTabIcon(tabIndex,QtGui.QIcon("images/16x16/actions/message.png"))
			tab.chat.textEditWrite(message)
		else:
			self.main.chat.addChatTab(frm,unicode(user),icon,message)

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
		self.homeDir=utils.getHomeDir() # get home dir
		utils.loadConfig(self) # load config files
		self.client=None
		# fill login form
		self.ui.login_password.setText(self.config['passwd'])
		self.ui.login_jid.setText(self.config['jid'])
		if self.config['savePasswd']=="True":
			self.ui.login_savePassword.setChecked(True)
		self.hosts={}

		self.chat=widgets.chatwindow.chatWindow(self,self)

		app.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		app.connect(app,QtCore.SIGNAL("lastWindowClosed() "),self.disconnect)
		app.connect(self.ui.showOffline, QtCore.SIGNAL("clicked(bool)"),self.hideOffline)
		app.connect(self.ui.actionShow_XML, QtCore.SIGNAL("triggered ( bool )"),self.showXml)
		app.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		app.connect(self.ui.actionJoin_Groupchat, QtCore.SIGNAL("triggered ( bool )"),self.joinGroupchat)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("customContextMenuRequested ( const QPoint & )"),self.bookmarksContextMenu)
		app.connect(self.ui.newBookmark, QtCore.SIGNAL("clicked ()"),self.newBookmark)
		QtCore.QObject.connect(self.ui.bookmarks, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.bookmarksClicked)

		self.ui.bookmarks.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.ui.bookmarks.header().hide()
		self.ui.bookmarks.hideColumn(1)

		self.ui.rosterStackedWidget.setCurrentIndex(0)
		self.loadRoster()
		self.loadSkin() # load chat skin
		self.statusPath="images/xxxxx/status/"
		self.shows={u"online":u"1",
					u"available":u"1",
					u"chat":u"2",
					u"away":u"3",
					u"xa":u"4",
					u"dnd":u"5",
					u"None":u"1",
					u"offline":u"9",
					u"unavailable":u"9"
					}
		self.icons={u"1":u"online",
					u"2":u"chat",
					u"3":u"away",
					u"4":u"xa",
					u"5":u"dnd",
					u"9":u"offline"
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
		action=self.statusMenu.addAction(self.getIcon(status="offline",size="16x16"),self.status["offline"])
		action.setData(QtCore.QVariant("offline"))
		self.ui.statusButton.setMenu(self.statusMenu)
		app.connect(self.statusMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusChanged)
		self.ui.statusButton.setText(unicode(self.status["offline"]))
		self.ui.statusButton.setIcon(self.getIcon("offline",size="16x16"))
		self.ui.statusButton.hide()
		self.offline=False
		self.xmlConsole=XMLConsole(self)
		self.ui.showOffline.hide()
		
		#self.addInfoSubscribe()
		#self.addInfoSubscribe()
		#self.addInfoSubscribe()

	#def addInfoSubscribe(self):
		#widget=subscribeWidget(self.ui.infoDockWidget)
		#self.ui.infoLayout.addWidget(widget)

	def bookmarksClicked(self,item,i):
		# join bookmarked groupchat
		data=item.data(0,32)
		lst=data.toList()
		jid=unicode(lst[0].toString()) # get jid
		nickname=unicode(lst[1].toString()) # get nickname
		# send jabber command
		self.chat.addGroupChatTab(jid,nickname)
		#self.main.groupchat[room+"@"+server]=[nickname,[]]
		self.client.joinGC(jid, nickname)

	def buildBookmarks(self):
		self.ui.bookmarks.clear()
		for k,v in self.client.bookmarks['conference'].iteritems():
			# add bookmark to the bookmarks list
			item=QtGui.QTreeWidgetItem(self.ui.bookmarks)
			item.setText(0,unicode(v.name))
			item.setText(1,unicode(v.jid.full()))
			item.setData(0,32,QtCore.QVariant([unicode(v.jid.full()),unicode(v.nick),unicode(v.password)]))
			item.setIcon(0,QtGui.QIcon("images/16x16/categories/muc.png"))


	def joinGroupchat(self,bool):
		newchat=widgets.joingroupchat.joinGroupChatWindow(self)
		ret=newchat.exec_()

	def bookmarksContextMenu(self,pos):
		# make groupchat bookmarks menu
		item=self.ui.bookmarks.itemFromIndex(self.ui.bookmarks.indexAt(pos)) # get selected item
		jid=unicode(item.text(1)) # get item jid
		menu=QtGui.QMenu(self.ui.bookmarks) # make menu
		if item.parent()==None:
			# Join bookmarked groupchat
			action=menu.addAction(self.tr("Join"))
			action.setData(item.data(0,32))
			action.setObjectName("join_bookmark")
			action=menu.addAction(self.tr("User list"))
			action.setData(item.data(0,32))
			action.setObjectName("show_users")
			# separator
			menu.addSeparator()
			# Edit bookmark
			action=menu.addAction(self.tr("Edit bookmark"))
			action.setData(item.data(0,32))
			action.setObjectName("edit_bookmark")
			# Delete bookmark
			action=menu.addAction(self.tr("Delete bookmark"))
			action.setData(item.data(0,32))
			action.setObjectName("delete_bookmark")

		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.groupchatContextMenuTriggered)
		# set menu position and show
		menu.move(self.ui.bookmarks.mapToGlobal(pos))
		menu.show()

	def newBookmark(self):
		# make new bookmark
		edit=widgets.preferences.editBookmark(self,"","","","","",self,False)
		ret=edit.exec_()


	def groupchatContextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="join":
			# join groupchat from Groupchats list
			jid=action.data() # get jid
			jid=unicode(jid.toString())
			room=jid.split("@")[0] # get room
			server=jid.split("@")[1] # get server
			# show join groupchat dialog
			newchat=joinGroupChatWindow(self,room=room,server=server)
			ret=newchat.exec_()
		elif cmd=="join_bookmark":
			# join bookmarked groupchat
			data=action.data()
			lst=data.toList()
			jid=unicode(lst[0].toString()) # get jid
			nickname=unicode(lst[1].toString()) # get nickname
			# send jabber command
			self.chat.addGroupChatTab(jid,nickname)
			#self.main.groupchat[room+"@"+server]=[nickname,[]]
			print jid,nickname
			self.client.joinGC(jid, nickname)
		elif cmd=="edit_bookmark":
			item=self.ui.bookmarks.currentItem()
			data=action.data()
			lst=data.toList()
			jid=unicode(lst[0].toString()) # get jid
			if len(jid.split("@"))!=1:
				room=jid.split("@")[0]
				server=jid.split("@")[1]
			else:
				room=jid
			name=unicode(item.text(0))
			nickname=unicode(lst[1].toString()) # get nickname
			password=unicode(lst[2].toString()) # get password
			edit=widgets.preferences.editBookmark(self,room,server,name,nickname,password,self)
			edit.exec_()
		elif cmd=="delete_bookmark":
			item=self.ui.bookmarks.currentItem()
			#self.ui.bookmarks.takeTopLevelItem(self.ui.bookmarks.indexOfTopLevelItem(item))
			del self.client.bookmarks['conference'][unicode(item.text(0))]
			self.client.setBookmarks()
			self.buildBookmarks()
			#jab.setBookmarks(self.bookmarks)
		elif cmd=="show_users":
			item=self.ui.bookmarks.currentItem()
			if int(item.childCount())!=0:
				# delete all users in groupchat
				for i in range(item.childCount()):
					item.takeChild(0)
			# set item expanded
			self.ui.bookmarks.setItemExpanded(item,True)
			self.client.getDiscoItems(unicode(item.text(1)),callback=self.client.on_discoItemsBookmarksReceived,callback_par=unicode(item.text(1)))

	def getUserType(self,jid):
		# get type of jid (rss,disk,jabber, etc.)
		print self.client.disco[jid]
		#if len(jid.split("@"))!=1:
			#if self.discoInfo.has_key(jid.split("@")[1]):
				#typ=self.discoInfo[jid.split("@")[1]]
				#if typ=="pep" or typ=="im":
					#typ="jabber"
				#elif typ=="file":
					#typ="disk"
				#return typ
		#else:
			#print jid
		return "jabber"

	def preferencesClicked(self,bool):
		# shows preferences
		w=widgets.preferences.preferencesWindow(self,self)
		w.show()

	def loadSkin(self):
		# loads config and repairs config file
		self.skin=ConfigObj("skins/"+self.config["chat_skin"],encoding='UTF8')

	def now(self):
		# get time
		h,m,s=time.localtime()[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def showXml(self,bool):
		self.xmlConsole.show()

	def hideOffline(self,bool):
		# hide or show offline users
		self.offline=not bool
		# rewrite online/all users stats in group QTreeWidgetItem
		for group,item in self.client.roster['groups'].iteritems():
			# return stats (online,offline,all users) for group
			for i in range(int(item.childCount())):
				child=item.child(i)
				if int(unicode(child.text(1))[0])==9:
					self.ui.roster.setItemHidden(child, not bool)
			self.ui.roster.hidden(not bool)

	def statusChanged(self,action):
		# status changed
		data=action.data()
		data=data.toString()
		self.ui.statusButton.setText(unicode(action.text()))
		self.ui.statusButton.setIcon(self.getIcon(status=data,size="16x16"))
		setstatus=statusWindow(data)
		setstatus.exec_()

	def loadRoster(self):
		# load roster widget
		layout=QtGui.QHBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.roster=widgets.rosterWidget.rosterWidget(self.ui.rosterWidget,self)
		layout.addWidget(self.ui.roster)

	def _connected(self):
		self.ui.rosterStackedWidget.setCurrentIndex(1)
		self.ui.statusButton.setText(unicode(self.status["online"]))
		self.ui.statusButton.setIcon(self.getIcon("online",size="16x16"))
		self.ui.statusButton.show()
		self.ui.showOffline.show()


	def disconnect(self):
		if self.client!=None:
			reactor.stop2()

	def getIcon(self,jid=None,typ=None,size="32x32",status=None,usertype="jabber"):
		# return status icon
		path=self.statusPath.replace("xxxxx",size)
		typ=unicode(typ)
		if jid!=None:
			#file=path+self.getUserType(jid)+"-"+self.icons[self.show[typ]]+".png"
			if len(jid.split("@"))>1:
				host=jid.split("@")[1]
			else:
				host=None
			if self.hosts.has_key(host):
				usertype=self.hosts[host]
			if status==None:
				status=self.icons[self.shows[typ]]
			file=path+usertype+"-"+status+".png"
			if os.path.exists(file):
				icon=QtGui.QIcon(file)
			else:
				#print "File not exist",file," <-",jid,typ
				#print "using",path+"jabber-"+self.iconSort[self.nickSort[typ]]+".png"
				icon=QtGui.QIcon(path+"jabber-"+self.icons[self.shows[typ]]+".png")
		else:
			if status==None:
				icon=QtGui.QIcon(path+"jabber-online.png")
			else:
				icon=QtGui.QIcon(path+"jabber-"+status+".png")
		return icon

	def connect(self):
		# Connect to the server
		jid=unicode(self.ui.login_jid.text())
		password=unicode(self.ui.login_password.text())
		if len(jid)!=0 and len(jid.split("@"))==2 and len(password)!=0:
			
			if jid!=self.config['jid'] or (password!=self.config['passwd'] and self.config['savePasswd']=="True") or self.config['savePasswd']!=unicode(self.ui.login_savePassword.isChecked()):
				ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save current login information?"),3,4)
				if ret==3:
					self.config['savePasswd']=self.ui.login_savePassword.isChecked()
					if self.ui.login_savePassword.isChecked()==True:
						self.config['passwd']=password
					else:
						self.config['passwd']=""
					self.config['jid']=jid
					self.config.write()
		if self.client==None:
			self.client = clientClass(jid+"/jabbim", password, jid.split("@")[1], 5222,self)
		self.client.connect()

class XMLConsole(QtGui.QMainWindow):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=widgets.xmlConsole.Ui_xmlConsole()
		self.ui.setupUi(self)

class statusWindow(QtGui.QDialog):
	def __init__(self,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=widgets.status.Ui_status()
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
		if self.data=="offline":
			MainWindow.client.sendPresence(show = "unavailable", status = unicode(self.ui.status.toPlainText ()))
			MainWindow.client.factory.stopTrying()
			MainWindow.ui.statusButton.setText(unicode(MainWindow.status["offline"]))
			MainWindow.ui.statusButton.setIcon(MainWindow.getIcon("offline",size="16x16"))
			MainWindow.ui.statusButton.hide()
			MainWindow.ui.rosterStackedWidget.setCurrentIndex(0)
			MainWindow.ui.showOffline.hide()

			pass
		else:
			#app.postEvent(jab,customEvent(["set_status",self.groupchat,self.data,unicode(self.ui.status.toPlainText ())]))
			#jab.setStatus(MainWindow.groupchat,self.data,unicode(self.ui.status.toPlainText ()))
			MainWindow.client.sendPresence(show = unicode(self.data), status = unicode(self.ui.status.toPlainText ()))
		self.done(1)


translator=QtCore.QTranslator()
translator.load("locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm")
app.installTranslator(translator)

MainWindow = mainWindow()
MainWindow.show()
reactor.run()

