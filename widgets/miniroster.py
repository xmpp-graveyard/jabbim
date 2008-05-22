import os,weakref
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from miniroster_ui import *

class miniRosterDialog(QtGui.QDialog):
	def __init__(self,main,call,multiple=False,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.ui=Ui_miniRoster()
		self.ui.setupUi(self)
		self.main=weakref.ref(main)
		self.multiple=multiple
		self.call=call
		self.ui.users.header().hide()
		if not self.multiple:
			QtCore.QObject.connect(self.ui.users,QtCore.SIGNAL("itemDoubleClicked ( QTreeWidgetItem *, int )"),self.accept)
		for group,groupItem in self.main().ui.roster.groups.iteritems():
			users=[]
			parent=QtGui.QTreeWidgetItem(self.ui.users)
			parent.setText(0,unicode(groupItem.name).replace(self.main().ui.roster.specialName,self.tr('Unknown')))
			self.ui.users.setItemExpanded(parent,True)
			for user in self.main().ui.roster.users:
				if user.group==group:
					users.append([user.name.lower(),user])
			users.sort()
			for user in users:
				item=user[1]
				child=QtGui.QTreeWidgetItem(parent)
				child.setText(0,item.name)
				child.jid=item.jid
				avatar=self.main().client.getAvatarImg(item.jid)
				if avatar:
					avatar=avatar[0]
				else:
					avatar=self.main().client.getAvatarImg(None)
					if avatar:
						avatar=avatar[0]
				avatar=avatar.scaled(22,22,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				child.setIcon(0,QtGui.QIcon(avatar))
				

	def accept(self,item=None,i=None):
		item=self.ui.users.currentItem()
		if item and item.parent()!=None:
			self.call(item.jid)
			QtGui.QDialog.accept(self)
