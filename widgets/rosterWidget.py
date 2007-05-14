import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from tooltip_ui import *

class delegate(QtGui.QItemDelegate):
	def __init__(self,parent=None):
		apply(QtGui.QItemDelegate.__init__,(self,parent))
		
	def paint(self,painter,option, index):
		r=QtCore.QRect(QtCore.QPoint(0, 0), option.rect.size())
		if unicode(index.data(QtCore.Qt.BackgroundRole).toString())=="#000000":
			painter.save()
			painter.translate(option.rect.topLeft())
			painter.fillRect(r,QtGui.QBrush(QtGui.QColor(index.data(QtCore.Qt.BackgroundRole).toString())))
			#drawBackground(painter, option, index);
			painter.restore()

		#print option.state
		if option.state & QtGui.QStyle.State_Selected:
			painter.save()
			painter.translate(option.rect.topLeft())
			painter.fillRect(r,option.palette.highlight())
			#drawBackground(painter, option, index);
			painter.restore()


		if not index.data(QtCore.Qt.DecorationRole).isNull():
			icon=QtGui.QIcon(index.data(QtCore.Qt.DecorationRole))
			painter.save()
			painter.translate(option.rect.topLeft())
			icon.paint(painter,0,0,16,16)
			painter.restore()

		
		doc=QtGui.QTextDocument()
		doc.setHtml(index.data().toString())
		painter.save()
		rect=option.rect.topLeft()
		rect.setX(rect.x()+20)
		painter.translate(rect)
		
		doc.drawContents(painter, QtCore.QRectF(QtCore.QRect(QtCore.QPoint(0, 0), option.rect.size())))
		#print "test"
		painter.restore()
		#drawFocus(painter, option, option.rect)

	
	def sizeHint(self,option,index):

		doc=QtGui.QTextDocument()
		doc.setHtml(index.data().toString())
		return doc.size().toSize()

		
		#QWidget *Delegate::createEditor(QWidget *parent, const QStyleOptionViewItem &/*option*/, const QModelIndex &/*index*/) const
		#{
		#return new QTextEdit(parent);
		#}
		
		#void Delegate::setEditorData(QWidget *editor, const QModelIndex &index) const
		#{
		#String value=index.data(Qt::DisplayRole).toString();
		#QTextEdit *te=static_cast<QTextEdit*>(editor);
		#te.setHtml(value);
		#}
		
		#def setModelData(editor,model,index):

			#QTextEdit *te=static_cast<QTextEdit*>(editor);
			#model.setData(index, te.toHtml());  
		
		
	def updateEditorGeometry(self,editor,option,index):

		editor.setGeometry(option.rect)



