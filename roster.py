
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from palette import *

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
		self.setIconSize(QtCore.QSize(28,28))
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
		# little hack for hidden items (we need some item at the end of roster)
		self.item=QtGui.QTreeWidgetItem(self)
		self.item.setText(1,"999")
		self.setItemHidden(self.item, True)
		# set color palette
		palette=loadPalette(self.main.palette["roster"])
		self.setPalette(palette)
		
		self.pixmap=QtGui.QPixmap("images/texture.png")

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
		self.main.chat.addChatTab(data,unicode(item.text(2)),item.icon(0))

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
		del self.main.groups[unicode(parent.text(2))]["users"][str(jid)]
		if len(self.main.groups[unicode(parent.text(2))]["users"])==0:
			del self.main.groups[unicode(parent.text(2))]

	def getGroups(self,jid):
		# get all groups where is JID jid
		groups=[]
		for k,v in self.main.groups.iteritems():
			if self.main.groups[k]["users"].has_key(jid):
				groups.append(unicode(k))
		return groups

	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"0"+unicode(name).lower())
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

	def mimeTypes(self):
		# set mimetypes, which we accept
		return QtCore.QStringList("text/plain")

	def startDrag(self,actions):
		# start dragging
		item=self.currentItem()
		data=item.data(32,0)
		data=str(data.toString())
		self.drag=QtGui.QDrag(self)
		mimeData=QtCore.QMimeData()
		mimeData.setText(data)
		self.drag.setMimeData(mimeData)
		self.dropAction = self.drag.start(QtCore.Qt.CopyAction)

	def dropMimeData(self,parent, index, data, action ):
		# drop data
		jid=str(data.text())
		print parent,data.text()
		if self.isGroupItem(parent):
			name=unicode(self.getUsers(jid)[0].text(2))
			self.changeGroup(jid,name,"+",unicode(parent.text(2)))
			return True
		else:
			return False
	
	def paintEvent(self,event):
		viewport=self.viewport()
		painter=QtGui.QPainter(viewport)
		for x in range(int(int(viewport.width())//self.pixmap.width())+1):
			for y in range(int(int(viewport.height())/self.pixmap.height())+1):
				painter.drawPixmap(x*int(self.pixmap.width()),y*self.pixmap.height(),self.pixmap)
		#painter.end()
		QtGui.QTreeWidget.paintEvent(self,event)
	
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
			self.refreshStats()
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
			self.refreshStats()
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
		elif cmd=="vcard":
			jid=action.data()
			jid=str(jid.toString())
			self.jab.getVCard(jid)
		elif cmd=="avatar":
			jid=action.data()
			jid=str(jid.toString())
			self.jab.getVCard(jid,True)
		elif cmd=="chat":
			jid=action.data()
			jid=str(jid.toString())
			user=self.getUsers(jid)[0]
			self.contactClicked(user,0)

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
