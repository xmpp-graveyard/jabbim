try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from login_ui import *
from preferences import *
import socket

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
		QtCore.QObject.connect(self.ui.proxy, QtCore.SIGNAL("clicked ()"),self.proxySettings)
		if self.main.config['savePasswd']=="True":
			self.ui.savePassword.setChecked(True)

	def proxySettings(self):
		win=preferencesWindow(self.main,self,0)
		win.show()

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
			user=jid.split("@")[0]
			server=jid.split("@")[1]
			password=unicode(password)
			if self.main.config['resource']=="":
				resource=unicode(socket.gethostname())
			else:
				resource=unicode(self.main.config["resource"])
			if self.main.config["proxy_type"]!="none":
				proxy={"type":self.main.config["proxy_type"],
								"server":self.main.config["proxy_server"],
								"user":self.main.config["proxy_user"],
								"passwd":self.main.config["proxy_passwd"],
								"port":self.main.config["proxy_port"],
								}
			else:
				proxy=None
			jabberLogin(self.jab,user,server,password,resource,proxy)
			self.ui.connect.setEnabled(False)

	def reject(self):
		self.main.close()
		self.close()

def jabberLogin(jab,user,server,password,resource,proxy):
	jab.user=user
	jab.server=server
	jab.password=password
	jab.resource=resource
	jab.proxy=proxy
	jab.start()