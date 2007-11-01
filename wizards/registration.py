try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

def createFirstPage(wizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Introduction"))

	label=QtGui.QLabel(wizard.tr("Choose your language and server."))
	label.setWordWrap(True)
	
	serverLabel=QtGui.QLabel(wizard.tr("Server:"))
	serverComboBox=QtGui.QComboBox()
	serverComboBox.addItems(QtCore.QStringList([wizard.tr("Choose server"),"jabbim.cz","jabbim.sk","jabbim.pl","jabbim.com","jabber.cz","njs.netlab.cz"]))
	serverComboBox.setEditable(True)
	
	layout=QtGui.QGridLayout()
	layout.addWidget(label,0,0,1,2)
	layout.addWidget(serverLabel,1,0,1,1)
	layout.addWidget(serverComboBox,1,1,1,1)
	
	page.registerField("server*",serverComboBox)
	
	page.setLayout(layout)
	return page

def createSecondPage(wizard):
	
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Email and Nickname"))

	label=QtGui.QLabel(wizard.tr("Type your email and nickname."))
	label.setWordWrap(True)
	
	nicknameLabel=QtGui.QLabel(wizard.tr("Nickname:"))
	nicknameLineEdit=QtGui.QLineEdit()
	
	emailLabel=QtGui.QLabel(wizard.tr("Email:"))
	emailLineEdit=QtGui.QLineEdit()
	
	layout=QtGui.QGridLayout()
	layout.addWidget(label,0,0,1,2)
	layout.addWidget(nicknameLabel,1,0,1,1)
	layout.addWidget(nicknameLineEdit,1,1,1,1)
	layout.addWidget(emailLabel,2,0,1,1)
	layout.addWidget(emailLineEdit,2,1,1,1)
		
	page.registerField("nickname*",nicknameLineEdit)
	page.registerField("email*",emailLineEdit)
	
	page.setLayout(layout)
	return page

class registrationWizard(QtGui.QWizard):
	def __init__(self,main,parent=None):
		apply(QtGui.QWizard.__init__,(self,parent))
		self.main=main
		self.addPage(createFirstPage(self))
		self.addPage(createSecondPage(self))
		self.setWindowTitle(self.tr("Registration Wizard"))