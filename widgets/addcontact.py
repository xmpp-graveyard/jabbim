import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from addcontact_ui import *

class addContactDialog(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_addContact()
		self.ui.setupUi(self)
		self.main=main
		for k,v in self.main.client.roster['groups'].iteritems():
			self.ui.add_group.addItem(unicode(k))
	def accept(self):
		jid=unicode(self.ui.add_jid.text())
		nickname=unicode(self.ui.add_nickname.text())
		group=unicode(self.ui.add_group.currentText())
		message=unicode(self.ui.add_message.toPlainText())
		
		self.main.client.addContact(jid,message,nickname,[group])

		self.done(1)