class tooltipWidget(QtGui.QWidget):
	def __init__(self,main,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.setMouseTracking (True)
		self.main=main
		self.ui=Ui_tooltipwidget()
		self.ui.setupUi(self)
		self.ui.gridlayout.setMargin(0)
		self.ui.gridlayout.setSpacing(0)
		self.setWindowFlags(QtCore.Qt.Popup)
		self.setPalette(QtGui.QToolTip.palette())
	def enterEvent(self,event):
		self.hide()

class rosterWidget(QtGui.QTreeWidget):
	def __init__(self,parent,main):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.setObjectName("roster")
		self.delegate=delegate()
		print self.itemDelegate()
		print self.delegate
		self.setItemDelegate(self.delegate)
		print self.itemDelegate()
		# main variables
		self.main=main # mainwindow pointer
		#self.jab=jab # jab instance pointer
		self.edit=0 # temp variable for tabPressed()
		# roster config and design informations
		self.setAlternatingRowColors(True)
		size=unicode(self.main.config['rosterIconSize']).rsplit("x")
		self.setIconSize(QtCore.QSize(int(size[0]),int(size[1])))
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

		self.tooltip=tooltipWidget(self.main)
		self.timer=QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout ()"),self.tooltip.hide)


		QtCore.QObject.connect(self, QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem * , int )"),self.contactClicked)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemExpanded ( QTreeWidgetItem * )"),self.expanded)
		QtCore.QObject.connect(self, QtCore.SIGNAL("itemCollapsed ( QTreeWidgetItem * )"),self.collapsed)

		self.dnd={}

	def expanded(self,item):
		# change icon if group item expanded
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-open.png"))

	def collapsed(self,item):
		# change icon if group item collapsed
		if item.parent()==None:
			item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))


	def contactClicked(self,item,column):
		# open chat window for clicked contact
		if self.main.client.roster['groups'].has_key(unicode(item.text(2))):
			return
		it=item.data(32,0)
		it=it.toList()
		data=str(it[0].toString())
		self.main.chat.addChatTab(data,unicode(item.text(2)),self.main.getIcon(data,self.main.icons[unicode(item.text(1))[0]],size="16x16"))

	def addMetaContact(self,jid,name,user):
		#item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)

		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("meta")]))
		self.sortItems(1,QtCore.Qt.AscendingOrder)
		return item


	def addResource(self,jid,name,user):
		#item=self.ui.roster.addResource(jid+'/'+resource,unicode(user.text(2))+" - "+resource,user)

		# add new resource called 'name', JID 'jid' with QTreeWidgetItem 'user'
		item=QtGui.QTreeWidgetItem(user)
		if name==None or len(name)==0:
			name=jid
		item.setText(0,unicode(name))
		item.setText(1,"9"+unicode(name).lower())
		item.setText(2,unicode(name))
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("resource")]))
		self.sortItems(1,QtCore.Qt.AscendingOrder)
		return item

	def startDrag(self,actions):
		# start dragging selected contact
		item=self.currentItem()
		it=item.data(32,0)
		it=it.toList()
		data=str(it[0].toString())
		self.drag=QtGui.QDrag(self)
		mimeData=QtCore.QMimeData()
		mimeData.setText(data)
		self.dnd[data]=item.parent()
		self.drag.setMimeData(mimeData)
		self.action=self.drag.start(QtCore.Qt.CopyAction)

	def dropMimeData(self,parent, index, data, action ):
		# drop data => change group for dropped contact
		jid=str(data.text())
		oldParent=self.dnd[jid]
		del self.dnd[jid]
		if parent in self.main.client.roster['groups'].values():
			#name=unicode(self.main.client.roster['users'][jid].rosterItems[0].text(2))
			#QString QInputDialog::getItem ( QWidget * parent, const QString & title, const QString & label, const QStringList & list, int current = 0, bool editable = true, bool * ok = 0, Qt::WindowFlags f = 0 )   [static]
			items=QtCore.QStringList()
			items.append(self.tr("Copy"))
			items.append(self.tr("Move"))
			q,b=QtGui.QInputDialog.getItem(self,self.tr("Copy/Move contact"),self.tr("Copy or move?"), items,0,False)
			q=unicode(q)
			# if user set new name of group
			if b==True and len(q)!=0:
				index=int(items.indexOf(QtCore.QRegExp(q)))
				print index
				if index==0:
					self.changeGroup(jid,"+",unicode(parent.text(2)))
				else:
					name=unicode(self.main.client.roster['users'][jid].name)
					contact=self.main.client.roster['users'][jid]
					g=contact.groups
					g.remove(unicode(oldParent.text(2)))
					self.main.client.sendRosterUpdate(contact.jid, name, contact.subscription,g+[unicode(parent.text(2))])

			return True
		else:
			return False

	def mimeTypes(self):
		# set mimetypes, which we accept
		return QtCore.QStringList("text/plain")

	def getUserItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return []
		return self.main.client.roster['users'][jid].getUserItems()

	def getResourceItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return {}
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
			self.main.client.roster['groups'][group].setText(0,"<font color=\"#FFFFFF\">"+unicode(self.main.client.roster['groups'][group].text(2))+" ("+str(online)+"/"+str(online+offline)+")</font>")

	def setStatus(self,jid,show,i=None,status=None):
		if not self.main.shows.has_key(show):
			if len(self.main.client.roster['users'][jid].status)!=0:
				if len(self.main.client.roster['users'][jid].status)>1:
					show=self.main.client.roster['users'][jid].status[0]
				else:
					show=self.main.client.roster['users'][jid].status
			else:
				show="online"

		#print i
		if i!=None:
			item=i
			name=unicode(item.text(0))
			item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
			item.setIcon(0,self.main.getIcon(jid,size=str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
			if self.main.shows[unicode(show)]!="9":
				self.setItemHidden(item, False)
		else:
			for item in self.getUserItems(jid):
				name=unicode(item.text(0))
				if status!=None:
					item.setText(0,unicode(item.text(2))+"<br/><font size=\"-1\"><i>&nbsp;&nbsp;"+status+"</i></font>")
				item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
				item.setIcon(0,self.main.getIcon(jid,size=str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
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
				item.setText(1,"9"+self.main.shows[unicode(show)]+unicode(name).lower())
				item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
			#if self.main.shows[unicode(show)]!="9":
				#self.setItemHidden(item, False)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		#self.refreshStats()


	def addSubGroup(self,name,sub,first="1"):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(sub)
		item.setText(0,name)
		item.setText(1,first+unicode(name).lower())
		item.setText(2,name)
		#item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))
		#item.setBackgroundColor(0,QtGui.QColor("#000000"))
		#item.setBackgroundColor(3,QtGui.QColor("#000000"))
		#item.setTextColor(0,QtGui.QColor("#FFFFFF"))
		#item.setTextColor(3,QtGui.QColor("#FFFFFF"))
		return item


	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,'<font color="#FFFFFF">'+name+"</font>")
		item.setText(1,"1"+unicode(name).lower())
		item.setText(2,name)
		item.setIcon(0,QtGui.QIcon("images/"+self.main.config['rosterIconSize']+"/icons/group-closed.png"))
		item.setBackgroundColor(0,QtGui.QColor("#000000"))
		item.setBackgroundColor(3,QtGui.QColor("#000000"))
		#item.setTextColor(0,QtGui.QColor("#FFFFFF"))
		#item.setTextColor(3,QtGui.QColor("#FFFFFF"))
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
		item.setData(32,0,QtCore.QVariant([unicode(jid),unicode("contact")]))
		item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize']),status=self.main.icons["9"]))
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		# item design
		if len(self.main.client.roster['users'][jid].status)!=0:
			if len(self.main.client.roster['users'][jid].status)>1:
				show=self.main.client.roster['users'][jid].status[0]
			else:
				show=self.main.client.roster['users'][jid].status
		else:
			show="offline"
		if unicode(item.text(1))[0]=='9':
			self.setItemHidden(item, offline)
		self.setStatus(jid,show)

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
		# groups . submenu
		group=contactMenu.addMenu (self.tr("Groups"))
		# groups . new group
		action=group.addAction(self.tr("New Group"))
		action.setData(QtCore.QVariant(jid))
		action.setObjectName("new_group")
		# groups . separator
		group.addSeparator()
		# groups . groups list
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
			action=unicode(items[1].toString())[0]
			group=unicode(items[1].toString())[1:]

			#if self.main.groups.has_key(group):
				#if self.main.groups[group]['item']==self.main.groups['Unknown']['item']:
					#group="Unknown"
			#else:
				#group="Unknown"
			self.changeGroup(jid,action,group)
			
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
			user=self.getUserItems(jid)[0]
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

	def changeGroup(self,jid,action,group):
			name=unicode(self.main.client.roster['users'][jid].name)
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


	def contextMenuEvent (self,event):
		# show contact context menu
		item=self.itemFromIndex(self.indexAt(QtCore.QPoint(event.x(),event.y())))
		group=item.parent()
		it=item.data(32,0)
		it=it.toList()
		jid=str(it[0].toString())
		if self.main.client.roster['users'].has_key(jid):
			contactMenu=self.buildContactMenu(str(jid),group)
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()
		else:
			contactMenu=self.buildGroupMenu(unicode(item.text(2)))
			contactMenu.move(event.globalX(),event.globalY())
			contactMenu.show()


	def viewportEvent(self,event):
		if event.type()==QtCore.QEvent.ToolTip:# and self.tooltip.isHidden():
			item=self.itemAt(int(event.x()),int(event.y()))
			if item!=None:
				if item.parent()!=None:
					it=item.data(32,0)
					it=it.toList()
					jid=str(it[0].toString())
					typ=str(it[1].toString())
					if typ=="contact":
						message=self.main.client.roster['users'][jid].status[1]
						#if os.path.isfile(self.main.homeDir+'/.jabbim/avatars/'+jid):
							#pixmap=QtGui.QPixmap()
							#f=open(self.main.homeDir+'/.jabbim/avatars/'+jid,"rb")
							#image=f.read()
							#f.close()
							#pixmap.loadFromData(image)
							#if pixmap.isNull():
								#self.tooltip.ui.icon.hide()
							#else:
								#self.tooltip.ui.icon.show()
								#self.tooltip.ui.icon.setPixmap(pixmap.scaled(64,64,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
						#else:
						self.tooltip.ui.icon.hide()
						self.tooltip.ui.jid.setText(jid)
						self.tooltip.ui.status.setText(self.main.status[self.main.icons[unicode(item.text(1))[0]]])
						if message!=None:
							if len(message)==0:
								self.tooltip.ui.message.hide()
							else:
								self.tooltip.ui.message.show()
								self.tooltip.ui.message.setText(message.replace("\n","<br/>"))
						else:
							self.tooltip.ui.message.hide()
						self.tooltip.adjustSize()
						if int(event.y())+20+int(self.tooltip.height())>int(self.height()):
							self.tooltip.move(self.mapToGlobal(QtCore.QPoint(0,event.y()-10-int(self.tooltip.height()))))
						else:
							self.tooltip.move(self.mapToGlobal(QtCore.QPoint(0,event.y()+20)))
						
						self.tooltip.show()
						self.timer.start(3000)
		return QtGui.QTreeWidget.viewportEvent(self,event)