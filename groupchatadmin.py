try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from groupchatadmin_ui import *
from palette import *

class groupchatAdminWindow(QtGui.QDialog):
	def __init__(self,parent,main,jab):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.parent=parent
		self.ui=Ui_groupchatadmin()
		self.ui.setupUi(self)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		QtCore.QObject.connect(self.ui.addmoderator, QtCore.SIGNAL("clicked ()"),self.addmoderator)
		QtCore.QObject.connect(self.ui.addowner, QtCore.SIGNAL("clicked ()"),self.addowner)
		QtCore.QObject.connect(self.ui.deleteowner, QtCore.SIGNAL("clicked ()"),self.deleteowner)
		QtCore.QObject.connect(self.ui.addmember, QtCore.SIGNAL("clicked ()"),self.addmember)
		QtCore.QObject.connect(self.ui.deletemember, QtCore.SIGNAL("clicked ()"),self.deletemember)
		QtCore.QObject.connect(self.ui.addban, QtCore.SIGNAL("clicked ()"),self.addban)
		QtCore.QObject.connect(self.ui.deleteban, QtCore.SIGNAL("clicked ()"),self.deleteban)
		#palette=loadPalette(self.main.palette["chatwindow"])
		#self.setPalette(palette)
		
	def addmoderator(self):
		jid,b=QtGui.QInputDialog.getText(self,self.tr("Add moderator"),self.tr("Enter Jabber ID of new moderator"), QtGui.QLineEdit.Normal, "")
		jid=unicode(jid)
		if b==True:
			#self.ui.moderatorlist.addItem(jid)
			items=[jid]
			#for i in range(self.ui.moderatorlist.count()):
				#item=self.ui.moderatorlist.item(i)
				#items.append(unicode(item.text()))
			self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,role="moderator")

	def addowner(self):
		jid,b=QtGui.QInputDialog.getText(self,self.tr("Add owner"),self.tr("Enter Jabber ID of new owner"), QtGui.QLineEdit.Normal, "")
		jid=unicode(jid)
		if b==True:
			#self.ui.ownerlist.addItem(jid)
			items=[jid]
			#for i in range(self.ui.ownerlist.count()):
				#item=self.ui.ownerlist.item(i)
				#items.append(unicode(item.text()))
			self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,affiliation="owner")

	def deleteowner(self):
		toDel=self.ui.ownerlist.selectedItems()[0]
		#self.ui.ownerlist.takeItem(self.ui.ownerlist.row(toDel))
		toDel=unicode(toDel.text())
		items=[]
		#for i in range(self.ui.ownerlist.count()):
			#item=self.ui.ownerlist.item(i)
			#items.append(unicode(item.text()))
		self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,affiliation="owner",toDel=[toDel,"none"])

	def addmember(self):
		jid,b=QtGui.QInputDialog.getText(self,self.tr("Add member"),self.tr("Enter Jabber ID of new member"), QtGui.QLineEdit.Normal, "")
		jid=unicode(jid)
		if b==True:
			#self.ui.ownerlist.addItem(jid)
			items=[jid]
			#for i in range(self.ui.ownerlist.count()):
				#item=self.ui.ownerlist.item(i)
				#items.append(unicode(item.text()))
			self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,affiliation="member")

	def deletemember(self):
		toDel=self.ui.memberlist.selectedItems()[0]
		#self.ui.ownerlist.takeItem(self.ui.ownerlist.row(toDel))
		toDel=unicode(toDel.text())
		items=[]
		#for i in range(self.ui.ownerlist.count()):
			#item=self.ui.ownerlist.item(i)
			#items.append(unicode(item.text()))
		self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,affiliation="member",toDel=[toDel,"none"])

	def addban(self):
		jid,b=QtGui.QInputDialog.getText(self,self.tr("Add new ban"),self.tr("Enter Jabber ID of new ban"), QtGui.QLineEdit.Normal, "")
		jid=unicode(jid)
		if b==True:
			#self.ui.ownerlist.addItem(jid)
			items=[jid]
			#for i in range(self.ui.ownerlist.count()):
				#item=self.ui.ownerlist.item(i)
				#items.append(unicode(item.text()))
			self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,affiliation="outcast")

	def deleteban(self):
		toDel=self.ui.banlist.selectedItems()[0]
		#self.ui.ownerlist.takeItem(self.ui.ownerlist.row(toDel))
		toDel=unicode(toDel.text())
		items=[]
		#for i in range(self.ui.ownerlist.count()):
			#item=self.ui.ownerlist.item(i)
			#items.append(unicode(item.text()))
		self.jab.groupchatSetAdminList(unicode(self.parent.jid),items,affiliation="outcast",toDel=[toDel,"none"])