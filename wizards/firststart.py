# -*- coding: utf-8 -*- 
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from twisted.internet import reactor
from twisted.python import log
import registration
import sys

def createFirstPage(wizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Welcome"))

	wizard.label=QtGui.QLabel(wizard.trUtf8("Vítejte ........."))
	wizard.label.setWordWrap(True)

	#label2=QtGui.QLabel(wizard.trUtf8("Jabber ID (JID) je obdoba emailové adresy. Je to Váš identifikátor v sítich jabber a ostatní uživatelé Vám na tuto adresu mohou pomocí jabberu psát."))
	#label2.setWordWrap(True)

	#wizard.label=QtGui.QLabel("")
	#wizard.label.setWordWrap(True)

	#label2=QtGui.QLabel(wizard.tr("Server je místo, kde jsou uložena Vaše uživatelská data.")
	#label2.setWordWrap(True)

	#wizard.serverLab=QtGui.QLabel()
	#wizard.jidLabel=QtGui.QLabel()

	#nicknameLabel=QtGui.QLabel(wizard.tr("Nickname:"))
	#wizard.nicknameLineEdit=QtGui.QLineEdit()
	##wizard.serverLabel=QtGui.QLabel()
	
	#passwordLabel=QtGui.QLabel(wizard.tr("Password:"))
	#passwordLineEdit=QtGui.QLineEdit()
	#passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)

	#password2Label=QtGui.QLabel(wizard.tr("Password again:"))
	#password2LineEdit=QtGui.QLineEdit()
	#password2LineEdit.setEchoMode(QtGui.QLineEdit.Password)
	
	#serverLabel=QtGui.QLabel(wizard.tr("Server:"))
	#wizard.serverComboBox=QtGui.QComboBox()
	#wizard.serverComboBox.addItems(QtCore.QStringList([wizard.tr("Choose server")]+servers))
	#wizard.serverComboBox.setEditable(True)
	#QtCore.QObject.connect(wizard.serverComboBox,QtCore.SIGNAL("activated ( const QString & )"),wizard.serverComboBoxActivated)
	#QtCore.QObject.connect(wizard.serverComboBox,QtCore.SIGNAL("editTextChanged ( const QString & )"),wizard.serverComboBoxActivated)
	#QtCore.QObject.connect(wizard.nicknameLineEdit,QtCore.SIGNAL("textEdited ( const QString & )"),wizard.nicknameChanged)
	
	wizard.newAccount=QtGui.QRadioButton(wizard.tr("Create new Jabber account"))
	wizard.newAccount.setChecked(True)
	wizard.oldAccount=QtGui.QRadioButton(wizard.tr("Use existed Jabber account"))
	
	layout=QtGui.QGridLayout()
	layout.addWidget(wizard.label,0,0,1,2)
	layout.addWidget(wizard.newAccount,1,0,1,2)
	layout.addWidget(wizard.oldAccount,2,0,1,2)
	

	
	page.registerField("newAccount",wizard.newAccount)
	page.registerField("oldAccount",wizard.oldAccount)
	page.setTitle(wizard.trUtf8("Vitejte...."))
	page.setSubTitle(wizard.trUtf8("Vyberte jednu z moznosti."))
	

	page.setLayout(layout)
	return page


def createSecondPage(wizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Welcome"))

	wizard.label=QtGui.QLabel(wizard.trUtf8("K vytvoreni noveho profilu je potreba vyplnit nasledujici formular."))
	wizard.label.setWordWrap(True)

	jidLabel=QtGui.QLabel(wizard.tr("Jabber ID:"))
	wizard.jid=QtGui.QLineEdit()

	wizard.savePassword=QtGui.QCheckBox(wizard.tr("Save password"))
	

	passwordLabel=QtGui.QLabel(wizard.tr("Password:"))
	wizard.password=QtGui.QLineEdit()
	wizard.password.setEchoMode(QtGui.QLineEdit.Password)
	wizard.password.setEnabled(False)
	QtCore.QObject.connect(wizard.savePassword,QtCore.SIGNAL("stateChanged ( int )"),wizard.password.setEnabled)

	layout=QtGui.QGridLayout()
	layout.addWidget(wizard.label,0,0,1,2)
	layout.addWidget(jidLabel,1,0,1,1)
	layout.addWidget(wizard.jid,1,1,1,1)
	layout.addWidget(wizard.savePassword,2,0,1,2)
	layout.addWidget(passwordLabel,3,0,1,1)
	layout.addWidget(wizard.password,3,1,1,1)
	
	page.registerField("jid*",wizard.jid)
	page.registerField("savePassword",wizard.savePassword)
	page.registerField("password",wizard.password)
	
	page.setTitle(wizard.trUtf8("Vitejte...."))
	page.setSubTitle(wizard.trUtf8("Prihlaseni"))
	

	page.setLayout(layout)
	return page

class firstStartWizard(QtGui.QWizard):
	def __init__(self,main,parent=None):
		apply(QtGui.QWizard.__init__,(self,parent))
		self.main=main
		self.addPage(createFirstPage(self))
		#self.addPage(createThirdPage(self))
		#self.addPage(createWaitPage(self))
		self.addPage(createSecondPage(self))
		#self.addPage(createFinishPage(self))
		self.setWindowTitle(self.tr("Add contact"))
		#self.cl=None
		#self.error=None
		#self.registered=False
		#self.jid=""


		
	def initializePage(self,i):
		##page=self.page(i)
		##print i,self.error
		##if i==2 and self.error!=None:
			##if self.error=="409":
				
			##self.error=None
		##if i==2:
			##server=servers[int(self.field("server").toString())-1]
			##self.serverLabel.setText("@"+server)
		if i==1:
			if self.newAccount.isChecked():
				self.accept()
			##server=servers[int(self.field("server").toString())-1]
			##jid=unicode(self.field("jid").toString())
			##password=unicode(self.field("password").toString())
			#j=self.jid.split("@")
			#name=j[0]
			#server=j[1]
			#password=unicode(self.field("password").toString())

			#self.cl = registrationClass(self,name,server, 'jab',password, 5222, reactor)
			##log.startLogging(sys.stdout)
			#self.cl.connect()
			#reactor.run()
		#elif i==2:
			#self.registered=True
		#elif i==3:
			#card={}
			#card["N-GIVEN"]=unicode(self.field("firstname").toString())
			#card["N-FAMILY"]=unicode(self.field("surname").toString())
			#card["EMAIL-INTERNET"]=unicode(self.field("email").toString())
			#avatar=self.avatar.pixmap()
			#if avatar:
				#bytes=QtCore.QByteArray()
				#buf=QtCore.QBuffer(bytes)
				#buf.open(QtCore.QIODevice.WriteOnly)
				#avatar.save(buf, "PNG")
				#card["PHOTO-BINVAL"]=base64.encodestring(str(bytes))
			#self.cl.setVCard(card)
		#return

	#def validateCurrentPage(self):
		#if int(self.currentId())==1:
			#if self.registered==True:
				#return True
			#else:
				#return False
		#elif int(self.currentId())==0:
			#if unicode(self.field("password").toString())==unicode(self.field("password2").toString()):
				#return True
			#else:
				#self.label.setText(self.trUtf8("Hesla nejsou stejná."))
				#return False
		#else:
			#return self.currentPage().validatePage()

	#def reject(self):
		
		#if self.cl:
			#self.cl.disconnect()
		#return QtGui.QWizard.reject(self)

	def accept(self):
		if self.newAccount.isChecked():
			self.hide()
			self.regwiz=registration.registrationWizard(self.main,None)
			self.regwiz.exec_()
		else:
			jid=unicode(self.jid.text())
			savePassword=self.savePassword.isChecked()
			password=unicode(self.password.text())
			self.main.newProfile(jid,password,savePassword)
			self.main.fillLoginForm()
		return QtGui.QWizard.accept(self)

	#def finished(self,result):
		#print "finished"
		#if self.cl:
			#self.cl.disconnect()
		#return QtGui.QWizard.finished(self,result)
