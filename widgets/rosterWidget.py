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

	def getUserItems(self,jid):
		if not self.main.client.roster['users'].has_key(jid):
			return []
		return self.main.client.roster['users'][jid].getUserItems()

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
		for item in self.getUserItems(jid):
			name=unicode(item.text(0))
			item.setText(1,self.main.shows[unicode(show)]+unicode(name).lower())
			item.setIcon(0,self.main.getIcon(size=str(self.main.config['rosterIconSize'])+"x"+str(self.main.config['rosterIconSize']),status=self.main.icons[self.main.shows[unicode(show)]]))
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		self.refreshStats()

	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"1"+unicode(name).lower())
		item.setText(2,name)
		#item.setIcon(0,QtGui.QIcon("images/16x16/icons/group-closed.png"))
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
		#self.setItemHidden(item, offline)
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