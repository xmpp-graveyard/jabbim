# -*- coding: utf-8 -*- 
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from twisted.internet import reactor
from twisted.python import log
import registration
import sys

def createFirstPage(firstStartWizard):
	# language and server
	page=QtGui.QWizardPage(firstStartWizard)
	page.setTitle(firstStartWizard.tr("Welcome"))

	firstStartWizard.label=QtGui.QLabel(firstStartWizard.trUtf8("Vítejte ........."),page)
	firstStartWizard.label.setWordWrap(True)
	policy=firstStartWizard.label.sizePolicy()
	policy.setHeightForWidth(True)
	policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
	firstStartWizard.label.setSizePolicy(policy)
	#firstStartWizard.label.setMinimumHeight(firstStartWizard.label.sizeHint().height())
	firstStartWizard.newAccount=QtGui.QRadioButton(firstStartWizard.tr("Create new Jabber account"))
	firstStartWizard.newAccount.setChecked(True)
	firstStartWizard.oldAccount=QtGui.QRadioButton(firstStartWizard.tr("Use existing Jabber account"))
	
	layout=QtGui.QGridLayout(page)
	layout.addWidget(firstStartWizard.label,0,0,1,2)
	layout.addWidget(firstStartWizard.newAccount,1,0,1,2)
	layout.addWidget(firstStartWizard.oldAccount,2,0,1,2)
	

	
	page.registerField("newAccount",firstStartWizard.newAccount)
	page.registerField("oldAccount",firstStartWizard.oldAccount)
	page.setTitle(firstStartWizard.trUtf8("Vitejte...."))
	page.setSubTitle(firstStartWizard.trUtf8("Vyberte jednu z moznosti."))
	
	page.setLayout(layout)
	return page


def createSecondPage(firstStartWizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(firstStartWizard.tr("Welcome"))

	firstStartWizard.label=QtGui.QLabel(firstStartWizard.trUtf8("K vytvoreni noveho profilu je potreba vyplnit nasledujici formular."))
	firstStartWizard.label.setWordWrap(True)
	policy=firstStartWizard.label.sizePolicy()
	policy.setHeightForWidth(True)
	policy.setVerticalPolicy(QtGui.QSizePolicy.Minimum)
	firstStartWizard.label.setSizePolicy(policy)

	jidLabel=QtGui.QLabel(firstStartWizard.tr("Jabber ID:"))
	firstStartWizard.jid=QtGui.QLineEdit()

	firstStartWizard.savePassword=QtGui.QCheckBox(firstStartWizard.tr("Save password"))
	

	passwordLabel=QtGui.QLabel(firstStartWizard.tr("Password:"))
	firstStartWizard.password=QtGui.QLineEdit()
	firstStartWizard.password.setEchoMode(QtGui.QLineEdit.Password)
	firstStartWizard.password.setEnabled(False)
	QtCore.QObject.connect(firstStartWizard.savePassword,QtCore.SIGNAL("stateChanged ( int )"),firstStartWizard.password.setEnabled)

	layout=QtGui.QGridLayout()
	layout.addWidget(firstStartWizard.label,0,0,1,2)
	layout.addWidget(jidLabel,1,0,1,1)
	layout.addWidget(firstStartWizard.jid,1,1,1,1)
	layout.addWidget(firstStartWizard.savePassword,2,0,1,2)
	layout.addWidget(passwordLabel,3,0,1,1)
	layout.addWidget(firstStartWizard.password,3,1,1,1)
	
	page.registerField("jid*",firstStartWizard.jid)
	page.registerField("savePassword",firstStartWizard.savePassword)
	page.registerField("password",firstStartWizard.password)
	
	page.setTitle(firstStartWizard.trUtf8("Vitejte...."))
	page.setSubTitle(firstStartWizard.trUtf8("Prihlaseni"))
	

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
		self.setWindowTitle(self.tr("Jabbim Wizard"))
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
			self.regwiz=registration.registrationWizard(self.main,self.main)
			self.regwiz.setGeometry(self.geometry())
			self.regwiz.exec_()
		else:
			jid=unicode(self.jid.text())
			savePassword=self.savePassword.isChecked()
			password=unicode(self.password.text())
			self.main.newProfile(jid,password,savePassword)
			self.main.profileChanged(jid)
			
		return QtGui.QWizard.accept(self)

	#def finished(self,result):
		#print "finished"
		#if self.cl:
			#self.cl.disconnect()
		#return QtGui.QWizard.finished(self,result)
