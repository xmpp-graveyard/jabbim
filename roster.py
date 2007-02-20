try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

class rosterWidget(QtGui.QTreeWidget):
	def __init__(self,parent,main,jab):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.setAlternatingRowColors(True)
		self.setIconSize(QtCore.QSize(28,28))
		self.setRootIsDecorated(False)
		self.setObjectName("roster")
		self.setDragEnabled(True)
		#self.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
		self.headerItem().setText(0,QtGui.QApplication.translate("roster", "Roster", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(1,QtGui.QApplication.translate("roster", "id", None, QtGui.QApplication.UnicodeUTF8))
		self.headerItem().setText(2,QtGui.QApplication.translate("roster", "name", None, QtGui.QApplication.UnicodeUTF8))
		self.hideColumn(1)
		self.hideColumn(2)
		#app.connect(self, QtCore.SIGNAL("itemChanged ( QTreeWidgetItem *, int )"),self.itemChange)
		self.edit=0
		self.setAcceptDrops(True)
		self.dragStartPosition=None
		self.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
		self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.contactClicked)
		self.item=QtGui.QTreeWidgetItem(self)
		self.item.setText(1,"999")
		self.setItemHidden(self.item, True)

	def hidden(self,bool):
		self.setItemHidden(self.item, False)
		self.setItemHidden(self.item, True)

	def contactClicked(self,item,column):
		if self.isGroupItem(item):
			return
		data=item.data(32,0)
		data=str(data.toString())
		self.main.chat.addChatTab(data,unicode(item.text(2)),item.icon(0))

	def isUser(self,jid):
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(str(jid)):
				return True
		return False

	def getStats(self,group):
		offline=0
		online=0
		for k,user in self.main.groups[unicode(group)]["users"].iteritems():
			if int(unicode(user["item"].text(1))[0])==9:
				offline+=1
			else:
				online+=1
		return online,offline,online+offline

	def isGroupItem(self,item):
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["item"]==item:
				return True
		return False

	def getUsers(self,jid,group=False):
		users=[]
		groups={}
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				users.append(self.main.groups[k]["users"][str(jid)]["item"])
				groups[self.main.groups[k]["users"][str(jid)]["item"]]=k
		if group==True:
			return groups
		return users
	

	def getResources(self,jid):
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				return self.main.groups[k]["users"][str(jid)]["resources"]


	def delUser(self,jid,user):
		parent=user.parent()
		index=parent.indexOfChild(user)
		parent.takeChild(index)
		if int(parent.childCount())==0:
			self.takeTopLevelItem(self.indexOfTopLevelItem(parent))
		del self.main.groups[unicode(parent.text(2))]["users"][str(jid)]
		if len(self.main.groups[unicode(parent.text(2))]["users"])==0:
			del self.main.groups[unicode(parent.text(2))]

	def getGroups(self,jid):
		groups=[]
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				groups.append(unicode(k))
		return groups

	def addGroup(self,name):
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"0"+unicode(name).lower())
		item.setText(2,name)
		item.setIcon(0,QtGui.QIcon("images/status/muc_inactive.png"))
		item.setBackgroundColor(0,QtGui.QColor(102,102,102))
		#self.groups[g].setFlags(self.users[str(item)].flags()|QtCore.Qt.ItemIsDragEnabled)
		item.setTextColor(0,QtGui.QColor(255,255,255))
		#self.groups[g].setIcon(0,QtGui.QIcon("images/status/closed.png"))
		return item
	
	def refreshStats(self):
		for k,v in self.main.groups.iteritems():
			online,offline,count=self.getStats(unicode(k))
			self.main.groups[k]["item"].setText(0,unicode(self.main.groups[k]["item"].text(2))+" ("+str(online)+"/"+str(count)+")")

	def addUser(self,jid,name,group,offline,icon):
		if group==None:
			item=QtGui.QTreeWidgetItem(self)
		else:
			item=QtGui.QTreeWidgetItem(group)
		if name==None or len(name)==0:
			name=jid
		#item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant(jid))
		item.setIcon(0,icon)
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		item.label=QtGui.QLabel(unicode(name),self)
		self.setItemWidget(item,0,item.label)
		self.setItemHidden(item, offline)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()
		return item

	def addResource(self,jid,name,user):
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant(jid))
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
				groups=[unicode(parent.text(2))]
			self.jab.roster.setItem(jid,unicode(item.text(0)),groups)

	#def itemEdit(self):
		#self.edit=self.currentItem()
		#self.editItem(self.currentItem(),0)

	def buildContactMenu(self,jid,group):
		contactMenu=QtGui.QMenu(self)
		contactMenu.addAction(self.tr("Chat"))
		contactMenu.addSeparator()

		if group!=None and len(self.getGroups(str(jid)))>1:
			action=contactMenu.addAction(self.tr("Delete from group"))
			action.setData(QtCore.QVariant([unicode(jid),u"-"+group.text(2)]))
			action.setObjectName("check_group")
		#elif len(self.getGroups(str(jid)))>1:
			#action=contactMenu.addAction(self.tr("Delete from group"))
			#action.setData(QtCore.QVariant([unicode(jid),u"-Unknown"]))
			#action.setObjectName("check_group")
			
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
		for k,v in self.main.groups.iteritems():
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
			name=unicode(self.getUsers(jid)[0].text(2))
			self.changeGroup(jid,name,"+",unicode(parent.text(2)))
			return True
		else:
			return False

	def changeGroup(self,jid,name,action,group):
		if action=="+":
			if not self.main.groups[group]["users"].has_key(str(jid)):
				item=self.getUsers(jid)[0].clone()
				#if group!="Unknown":
					#self.main.groups[group]["item"].addChild(item)
				#else:
				self.main.groups[group]["item"].addChild(item)
				resources=list(self.getResources(str(jid)))
				print resources
				self.main.groups[group]["users"][str(jid)]={"item":item,"resources":resources}
				#self.main.groups[group]["users"][str(jid)]["resources"]=
				self.jab.roster.setItem(jid,name,self.getGroups(jid)+[unicode(group)])
		else:
			user=self.main.groups[group]["users"][str(jid)]
			self.delUser(jid,user["item"])
			groups=self.getGroups(jid)
			print groups
			self.jab.roster.setItem(jid,name,groups)
		self.refreshStats()
		self.sortItems (1,QtCore.Qt.AscendingOrder)

	def contactMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="delete_action":
			jid=action.data()
			jid=str(jid.toString())
			print "roster_delete_action",jid
			for user in self.getUsers(jid):
				self.delUser(jid,user)
			self.jab.roster.delItem(jid)
		elif cmd=="new_group":
			jid=action.data()
			jid=str(jid.toString())
			name=unicode(self.getUsers(jid)[0].text(2))
			print "roster_new_group_action",jid,name
			group,b=QtGui.QInputDialog.getText(self,self.tr("New group"),self.tr("Add user to new group"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			if b==True:
				self.main.groups[group]={"item":self.addGroup(group),"users":{}}
				item=self.getUsers(jid)[0].clone()
				print list(self.getResources(str(jid)))
				self.main.groups[group]["users"][str(jid)]={"item":item,"resources":list(self.getResources(str(jid)))}
				self.main.groups[group]["item"].addChild(item)
				
				self.sortItems (1,QtCore.Qt.AscendingOrder)
				self.jab.roster.setItem(jid,name,self.getGroups(jid)+[unicode(group)])
		elif cmd=="check_group":
			items=action.data()
			items=items.toList()
			jid=str(items[0].toString())
			name=unicode(self.getUsers(jid)[0].text(2))
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]
			print "roster_change_group_action",jid,group
			self.changeGroup(jid,name,action,group)
		self.refreshStats()

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
