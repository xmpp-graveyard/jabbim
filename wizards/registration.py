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
from twisted.words.xish import domish
from twisted.words.xish.domish import Element
##from twisted.internet import reactor, address
from twisted.words.protocols.jabber.xmlstream import IQ
import base64

servers=["jabbim.cz","jabbim.sk","jabbim.pl","jabbim.com","jabber.cz","njs.netlab.cz"]
def createFirstPage(wizard):
	# language and server
	page=QtGui.QWizardPage()
	page.setTitle(wizard.tr("Introduction"))

	label=QtGui.QLabel(wizard.trUtf8("Server je místo, kde jsou uložena Vaše uživatelská data."))
	label.setWordWrap(True)

	label2=QtGui.QLabel(wizard.trUtf8("Jabber ID (JID) je obdoba emailové adresy. Je to Váš identifikátor v sítich jabber a ostatní uživatelé Vám na tuto adresu mohou pomocí jabberu psát."))
	label2.setWordWrap(True)

	wizard.label=QtGui.QLabel("")
	wizard.label.setWordWrap(True)

	#label2=QtGui.QLabel(wizard.tr("Server je místo, kde jsou uložena Vaše uživatelská data.")
	#label2.setWordWrap(True)

	#wizard.serverLab=QtGui.QLabel()
	wizard.jidLabel=QtGui.QLabel()

	nicknameLabel=QtGui.QLabel(wizard.tr("Nickname:"))
	wizard.nicknameLineEdit=QtGui.QLineEdit()
	#wizard.serverLabel=QtGui.QLabel()
	
	passwordLabel=QtGui.QLabel(wizard.tr("Password:"))
	passwordLineEdit=QtGui.QLineEdit()
	passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)

	password2Label=QtGui.QLabel(wizard.tr("Password again:"))
	password2LineEdit=QtGui.QLineEdit()
	password2LineEdit.setEchoMode(QtGui.QLineEdit.Password)
	
	serverLabel=QtGui.QLabel(wizard.tr("Server:"))
	wizard.serverComboBox=QtGui.QComboBox()
	wizard.serverComboBox.addItems(QtCore.QStringList([wizard.tr("Choose server")]+servers))
	wizard.serverComboBox.setEditable(True)
	QtCore.QObject.connect(wizard.serverComboBox,QtCore.SIGNAL("activated ( const QString & )"),wizard.serverComboBoxActivated)
	QtCore.QObject.connect(wizard.nicknameLineEdit,QtCore.SIGNAL("textEdited ( const QString & )"),wizard.nicknameChanged)
	
	layout=QtGui.QGridLayout()
	layout.addWidget(wizard.label,0,0,1,2)
	layout.addWidget(label,1,0,1,2)
	layout.addWidget(serverLabel,2,0,1,1)
	layout.addWidget(wizard.serverComboBox,2,1,1,1)
	layout.addWidget(nicknameLabel,3,0,1,1)
	layout.addWidget(wizard.nicknameLineEdit,3,1,1,1)
	layout.addWidget(passwordLabel,4,0,1,1)
	layout.addWidget(passwordLineEdit,4,1,1,1)
	layout.addWidget(password2Label,5,0,1,1)
	layout.addWidget(password2LineEdit,5,1,1,1)
	layout.addWidget(label2,6,0,1,2)
	layout.addWidget(QtGui.QLabel(wizard.trUtf8("Vaše Jabber ID:")),7,0,1,1)
	layout.addWidget(wizard.jidLabel,7,1,1,1)
	
	page.registerField("server*",wizard.serverComboBox)
	page.registerField("nickname*",wizard.nicknameLineEdit)
	page.registerField("password*",passwordLineEdit)
	page.registerField("password2*",password2LineEdit)
	page.setTitle(wizard.trUtf8("Registrace Jabber účtu"))
	page.setSubTitle(wizard.trUtf8("Vyberte server, na kterém chcete účet zaregistrovat a Svoji přezdívku."))
	

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
	page.setSubTitle(wizard.trUtf8("Váš účet byl zaregistrován. Nyní stačí jen vyplnit informace o Vás."))
	
	firstnameLabel=QtGui.QLabel(wizard.tr("Firstname:"))
	firstnameLineEdit=QtGui.QLineEdit()
	
	surnameLabel=QtGui.QLabel(wizard.tr("Surname:"))
	surnameLineEdit=QtGui.QLineEdit()
	
	emailLabel=QtGui.QLabel(wizard.tr("Email:"))
	emailLineEdit=QtGui.QLineEdit()
	emailLineEdit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[_a-zA-Z0-9-]+(\.[_a-zA-Z0-9-]+)*@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.(([0-9]{1,3})|([a-zA-Z]{2,3})|(aero|coop|info|museum|name))$"),emailLineEdit))
	
	avatarLabel=QtGui.QLabel(wizard.tr("Avatar:"))
	wizard.avatar=QtGui.QLabel("")
	button=QtGui.QPushButton(wizard.tr("Open"))
	QtCore.QObject.connect(button,QtCore.SIGNAL("clicked()"),wizard.setAvatar)
	
	layout=QtGui.QGridLayout()
	#layout.addWidget(label,0,0,1,2)
	layout.addWidget(firstnameLabel,1,0,1,1)
	layout.addWidget(firstnameLineEdit,1,1,1,2)
	layout.addWidget(surnameLabel,2,0,1,1)
	layout.addWidget(surnameLineEdit,2,1,1,2)
	layout.addWidget(emailLabel,3,0,1,1)
	layout.addWidget(emailLineEdit,3,1,1,2)
	layout.addWidget(avatarLabel,4,0,1,1)
	layout.addWidget(wizard.avatar,4,1,1,1)
	layout.addWidget(button,4,2,1,1)
		
	page.registerField("firstname*",firstnameLineEdit)
	page.registerField("surname*",surnameLineEdit)
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
						self.main.registered=False
						self.main.back()
	def _authd(self, el):
		self.main.registered=True
		self.main.next()

	def setVCard(self, card):
		""" Posle vlastni vcard """
