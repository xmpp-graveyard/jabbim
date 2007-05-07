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
		self.setIconSize(QtCore.QSize(16,16))
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

	def addGroup(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		item.setText(0,name)
		item.setText(1,"1"+unicode(name).lower())
		item.setText(2,name)
		#item.setIcon(0,QtGui.QIcon("images/32x32/icons/group-closed.png"))
		item.setBackgroundColor(0,QtGui.QColor("#000000"))
		item.setBackgroundColor(3,QtGui.QColor("#000000"))
		item.setTextColor(0,QtGui.QColor("#FFFFFF"))
		item.setTextColor(3,QtGui.QColor("#FFFFFF"))
		return item
	
	def addUser(self,jid,name,group,offline=True,icon=None):
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
		#item.setIcon(0,icon)
		item.setFlags(item.flags()|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled)
		# item design
		#self.setItemHidden(item, offline)
		#self.sortItems (1,QtCore.Qt.AscendingOrder)
		#self.refreshStats()
		return item