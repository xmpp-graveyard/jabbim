try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from addcontact_ui import *

class addContactWindow(QtGui.QDialog):
	def __init__(self,main,jab,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.setModal(True)
		self.ui=Ui_addContact()
		self.ui.setupUi(self)
		for k,v in self.main.groups.iteritems():
			self.ui.group.addItem(unicode(k))

	def accept(self):
		jid=unicode(self.ui.jid.text())
		nickname=unicode(self.ui.nickname.text())
		group=unicode(self.ui.group.currentText())
		print "adding",jid,nickname,group
		if len(group)!=0:
			if self.main.groups.has_key(group):
				self.main.groups[group]["users"][str(jid)]=self.main.ui.roster.addUser(jid,nickname,self.main.groups[group]["item"],self.main.offline,self.main.statuses["offline"])
			else:
				self.main.groups[group]={"item":self.main.ui.roster.addGroup(group),"users":{}}
				self.main.groups[group]["users"][str(jid)]=self.main.ui.roster.addUser(jid,nickname,self.main.groups[group]["item"],self.main.offline,self.main.statuses["offline"])
		else:
			self.main.groups["Unknown"]["users"][str(jid)]=self.main.ui.roster.addUser(jid,nickname,None,self.main.offline,self.main.statuses["offline"])
		self.jab.roster.setItem(jid,nickname,[group])
		self.jab.roster.Subscribe(jid)
		self.done(1)

	def reject(self):
		self.close()