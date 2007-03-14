
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from palette import *
from subscription_ui import *
from addcontact import *

class subscriptionWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_subscriptionwidget()
		self.ui.setupUi(self)
		self.ui.gridlayout.setMargin(3)
		self.ui.gridlayout.setSpacing(0)

class rosterWidget(QtGui.QTreeWidget):
	def __init__(self,parent,main,jab):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.setObjectName("roster")
		# main variables
		self.main=main # mainwindow pointer
		self.jab=jab # jab instance pointer
		self.edit=0 # temp variable for tabPressed()
		# roster config and design informations
		self.setAlternatingRowColors(True)
		self.setIconSize(QtCore.QSize(22,22))
		self.setRootIsDecorated(False)
		self.setDragEnabled(True)
		self.setAcceptDrops(True)
		self.setAllColumnsShowFocus(True)
		#self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.header().hide()
		# add and hide columns
		self.headerItem().setText(0,QtGui.QApplication.translate("roster", "Roster", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(1,QtGui.QApplication.translate("roster", "id", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(2,QtGui.QApplication.translate("roster", "name", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(3,QtGui.QApplication.translate("roster", "", None, QtGui.QApplication.UnicodeUTF8))
		self.hideColumn(1)
		self.hideColumn(2)
		# signals
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.contactClicked)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemExpanded ( QTreeWidgetItem * )"),self.expanded)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemCollapsed ( QTreeWidgetItem * )"),self.collapsed)
		short=QtGui.QShortcut("f2",self)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.editItem)
		# little hack for hidden items (we need some item at the end of roster)
		self.item=QtGui.QTreeWidgetItem(self)
		self.item.setText(1,"999")
		self.setItemHidden(self.item, True)
		# set color palette
		palette=self.palette()
		palette,images=loadPalette(palette,self.main.palette["roster"])
		self.setPalette(palette)
		self.pixmap=images['bgImage']
		self.addSubscription("test")
		self.addSubscription("test")
		self.addSubscribed("test")
		self.addSubscribed("test")
	
	def expanded(self,item):
		# change icon if group item expanded
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/32x32/icons/group-open.png"))

	def collapsed(self,item):
		# change icon if group item collapsed
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/32x32/icons/group-closed.png"))

	def resizeEvent(self,event):
		# when we resize roster, we need to resize columns too, because of avatar.
		QtGui.QTreeWidget.resizeEvent(self,event)
		if self.verticalScrollBar().isVisible():
			self.setColumnWidth(0,int(self.width())-50)
		else:
			self.setColumnWidth(0,int(self.width())-38)

	def hidden(self,bool):
		# little hack (qt don't repaint reshown items, when we have not one top level item at the end)
		self.setItemHidden(self.item, False)
		self.setItemHidden(self.item, True)

	def contactClicked(self,item,column):
		# open chat window for clicked contact
		if self.isGroupItem(item):
			return
		data=item.data(32,0) # get jid
		data=str(data.toString())
		self.main.chat.addChatTab(data,unicode(item.text(2)),self.main.getIcon(data,self.main.iconSort[unicode(item.text(1))[0]],size="16x16"))

	def getStats(self,group):
		# return stats (online,offline,all users) for group
		offline=0
		online=0
		for k,user in self.main.groups[unicode(group)]["users"].iteritems():
			if int(unicode(user["item"].text(1))[0])==9:
				offline+=1
			else:
				online+=1
		return online,offline,online+offline

	def refreshStats(self):
		# rewrite online/all users stats in group QTreeWidgetItem
		for k,v in self.main.groups.iteritems():
			online,offline,count=self.getStats(unicode(k))
			self.main.groups[k]["item"].setText(0,unicode(self.main.groups[k]["item"].text(2))+" ("+str(online)+"/"+str(count)+")")

	def isUser(self,jid):
		# returns True, if jid is user in roster
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(str(jid)):
				return True
		return False

	def isGroupItem(self,item):
		# return True, if item is group item in roster
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["item"]==item:
				return True
		return False

	def getUsers(self,jid,group=False):
		# return all QTreeWidgetItems for JID jid [item,item, ...]
		# if group is True, return {item:group, ...}
		users=[]
		groups={}
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				users.append(self.main.groups[k]["users"][str(jid)]["item"])
				groups[self.main.groups[k]["users"][str(jid)]["item"]]=k
		if group==True:
			return groups
		return users

	def getServerUsers(self,jid,group=False):
		# get all QTreeWidgetItems which are on server 'jid'. [item,item, ...]
		# if group is True, return {item:group, ...}
		users=[]
		groups={}
		for k,v in self.main.groups.iteritems():
			for key in self.main.groups[k]["users"].keys():
				if len(key.split("@"))>1:
					if key.split("@")[1]==jid:
						users.append(self.main.groups[k]["users"][key]["item"])
						groups[self.main.groups[k]["users"][key]["item"]]=k
		if group==True:
			return groups
		return users

	def getResources(self,jid):
		# get jid resources
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				return self.main.groups[k]["users"][str(jid)]["resources"]

	def delUser(self,jid,user):
		# del user with JID jid and QTreeWidgetItem user
		parent=user.parent()
		index=parent.indexOfChild(user)
		parent.takeChild(index)
		if int(parent.childCount())==0:
			self.takeTopLevelItem(self.indexOfTopLevelItem(parent))
		if parent==self.main.groups['Unknown']['item']:
			group="Unknown"
		else:
			group=unicode(parent.text(2))
		del self.main.groups[group]["users"][str(jid)]
		if len(self.main.groups[group]["users"])==0:
			del self.main.groups[group]

	def getGroups(self,jid):
		# get all groups where is JID jid
		groups=[]
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				if v['item']==self.main.groups['Unknown']['item']:
					groups.append("Unknown")
				else:
					groups.append(unicode(k))
		return groups

	def addSubscribed(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		widget=QtGui.QWidget(self)
		widget.setMinimumHeight(85)
		gridlayout = QtGui.QGridLayout(widget)
		spacerItem = QtGui.QSpacerItem(41,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		gridlayout.addItem(spacerItem,1,1,1,1)
		
		ok = QtGui.QToolButton(widget)
		gridlayout.addWidget(ok,1,0,1,1)
		
		text = QtGui.QLabel()
		text.setWordWrap(True)
		gridlayout.addWidget(text,0,0,1,2)
		
		text.setText(self.tr("User")+' <b>'+unicode(name)+'</b> '+self.tr("added you to his/her roster."))
		item.setText(1,"0"+unicode(name).lower())
		self.setItemWidget(item,0,widget)
		
		action=QtGui.QAction(self.tr("Ok"),widget)
		action.item=item
		ok.setDefaultAction(action)
		QtCore.QObject.connect(ok, QtCore.SIGNAL("triggered ( QAction *)"),self.subscribedAccepted)
		if self.main.palette["roster"].has_key("added"):
			if len(self.main.palette["roster"]["added"])!=0:
				color=QtGui.QColor(self.main.palette["roster"]["added"])
				if self.main.palette["roster"].has_key("addedAlpha"):
					if len(self.main.palette["roster"]["addedAlpha"])!=0:
						color.setAlpha(int(self.main.palette["roster"]["addedAlpha"]))
				item.setBackgroundColor(0,color)
				item.setBackgroundColor(3,color)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		return item

	def subscribedAccepted(self,action):
		self.takeTopLevelItem(self.indexOfTopLevelItem(action.item))

	def addSubscription(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		widget=subscriptionWidget(self)
		widget.ui.text.setText(self.tr("User")+' <b>'+unicode(name)+'</b> '+self.tr("wants to add you to his/her roster. <b>Add him/her?</b>"))
		item.setText(1,"0"+unicode(name).lower())
		self.setItemWidget(item,0,widget)
		widget2=QtGui.QWidget(self)
		action=QtGui.QAction(self.tr("Yes"),widget.ui.add)
		action.item=item
		widget.ui.add.setDefaultAction(action)
		action=QtGui.QAction(self.tr("No"),widget.ui.delete)
		action.item=item
		widget.ui.delete.setDefaultAction(action)
		action=QtGui.QAction(self.tr("Get VCard"),widget.ui.vcard)
		action.item=item
		widget.ui.vcard.setDefaultAction(action)
		QtCore.QObject.connect(widget.ui.add, QtCore.SIGNAL("triggered ( QAction *)"),self.subscriptionAccepted)
		QtCore.QObject.connect(widget.ui.delete, QtCore.SIGNAL("triggered ( QAction *)"),self.subscriptionRejected)
		QtCore.QObject.connect(widget.ui.vcard, QtCore.SIGNAL("triggered ( QAction *)"),self.showVCard)
		self.setItemWidget(item,3,widget2)
		if self.main.palette["roster"].has_key("add"):
			if len(self.main.palette["roster"]["add"])!=0:
				color=QtGui.QColor(self.main.palette["roster"]["add"])
				if self.main.palette["roster"].has_key("addAlpha"):
					if len(self.main.palette["roster"]["addAlpha"])!=0:
						color.setAlpha(int(self.main.palette["roster"]["addAlpha"]))
				item.setBackgroundColor(0,color)
				item.setBackgroundColor(3,color)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		return item

	def showVCard(self,action):
		jid=unicode(action.item.text(1))[1:]
		self.jab.getVCard(jid)
		
	def subscriptionAccepted(self,action):
		jid=unicode(action.item.text(1))[1:]
		self.takeTopLevelItem(self.indexOfTopLevelItem(action.item))
		win=addContactWindow(self.main,self.jab,self,jid,jid)
		ret=win.exec_()
		if ret:
			self.jab.roster.Authorize(jid)
		else:
			self.jab.roster.Unauthorize(jid)

	def subscriptionRejected(self,action):
		jid=unicode(action.item.text(1))[1:]
		self.takeTopLevelItem(self.indexOfTopLevelItem(action.item))
		self.jab.roster.Unauthorize(jid)

	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"1"+unicode(name).lower())
		item.setText(2,name)
		item.setIcon(0,QtGui.QIcon("images/32x32/icons/group-closed.png"))
		# Palette colors
		if self.main.palette["roster"].has_key("group"):
			if len(self.main.palette["roster"]["group"])!=0:
				item.setBackgroundColor(0,QtGui.QColor(self.main.palette["roster"]["group"]))
				item.setBackgroundColor(3,QtGui.QColor(self.main.palette["roster"]["group"]))
		if self.main.palette["roster"].has_key("groupText"):
			if len(self.main.palette["roster"]["groupText"])!=0:
				item.setTextColor(0,QtGui.QColor(self.main.palette["roster"]["groupText"]))
				item.setTextColor(3,QtGui.QColor(self.main.palette["roster"]["groupText"]))
		return item

	def addUser(self,jid,name,group,offline,icon):
		# add new user to the roster and resturn QTreeWidgetItem
		if group==None:
			item=QtGui.QTreeWidgetItem(self)
		else:
			item=QtGui.QTreeWidgetItem(group)
		# if we get no name, we can use jid as name
		if name==None or len(name)==0:
			name=jid
		# item data
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant(jid))
		item.setIcon(0,icon)
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		# item design
		self.setItemHidden(item, offline)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()
		return item

	def addResource(self,jid,name,user):
		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant(jid))
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		return item

	def editItem(self):
		# Edit contact name
		item=self.currentItem()
		name,b=QtGui.QInputDialog.getText(self,self.tr("Edit contact"),self.tr("Enter new contact nickname"), QtGui.QLineEdit.Normal, "")
		name=unicode(name)
		jid=item.data(32,0)
		jid=str(jid.toString())
		if b==True:
			self.jab.roster.setItem(jid,name,self.getGroups(jid))
			for user in self.getUsers(jid):
				user.setText(0,name)
				user.setText(2,name)

	def buildContactMenu(self,jid,group):
		# build contact menu
		contactMenu=QtGui.QMenu(self)
		# chat
		action=contactMenu.addAction(self.tr("Chat"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("chat")
		# send file
		action=contactMenu.addAction(self.tr("Send file"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("send_file")
		# separator
		contactMenu.addSeparator()
		# vcard
		action=contactMenu.addAction(self.tr("vCard"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("vcard")
		# get avatar
		action=contactMenu.addAction(self.tr("Get avatar"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("avatar")
		# separator
		contactMenu.addSeparator()
		# delete from group
		if group!=None and len(self.getGroups(str(jid)))>1:
			action=contactMenu.addAction(self.tr("Delete from group"))
			action.setData(QtCore.QVariant([unicode(jid),u"-"+group.text(2)]))
			action.setObjectName("check_group")
		# delete from roster
		action=contactMenu.addAction(self.tr("Delete from roster"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("delete_action")
		# separator
		contactMenu.addSeparator()
		# groups -> submenu
		group=contactMenu.addMenu (self.tr("Groups"))
		# groups -> new group
		action=group.addAction(self.tr("New Group"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("new_group")
		# groups -> separator
		group.addSeparator()
		# groups -> groups list
		g=self.getGroups(str(jid))
		for k,v in self.main.groups.iteritems():
			action=group.addAction(unicode(k))
			action.setObjectName("check_group")
			action.setCheckable(True)
			if k in g:
				action.setChecked(True)
				action.setData(QtCore.QVariant([unicode(jid),u"-"+unicode(k)]))
			else:
				action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu

	def buildGroupMenu(self,group):
		# build contact menu
		contactMenu=QtGui.QMenu(self)
		# chat
		action=contactMenu.addAction(self.tr("Get avatars"))
		action.setData(QtCore.QVariant(group))
		action.setObjectName("get_avatars")
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu


	def mimeTypes(self):
		# set mimetypes, which we accept
		return QtCore.QStringList("text/plain")

	def startDrag(self,actions):
		# start dragging selected contact
		item=self.currentItem()
		data=item.data(32,0)
		data=str(data.toString())
		self.drag=QtGui.QDrag(self)
		mimeData=QtCore.QMimeData()
		mimeData.setText(data)
		self.drag.setMimeData(mimeData)
		self.dropAction = self.drag.start(QtCore.Qt.CopyAction)

	def dropMimeData(self,parent, index, data, action ):
		# drop data => change group for dropped contact
		jid=str(data.text())
		if self.isGroupItem(parent):
			name=unicode(self.getUsers(jid)[0].text(2))
			self.changeGroup(jid,name,"+",unicode(parent.text(2)))
			return True
		else:
			return False
	
	def paintEvent(self,event):
		# paintEvent handler
		# paint roster background texture
		if self.pixmap!=None:
			viewport=self.viewport()
			painter=QtGui.QPainter(viewport)
			for x in range(int(int(viewport.width())//self.pixmap.width())+1):
				for y in range(int(int(viewport.height())/self.pixmap.height())+1):
					painter.drawPixmap(x*int(self.pixmap.width()),y*self.pixmap.height(),self.pixmap)
		QtGui.QTreeWidget.paintEvent(self,event)
	
	def changeGroup(self,jid,name,action,group):
		# change group for contact
		if action=="+":
			# add contact to the group, if he isn't there
			if not self.main.groups[group]["users"].has_key(str(jid)):
				item=self.getUsers(jid)[0].clone() # clone contact item
				self.main.groups[group]["item"].addChild(item) # add item to the new group
				# copy resources
				resources=list(self.getResources(str(jid)))
				self.main.groups[group]["users"][str(jid)]={"item":item,"resources":resources}
				# send jabber command
				self.jab.roster.setItem(jid,name,self.getGroups(jid)+[unicode(group)])
		else:
			# delete contact
			user=self.main.groups[group]["users"][str(jid)]
			self.delUser(jid,user["item"])
			groups=self.getGroups(jid)
			# send jabber command
			self.jab.roster.setItem(jid,name,groups)
		# refresh group stats
		self.refreshStats()
		# sort items
		self.sortItems (1,QtCore.Qt.AscendingOrder)

	def contactMenuTriggered(self,action):
		# contact menu action handler
		cmd=action.objectName()
		if cmd=="delete_action":
			# delete contact from roster
			# get contact jid
			jid=action.data()
			jid=str(jid.toString())
			print "roster_delete_action",jid
			# delete user from groups
			for user in self.getUsers(jid):
				self.delUser(jid,user)
			self.jab.roster.delItem(jid) # send jabber command
			self.refreshStats() # refresh group stats
		elif cmd=="new_group":
			# add contact to the new group
			# get contact jid
			jid=action.data()
			jid=str(jid.toString())
			name=unicode(self.getUsers(jid)[0].text(2)) # get contact name
			print "roster_new_group_action",jid,name
			# get new group name with QDialog
			group,b=QtGui.QInputDialog.getText(self,self.tr("New group"),self.tr("Add user to new group"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			# if user set new name of group
			if b==True and len(group)!=0:
				# add new group
				self.main.groups[group]={"item":self.addGroup(group),"users":{}} 
				item=self.getUsers(jid)[0].clone() # clone contact item
				# add contact to the new group
				self.main.groups[group]["users"][str(jid)]={"item":item,"resources":list(self.getResources(str(jid)))}
				self.main.groups[group]["item"].addChild(item)
				self.sortItems (1,QtCore.Qt.AscendingOrder) # sort items
				# send jabber command
				self.jab.roster.setItem(jid,name,self.getGroups(jid)+[unicode(group)])
			# refresh stats
			self.refreshStats()
		elif cmd=="check_group":
			items=action.data()
			items=items.toList()
			jid=str(items[0].toString())
			name=unicode(self.getUsers(jid)[0].text(2))
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]
			print "roster_change_group_action",jid,group
			if self.main.groups.has_key(group):
				if self.main.groups[group]['item']==self.main.groups['Unknown']['item']:
					group="Unknown"
			else:
				group="Unknown"
			# change group
			self.changeGroup(jid,name,action,group)
			# refresh stats
			self.refreshStats()
		elif cmd=="vcard":
			# get vcard of selected contact
			jid=action.data()
			jid=str(jid.toString())
			self.jab.getVCard(jid)
		elif cmd=="avatar":
			# get avatar of selected contact
			jid=action.data()
			jid=str(jid.toString())
			self.jab.getVCard(jid,True)
		elif cmd=="get_avatars":
			# get avatars of users in selected group
			group=action.data()
			group=unicode(group.toString())
			for jid,item in self.main.groups[group]["users"].iteritems():
				self.jab.getVCard(jid,True)
		elif cmd=="chat":
			# chat with selected contact
			jid=action.data()
			jid=str(jid.toString())
			user=self.getUsers(jid)[0]
			self.contactClicked(user,0)
		elif cmd=="send_file":
			# chat with selected contact
			jid=action.data()
			jid=str(jid.toString())
			jid=jid+"/"+self.getResources(jid)[0]
			file=QtGui.QFileDialog.getOpenFileName(self,"Choose file")
			if len(file)!=0:
				print file,"to",jid
				self.jab.sendFile(jid,unicode(file))


	def contextMenuEvent (self,event):
		# show contact context menu
		item=self.itemFromIndex(self.indexAt(QtCore.QPoint(event.x(),event.y())))
		group=item.parent()
		data=item.data(32,0)
		data=data.toString()
		if self.isUser(data):
			contactMenu=self.buildContactMenu(str(data),group)
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()
		else:
			contactMenu=self.buildGroupMenu(unicode(item.text(2)))
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()
