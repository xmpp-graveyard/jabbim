try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from preferences_ui import *

class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.nickname.setText(self.main.config['nickname'])
		self.ui.password.setText(self.main.config['passwd'])
		self.ui.jid.setText(self.main.config['jid'])

	def accept(self):
		jid=unicode(self.ui.jid.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		self.main.config['nickname']=nickname
		self.main.config['passwd']=password
		self.main.config['jid']=jid
		self.main.config.write()
		self.done(1)