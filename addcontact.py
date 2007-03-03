try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from addcontact_ui import *

class addContactWindow(QtGui.QDialog):
	def __init__(self,main,jab,parent=None,jid="",nickname=""):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.setModal(True)
		self.ui=Ui_addContact()
		self.ui.setupUi(self)
		self.ui.jid.setText(unicode(jid))
		self.ui.nickname.setText(unicode(nickname))
		for k,v in self.main.groups.iteritems():
			self.ui.group.addItem(unicode(k))

	def accept(self):
		jid=unicode(self.ui.jid.text())
		nickname=unicode(self.ui.nickname.text())
		group=unicode(self.ui.group.currentText())
		print "adding",jid,nickname,group
		addContact(jid,nickname,group,self.main,self.jab)
		self.done(1)

	def reject(self):
		self.close()

def addContact(jid,nickname,group,main,jab):
	if len(group)!=0:
		if main.groups.has_key(group):
			main.groups[group]["users"][str(jid)]={"item":main.ui.roster.addUser(jid,nickname,main.groups[group]["item"],main.offline,main.getIcon(jid,"offline")),"resources":[]}
		else:
			main.groups[group]={"item":main.ui.roster.addGroup(group),"users":{}}
			main.groups[group]["users"][str(jid)]={"item":main.ui.roster.addUser(jid,nickname,main.groups[group]["item"],main.offline,main.getIcon(jid,"offline")),"resources":[]}
	else:
		main.groups["Unknown"]["users"][str(jid)]={"item":main.ui.roster.addUser(jid,nickname,main.groups["Unknown"]["item"],main.offline,main.getIcon(jid,"offline")),"resources":[]}
	jab.roster.setItem(jid,nickname,[group])
	jab.roster.Subscribe(jid)