#		log.msg( 'requesting vcard for ' + unicode(jid))
		iq = IQ(self.xmlstream, 'set')
#		iq['to'] = jid
		vcard = iq.addElement('vCard', 'vcard-temp')
		for k,v in card.iteritems():
			s = k.split('-')
			if len(s)>1:
				found = False
				for el in vcard.elements():
					if el.name == s[0]:
						el.addElement(s[1], content = v)
						found = True
						break
				if not found:
					el = vcard.addElement(s[0])
					el.addElement(s[1], content = v)
			else:
				el = vcard.addElement(k, content = v)
				
					
		#self.disp(iq['id'])
		iq.timeout = 60
		d = iq.send()
		log.msg("END: setVCard")
		#self.main.next()
		#return d


class registrationWizard(QtGui.QWizard):
	def __init__(self,main,parent=None):
		apply(QtGui.QWizard.__init__,(self,parent))
		self.main=main
		self.addPage(createFirstPage(self))
		#self.addPage(createThirdPage(self))
		self.addPage(createWaitPage(self))
		self.addPage(createSecondPage(self))
		self.addPage(createFinishPage(self))
		self.setWindowTitle(self.tr("Registration Wizard"))
		self.cl=None
		self.error=None
		self.registered=False
		self.jid=""

	def setAvatar(self):
		file=list(QtGui.QFileDialog.getOpenFileNames(self,self.tr("Choose avatar")))
		if len(file)!=0:
			resized=False
			file=unicode(file[0])
			avatar=QtGui.QPixmap(file)
			print int(avatar.width()), int(avatar.height())
			if int(avatar.width())>128 or int(avatar.height())>128:
				avatar=avatar.scaled(128,128,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				resized=True
			self.avatar.setPixmap(avatar)
			if resized:
				QtGui.QMessageBox.information(self,self.tr("Avatar"),self.tr("Your avatar was too big. He had to be resized to smaller size."))


	def nicknameChanged(self,nickname):
		self.jid=nickname+"@"+self.serverComboBox.currentText()
		self.jidLabel.setText(self.jid)

	def serverComboBoxActivated(self,server):
		server=unicode(server)
		nickname=unicode(self.field("nickname").toString())
		self.jid=nickname+"@"+server
		self.jidLabel.setText(self.jid)
		
		
	def initializePage(self,i):
		#page=self.page(i)
		#print i,self.error
		#if i==2 and self.error!=None:
			#if self.error=="409":
				
			#self.error=None
		#if i==2:
			#server=servers[int(self.field("server").toString())-1]
			#self.serverLabel.setText("@"+server)
		if i==1:
			#server=servers[int(self.field("server").toString())-1]
			#jid=unicode(self.field("jid").toString())
			#password=unicode(self.field("password").toString())
			j=self.jid.split("@")
			name=j[0]
			server=j[1]
			password=unicode(self.field("password").toString())

			self.cl = registrationClass(self,name,server, 'jab',password, 5222, reactor)
			#log.startLogging(sys.stdout)
			self.cl.connect()
			reactor.run()
		elif i==2:
			self.registered=True
		elif i==3:
			card={}
			card["N-GIVEN"]=unicode(self.field("firstname").toString())
			card["N-FAMILY"]=unicode(self.field("surname").toString())
			card["EMAIL-INTERNET"]=unicode(self.field("email").toString())
			avatar=self.avatar.pixmap()
			if avatar:
				bytes=QtCore.QByteArray()
				buf=QtCore.QBuffer(bytes)
				buf.open(QtCore.QIODevice.WriteOnly)
				avatar.save(buf, "PNG")
				card["PHOTO-BINVAL"]=base64.encodestring(str(bytes))
			self.cl.setVCard(card)
		return

	def validateCurrentPage(self):
		if int(self.currentId())==1:
			if self.registered==True:
				return True
			else:
				return False
		elif int(self.currentId())==0:
			if unicode(self.field("password").toString())==unicode(self.field("password2").toString()):
				return True
			else:
				self.label.setText(self.trUtf8("Hesla nejsou stejná."))
				return False
		else:
			return self.currentPage().validatePage()

	def reject(self):
		
		if self.cl:
			self.cl.disconnect()
		return QtGui.QWizard.reject(self)

	def accept(self):
		if self.registered:
			j=self.jid.split("@")
			name=j[0]
			server=j[1]
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
