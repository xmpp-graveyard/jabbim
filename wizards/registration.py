# -*- coding: utf-8 -*- 
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from twisted.internet import reactor
from pyxl import register
from twisted.python import log
import sys
from include import rot13


servers=["jabbim.cz","jabbim.sk","jabbim.pl","jabbim.com","jabber.cz","njs.netlab.cz"]
def createFirstPage(wizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Introduction"))

	#label=QtGui.QLabel(wizard.tr("Choose your language and server."))
	#label.setWordWrap(True)
	
	serverLabel=QtGui.QLabel(wizard.tr("Server:"))
	serverComboBox=QtGui.QComboBox()
	serverComboBox.addItems(QtCore.QStringList([wizard.tr("Choose server")]+servers))
	serverComboBox.setEditable(True)
	
	layout=QtGui.QGridLayout()
	#layout.addWidget(label,0,0,1,2)
	layout.addWidget(serverLabel,0,0,1,1)
	layout.addWidget(serverComboBox,0,1,1,1)
	
	page.registerField("server*",serverComboBox)
	page.setTitle(wizard.trUtf8("Registrace Jabber účtu"))
	page.setSubTitle(wizard.trUtf8("Vyberte server, na kterém chcete účet zaregistrovat."))

	page.setLayout(layout)
	return page

def createWaitPage(wizard):
	
	page=QtGui.QWizardPage()
	page.setTitle(wizard.trUtf8("Registrace Jabber účtu"))
	page.setSubTitle(wizard.trUtf8("Právě probíhá registrace Vašeho účtu. Prosím vyčkejte."))
	#label=QtGui.QLabel(wizard.tr("Registering your account."))
	#label.setWordWrap(True)
	
	#layout=QtGui.QGridLayout()
	#layout.addWidget(label,0,0,1,1)
	
	#page.setLayout(layout)
	return page

def createFinishPage(wizard):
	
	page=QtGui.QWizardPage()
	page.setTitle(wizard.trUtf8("Registrace Jabber účtu"))
	page.setSubTitle(wizard.trUtf8("Vaše registrace byla úspěšně dokončena."))

	#label=QtGui.QLabel(wizard.tr("Your account is registered."))
	#label.setWordWrap(True)
	
	#layout=QtGui.QGridLayout()
	#layout.addWidget(label,0,0,1,1)
	
	#page.setLayout(layout)
	return page

def createSecondPage(wizard):
	
	page=QtGui.QWizardPage()
	#page.setTitle(wizard.tr("Email and Nickname"))
	page.setTitle(wizard.trUtf8("Registrace Jabber účtu"))
	page.setSubTitle(wizard.trUtf8("Zadejte Váš email a Vaši přezdívku."))
	label=QtGui.QLabel("")
	label.setWordWrap(True)
	
	nicknameLabel=QtGui.QLabel(wizard.tr("Nickname:"))
	nicknameLineEdit=QtGui.QLineEdit()
	
	emailLabel=QtGui.QLabel(wizard.tr("Email:"))
	emailLineEdit=QtGui.QLineEdit()
	emailLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(([0-9]{1,3})|([a-zA-Z]{2,3})|(aero|coop|info|museum|name))$"),emailLineEdit))
	
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
	#page.setTitle(wizard.tr("JID registration"))
	page.setTitle(wizard.trUtf8("Registrace Jabber účtu"))
	page.setSubTitle(wizard.trUtf8("Vyberte si Jabber ID a napište heslo k Vašemu budoucímu účtu."))

	wizard.label=QtGui.QLabel("")
	wizard.label.setWordWrap(True)
	
	jidLabel=QtGui.QLabel(wizard.tr("JID:"))
	jidLineEdit=QtGui.QLineEdit()
	wizard.serverLabel=QtGui.QLabel()
	
	passwordLabel=QtGui.QLabel(wizard.tr("Password:"))
	passwordLineEdit=QtGui.QLineEdit()
	passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
	
	layout=QtGui.QGridLayout()
	layout.addWidget(wizard.label,0,0,1,3)
	layout.addWidget(jidLabel,1,0,1,1)
	layout.addWidget(jidLineEdit,1,1,1,1)
	layout.addWidget(wizard.serverLabel,1,2,1,1)
	layout.addWidget(passwordLabel,2,0,1,1)
	layout.addWidget(passwordLineEdit,2,1,1,2)
		
	page.registerField("jid*",jidLineEdit)
	page.registerField("password*",passwordLineEdit)
	
	page.setLayout(layout)
	return page

class registrationClass(register.RegisteringClient):
	def __init__(self,main, username, server, resource,password, port, reactor):
		register.RegisteringClient.__init__(self, username, server, resource,password, port, reactor)
		self.main=main

	def _regfailed(self, el):
		for x in el.elements():
			#print unicode(x.toXml())
			if unicode(x.name)=="error":
				if x.hasAttribute("code"):
					if x['code']=="409":
						print "nickname conflict"
						self.main.error="409"
						self.main.label.setTextFormat(QtCore.Qt.RichText)
						self.main.label.setText(self.main.tr("<b>This Jabber ID is already registered by someone else.</b>"))
						self.main.back()
	def _authd(self, el):
		self.main.next()

class registrationWizard(QtGui.QWizard):
	def __init__(self,main,parent=None):
		apply(QtGui.QWizard.__init__,(self,parent))
		self.main=main
		self.addPage(createFirstPage(self))
		self.addPage(createSecondPage(self))
		self.addPage(createThirdPage(self))
		self.addPage(createWaitPage(self))
		self.addPage(createFinishPage(self))
		self.setWindowTitle(self.tr("Registration Wizard"))
		self.cl=None
		self.error=None
		self.registered=False
	
	def initializePage(self,i):
		#page=self.page(i)
		#print i,self.error
		#if i==2 and self.error!=None:
			#if self.error=="409":
				
			#self.error=None
		if i==2:
			server=servers[int(self.field("server").toString())-1]
			self.serverLabel.setText("@"+server)
		elif i==3:
			server=servers[int(self.field("server").toString())-1]
			jid=unicode(self.field("jid").toString())
			password=unicode(self.field("password").toString())

			self.cl = registrationClass(self,jid,server, 'jab',password, 5222, reactor)
			#log.startLogging(sys.stdout)
			self.cl.connect()
			reactor.run()
		elif i==4:
			self.registered=True
		return
	
	def reject(self):
		
		if self.cl:
			self.cl.disconnect()
		return QtGui.QWizard.reject(self)

	def accept(self):
		if self.registered:
			server=servers[int(self.field("server").toString())-1]
			name=unicode(self.field("jid").toString())
			password=unicode(self.field("password").toString())
			
			self.main.config['passwd']=rot13.scramble(password)
			self.main.config['jid']=name+"@"+server
			self.main.config['savePasswd']="True"
			self.main.fillLoginForm()
		if self.cl:
			self.cl.disconnect()
		return QtGui.QWizard.accept(self)

	def finished(self,result):
		print "finished"
		if self.cl:
			self.cl.disconnect()
		return QtGui.QWizard.finished(self,result)