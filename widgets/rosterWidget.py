import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

class rosterWidget(QtGui.QTreeWidget):
	def __init__(self,parent,main):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.setObjectName("roster")
		# main variables
		self.main=main # mainwindow pointer
		#self.jab=jab # jab instance pointer
		self.edit=0 # temp variable for tabPressed()
		# roster config and design informations
		self.setAlternatingRowColors(True)
		self.setIconSize(QtCore.QSize(int(self.main.config['rosterIconSize']),int(self.main.config['rosterIconSize'])))
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
		self.headerItem().setText(4,QtGui.QApplication.translate("roster", "", None, QtGui.QApplication.UnicodeUTF8))
		self.hideColumn(1)
		self.hideColumn(2)
		self.hideColumn(4)
		self.item=QtGui.QTreeWidgetItem(self)
		self.item.setText(1,"999")
		self.setItemHidden(self.item, True)

		QtCore.QObject.connect(self, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.contactClicked)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemExpanded ( QTreeWidgetItem * )"),self.expanded)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemCollapsed ( QTreeWidgetItem * )"),self.collapsed)


	def expanded(self,item):
		# change icon if group item expanded
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"x"+self.main.config['rosterIconSize']+"/icons/group-open.png"))

	def collapsed(self,item):
		# change icon if group item collapsed
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"x"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))


	def contactClicked(self,item,column):
		# open chat window for clicked contact
		if self.main.client.roster['groups'].has_key(unicode(item.text(2))):
			return
		data=item.data(32,0) # get jid
		data=str(data.toString())
		self.main.chat.addChatTab(data,unicode(item.text(2)),self.main.getIcon(data,self.main.icons[unicode(item.text(1))[0]],size="16x16"))

	def addResource(self,jid,name,user):
		#item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)

		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant(jid))
		self.sortItems(1,QtCore.Qt.AscendingOrder)
		return item


	def getUserItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return []
		return self.main.client.roster['users'][jid].getUserItems()

	def getResourceItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return []
		return self.main.client.roster['users'][jid].resourcesItems


	def hidden(self,bool):
		# little hack (qt doesn't repaint reshown items, when we have not one top level item at the end)
		self.setItemHidden(self.item, False)
		self.setItemHidden(self.item, True)


	def refreshStats(self):
		# rewrite online/all users stats in group QTreeWidgetItem
		for group,item in self.main.client.roster['groups'].iteritems():
			# return stats (online,offline,all users) for group
			offline=0
			online=0
			for i in range(int(item.childCount())):
				if int(unicode(item.child(i).text(1))[0])==9:
					offline+=1
				else:
					online+=1
			self.main.client.roster['groups'][group].setText(0,unicode(self.main.client.roster['groups'][group].text(2))+" ("+str(online)+"/"+str(online+offline)+")")

	def setStatus(self,jid,show):
		if not self.main.shows.has_key(show):
			show="online"
		for item in self.getUserItems(jid):
			name=unicode(item.text(0))
			item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
			item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize'])+"x"+str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
			if self.main.shows[unicode(show)]!="9":
				self.setItemHidden(item, False)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()

	def setResourceStatus(self,jid,resource,show):
		if not self.main.shows.has_key(show):
			show="online"
		#for item in self.getResourceItems(jid):
		if self.main.client.roster['users'].has_key(jid):
			if self.main.client.roster['users'][jid].resourcesItems.has_key(resource):
				item=self.main.client.roster['users'][jid].resourcesItems[resource]
				name=unicode(item.text(0))
				item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
				item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize'])+"x"+str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
			#if self.main.shows[unicode(show)]!="9":
				#self.setItemHidden(item, False)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		#self.refreshStats()


	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"1"+unicode(name).lower())
		item.setText(2,name)
		item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"x"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))
		item.setBackgroundColor(0,QtGui.QColor("#000000"))
		item.setBackgroundColor(3,QtGui.QColor("#000000"))
		item.setTextColor(0,QtGui.QColor("#FFFFFF"))
		item.setTextColor(3,QtGui.QColor("#FFFFFF"))
		return item
	
	def addUser(self,jid,name,group,offline=True):
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
		item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize'])+"x"+str(self.main.config['rosterIconSize']),status=self.main.icons["9"]))
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		# item design
		self.setItemHidden(item, offline)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()
		return item
		
	def resizeEvent(self,event):
		# when we resize roster, we need to resize columns too, because of avatar.
		QtGui.QTreeWidget.resizeEvent(self,event)
		if self.verticalScrollBar().isVisible():
			self.setColumnWidth(0,int(self.width())-50)
		else:
			self.setColumnWidth(0,int(self.width())-38)
		#self.tooltip.setMaximumWidth(self.width())
		#self.tooltip.setMinimumWidth(self.width())
		
	def buildContactMenu(self,jid,group):
		# build contact menu
		contactMenu=QtGui.QMenu(self)
		# chat
		action=contactMenu.addAction(self.tr("Chat"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("chat")
		# separator
		contactMenu.addSeparator()
		# vcard
		action=contactMenu.addAction(self.tr("vCard"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("vcard")
		# separator
		contactMenu.addSeparator()
		# delete from group
		if group!=None and len(self.main.client.roster['users'][jid].groups)>1:
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
		#g=self.getGroups(str(jid))
		for k,v in self.main.client.roster['groups'].iteritems():
			if k!="Unknown":
				action=group.addAction(unicode(k))
				action.setObjectName("check_group")
				action.setCheckable(True)
			#if len(self.main.client.roster['users'][jid].groups)==0:
				#if k=="Unknown":
					#action.setChecked(True)
					#action.setData(QtCore.QVariant([unicode(jid),u"-"+unicode(k)]))
				#else:
					#action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))
			#else:
				if k in self.main.client.roster['users'][jid].groups:
					action.setChecked(True)
					action.setData(QtCore.QVariant([unicode(jid),u"-"+unicode(k)]))
				else:
					action.setData(QtCore.QVariant([unicode(jid),u"+"+unicode(k)]))
		# signal
		contactMenu.connect(contactMenu, QtCore.SIGNAL("triggered ( QAction * )"),self.contactMenuTriggered)
		return contactMenu

	def contactMenuTriggered(self,action):
		# contact menu action handler
		cmd=action.objectName()
		if cmd=="delete_action":
			print "delete_action"
			## delete contact from roster
			## get contact jid
			#jid=action.data()
			#jid=str(jid.toString())
			#print "roster_delete_action",jid
			## delete user from groups
			#for user in self.getUsers(jid):
				#self.delUser(jid,user)
			#QtGui.QApplication.postEvent(self.jab,customEvent(["roster_del_item",jid]))
			##self.jab.roster.delItem(jid) # send jabber command
			#self.refreshStats() # refresh group stats
		elif cmd=="new_group":
			# add contact to the new group
			# get contact jid
			jid=action.data()
			jid=str(jid.toString())
			name=unicode(self.main.client.roster['users'][jid].name)
			print "roster_new_group_action",jid,name
			# get new group name with QDialog
			group,b=QtGui.QInputDialog.getText(self,self.tr("New group"),self.tr("Add user to new group"), QtGui.QLineEdit.Normal, "")
			group=unicode(group)
			# if user set new name of group
			if b==True and len(group)!=0:
				# add new group
				contact=self.main.client.roster['users'][jid]
				self.main.client.sendRosterUpdate(contact.jid, contact.name, contact.subscription, self.main.client.roster['users'][jid].groups+[group])
		elif cmd=="check_group":
			items=action.data()
			items=items.toList()
			jid=str(items[0].toString())
			name=unicode(self.main.client.roster['users'][jid].name)
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]

			#if self.main.groups.has_key(group):
				#if self.main.groups[group]['item']==self.main.groups['Unknown']['item']:
					#group="Unknown"
			#else:
				#group="Unknown"


			if action=="+":
				contact=self.main.client.roster['users'][jid]
				print "adding",jid,"groups:",self.main.client.roster['users'][jid].groups+[group]
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription, self.main.client.roster['users'][jid].groups+[group])
			else:
				contact=self.main.client.roster['users'][jid]
				g=contact.groups
				g.remove(group)
				print "deleting",jid,"groups:",g,'name:',name
				self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g)

		elif cmd=="vcard":
			# get vcard of selected contact
			jid=action.data()
			jid=str(jid.toString())
			QtGui.QApplication.postEvent(self.jab,customEvent(["get_vcard",jid]))
			#self.jab.getVCard(jid)
		elif cmd=="avatar":
			# get avatar of selected contact
			jid=action.data()
			jid=str(jid.toString())
			QtGui.QApplication.postEvent(self.jab,customEvent(["get_vcard",jid]))
			#self.jab.getVCard(jid,True)
		elif cmd=="get_avatars":
			# get avatars of users in selected group
			group=action.data()
			if not self.main.groups.has_key(group):
				group="Unknown"
			for jid,item in self.main.groups[group]["users"].iteritems():
				QtGui.QApplication.postEvent(self.jab,customEvent(["get_vcard",jid]))
				#self.jab.getVCard(jid,True)
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
				#self.jab.sendFile(jid,unicode(file))

	def contextMenuEvent (self,event):
		# show contact context menu
		item=self.itemFromIndex(self.indexAt(QtCore.QPoint(event.x(),event.y())))
		group=item.parent()
		jid=item.data(32,0)
		jid=unicode(jid.toString())
		if self.main.client.roster['users'].has_key(jid):
			contactMenu=self.buildContactMenu(str(jid),group)
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()
		else:
			contactMenu=self.buildGroupMenu(unicode(item.text(2)))
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()