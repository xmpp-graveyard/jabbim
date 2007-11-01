try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

servers=["jabbim.cz","jabbim.sk","jabbim.pl","jabbim.com","jabber.cz","njs.netlab.cz"]
def createFirstPage(wizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Introduction"))

	label=QtGui.QLabel(wizard.tr("Choose your language and server."))
	label.setWordWrap(True)
	
	serverLabel=QtGui.QLabel(wizard.tr("Server:"))
	serverComboBox=QtGui.QComboBox()
	serverComboBox.addItems(QtCore.QStringList([wizard.tr("Choose server")]+servers))
	serverComboBox.setEditable(True)
	
	layout=QtGui.QGridLayout()
	layout.addWidget(label,0,0,1,2)
	layout.addWidget(serverLabel,1,0,1,1)
	layout.addWidget(serverComboBox,1,1,1,1)
	
	page.registerField("server*",serverComboBox)
	
	page.setLayout(layout)
	return page

def createWaitPage(wizard):
	
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Connecting"))

	label=QtGui.QLabel(wizard.tr("Downloading informations from server."))
	label.setWordWrap(True)
	
	layout=QtGui.QGridLayout()
	layout.addWidget(label,0,0,1,1)
	
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

def createThirdPage(wizard):
	
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("JID registration"))

	label=QtGui.QLabel(wizard.tr("Jabber ID registration."))
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
		self.addPage(createWaitPage(self))
		self.addPage(createSecondPage(self))
		self.setWindowTitle(self.tr("Registration Wizard"))
	
	def initializePage(self,i):
		#page=self.page(i)
		if i==1:
			server=servers[int(self.field("server").toString())-1]
			self.main.client.getDiscoInfo(values['jid'],callback=self._discoinfo)
			
	def _discoinfo(self,data=None):
		self.discoInfo=data
		self.next()
	