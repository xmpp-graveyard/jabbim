try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from login_ui import *

class loginWindow(QtGui.QDialog):
	def __init__(self,main,jab,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.setModal(True)
		self.ui=Ui_login()
		self.ui.setupUi(self)
		self.ui.password.setText(self.main.config['passwd'])
		self.ui.jid.setText(self.main.config['jid'])
		if self.main.config['savePasswd']=="True":
			self.ui.savePassword.setChecked(True)

	def accept(self):
		jid=unicode(self.ui.jid.text())
		password=unicode(self.ui.password.text())
		if len(jid)!=0 and len(jid.split("@"))==2 and len(unicode(self.ui.password.text()))!=0:
			if jid!=self.main.config['jid'] or (password!=self.main.config['passwd'] and self.main.config['savePasswd']=="True") or self.main.config['savePasswd']!=str(self.ui.savePassword.isChecked()):
				ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save current login information?"),3,4)
				if ret==3:
					self.main.config['savePasswd']=self.ui.savePassword.isChecked()
					if self.ui.savePassword.isChecked()==True:
						self.main.config['passwd']=password
					else:
						self.main.config['passwd']=""
					self.main.config['jid']=jid
					self.main.config.write()
			self.jab.user=jid.split("@")[0]
			self.jab.server=jid.split("@")[1]
			self.jab.password=unicode(password)
			self.jab.connect()
			self.ui.connect.setEnabled(False)

	def reject(self):
		self.main.close()
		self.close()