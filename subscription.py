try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from subscription_ui import *

class subscriptionWidget(QtGui.QWidget):
	def __init__(self,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_subscriptionwidget()
		self.ui.setupUi(self)
		self.ui.gridlayout.setMargin(0)
		self.ui.gridlayout.setSpacing(0)


class infoWidget(QtGui.QTreeWidget):
	def __init__(self,parent,main,jab):
		apply(QtGui.QTreeWidget.__init__,(self,parent))
		self.setObjectName("infowidget")
		# main variables
		self.main=main # mainwindow pointer
		self.jab=jab # jab instance pointer
		self.setRootIsDecorated(False)
		self.header().hide()
		self.addSubscription("test")
		self.addSubscription("test")
		self.addSubscription("test")

	def addSubscription(self,name):
		# add new group to the roster and return group QTreeWidgetItem
		item=QtGui.QTreeWidgetItem(self)
		widget=subscriptionWidget(self)
		item.setText(1,"0"+unicode(name).lower())
		self.setItemWidget(item,0,widget)
		self.sortItems (1,QtCore.Qt.AscendingOrder)
		return item
