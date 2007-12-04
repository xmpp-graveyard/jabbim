import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from vcardeditor_ui import *
import base64
from twisted.words.xish.domish import Element

class vcardEditorDialog(QtGui.QDialog):
	def __init__(self,main,jid,parent=None,editable=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_VCardEdit()
		self.main=main
		if jid not in [self.main.client.jid.full(), self.main.client.jid.userhost()]:
			self.setWindowTitle(jid+" - "+self.tr("vCard"))
		else:
			self.setWindowTitle(self.tr("VCard Editor"))
		self.ui.setupUi(self)
		self.data=None

		d=self.main.client.getVCard(jid)
		d.addCallback(self.vcardArrived)
		d.addErrback(self.noVcard)
		self.ui.tabWidget.setEnabled(False)

		self.ui.avatar.setPixmap(QtGui.QPixmap())

		self.ui.avatar.setText("")
		text=""
		#if data.has_key("N-GIVEN"):
			#self.ui.name.setText(data['N-GIVEN'])
		#if data.has_key("N-FAMILY"):
			#self.ui.surname.setText(data['N-FAMILY'])
		#if data.has_key("PHOTO-BINVAL"):
			#image=base64.decodestring(str(data["PHOTO-BINVAL"]))
			#pixmap=QtGui.QPixmap()
			#pixmap.loadFromData(image)
			#pixmap=QtGui.QIcon(pixmap)
			#self.ui.avatar.setPixmap(pixmap.pixmap(128,128))
		#if data.has_key("NICKNAME"):
			#self.ui.nickname.setText(data['NICKNAME'])
		#if data.has_key("FN"):
			#self.ui.fullname.setText(data['FN'])
		#<ADR>
			#<WORK/>
			#<EXTADD>Suite 600</EXTADD>
			#<STREET>1899 Wynkoop Street</STREET>
			#<LOCALITY>Denver</LOCALITY>
			#<REGION>CO</REGION>
			#<PCODE>80202</PCODE>
			#<CTRY>USA</CTRY>
		#</ADR>
		self.editable=editable
		
		if not self.editable:
			self.ui.name.setReadOnly(True)
			self.ui.nickname.setReadOnly(True)
			self.ui.fullname.setReadOnly(True)
			self.ui.surname.setReadOnly(True)
			self.ui.pushButton.hide()
			self.ui.setAvatar.hide()
			self.ui.homeextadd.setReadOnly(True)
			self.ui.homestreet.setReadOnly(True)
			self.ui.homelocality.setReadOnly(True)
			self.ui.homecountry.setReadOnly(True)
			self.ui.homepcode.setReadOnly(True)
		else:
			QtCore.QObject.connect(self.ui.setAvatar, QtCore.SIGNAL("clicked()"),self.setAvatar)
	
	def noVcard(self,data=None):
		self.ui.download.setText(self.tr("Can't download vCard of this contact."))
	def vcardArrived(self,data):
		self.data=data
		if self.data:
			for x in self.data.elements():
				name=unicode(x.name)
				if name=="NICKNAME":
					self.ui.nickname.setText(unicode(x))
				elif name=="FN":
					self.ui.fullname.setText(unicode(x))
				elif name=="ADR":
					typ=""
					for y in x.elements():
						child=unicode(y.name)
						if child=="HOME":
							typ="HOME"
					if typ=="HOME":
						for y in x.elements():
							child=unicode(y.name)
							if child=="EXTADD":
								self.ui.homeextadd.setText(unicode(y))
							elif child=="STREET":
								self.ui.homestreet.setText(unicode(y))
							elif child=="LOCALITY":
								self.ui.homelocality.setText(unicode(y))
							elif child=="CTRY":
								self.ui.homecountry.setText(unicode(y))
							elif child=="PCODE":
								self.ui.homepcode.setText(unicode(y))
				else:
					for y in x.elements():
						child=unicode(y.name)
						if name=="N" and child=="GIVEN":
							self.ui.name.setText(unicode(y))
						elif name=="N" and child=="FAMILY":
							self.ui.surname.setText(unicode(y))
						elif name=="PHOTO" and child=="BINVAL":
							image=base64.decodestring(str(unicode(y)))
							pixmap=QtGui.QPixmap()
							pixmap.loadFromData(image)
							pixmap=QtGui.QIcon(pixmap)
							self.ui.avatar.setPixmap(pixmap.pixmap(128,128))
			self.ui.download.hide()
			self.ui.tabWidget.setEnabled(True)
		else:
			self.data = Element(('vcard-temp','vCard'))
			self.ui.download.setText(self.tr("Can't download vCard of this contact."))
			if self.editable:
				self.ui.download.hide()
				self.ui.tabWidget.setEnabled(True)
		

	def setAvatar(self):
		file=list(QtGui.QFileDialog.getOpenFileNames(self,"Choose picture"))
		if len(file)!=0:
			resized=False
			file=unicode(file[0])
			avatar=QtGui.QPixmap(file)
			print int(avatar.width()), int(avatar.height())
			if int(avatar.width())>128 or int(avatar.height())>128:
				avatar=avatar.scaled(128,128,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				resized=True
			self.ui.avatar.setPixmap(avatar)
			if resized:
				QtGui.QMessageBox.information(self,self.tr("Avatar"),self.tr("Your avatar was too big. He had to be resized to smaller size."))

	def accept(self):
		if self.editable and self.data:
			name2=unicode(self.ui.name.text())
			nickname=unicode(self.ui.nickname.text())
			fullname=unicode(self.ui.fullname.text())
			surname=unicode(self.ui.surname.text())

			homeextadd=unicode(self.ui.homeextadd.text())
			homestreet=unicode(self.ui.homestreet.text())
			homelocality=unicode(self.ui.homelocality.text())
			homecountry=unicode(self.ui.homecountry.text())
			homepcode=unicode(self.ui.homepcode.text())

			avatar=self.ui.avatar.pixmap()
			n=False
			photo=False
			homeadr=False
			for x in self.data.elements():
				name=unicode(x.name)
				if name=="NICKNAME" and nickname!=None:
					x.children = []
					x.children.append(nickname)
					nickname=None
					#x.addElement('value', content = unicode(widget.text()))
				elif name=="FN" and fullname!=None:
					x.children = []
					x.children.append(fullname)
					fullname=None

				elif name=="ADR":
					typ=""
					for y in x.elements():
						child=unicode(y.name)
						if child=="HOME":
							typ="HOME"
							homeadr=x
					if typ=="HOME":
						for y in x.elements():
							child=unicode(y.name)
							if child=="EXTADD":
								y.children = []
								y.children.append(homeextadd)
								homeextadd=None
							elif child=="STREET":
								y.children = []
								y.children.append(homestreet)
								homestreet=None
							elif child=="LOCALITY":
								y.children = []
								y.children.append(homelocality)
								homelocality=None
							elif child=="CTRY":
								y.children = []
								y.children.append(homecountry)
								homecountry=None
							elif child=="PCODE":
								y.children = []
								y.children.append(homepcode)
								homepcode=None


				else:
					for y in x.elements():
						child=unicode(y.name)
						if name=="N":
							n=x
						if name=="PHOTO":
							photo=x
						if name=="N" and child=="GIVEN" and name2!=None:
							y.children = []
							y.children.append(name2)
							name2=None
							#self.ui.name.setText(unicode(y))
						elif name=="N" and child=="FAMILY" and surname!=None:
							y.children = []
							y.children.append(surname)
							surname=None
						elif name=="PHOTO" and child=="BINVAL" and avatar!=None:
							#avatar=self.ui.avatar.pixmap()
							y.children = []
							if not avatar.isNull():
								bytes=QtCore.QByteArray()
								buf=QtCore.QBuffer(bytes)
								buf.open(QtCore.QIODevice.WriteOnly)
								avatar.save(buf, "PNG")
							
								y.children.append(base64.encodestring(str(bytes)))
							avatar=None
			if name2!=None:
				if len(name2)!=0:
					if not n:
						n=self.data.addElement('N')
					n.addElement('GIVEN', content = unicode(name2))
			if surname!=None:
				if len(surname)!=0:
					if not n:
						n=self.data.addElement('N')
					n.addElement('FAMILY', content = unicode(surname))
			if homeextadd!=None:
				if len(homeextadd)!=0:
					if not homeadr:
						homeadr=self.data.addElement('ADR')
						homeadr.addElement('HOME')
					homeadr.addElement('EXTADD', content = unicode(homeextadd))
			if homestreet!=None:
				if len(homestreet)!=0:
					if not homeadr:
						homeadr=self.data.addElement('ADR')
						homeadr.addElement('HOME')
					homeadr.addElement('STREET', content = unicode(homestreet))
			if homelocality!=None:
				if len(homelocality)!=0:
					if not homeadr:
						homeadr=self.data.addElement('ADR')
						homeadr.addElement('HOME')
					homeadr.addElement('LOCALITY', content = unicode(homelocality))
			if homecountry!=None:
				if len(homecountry)!=0:
					if not homeadr:
						homeadr=self.data.addElement('ADR')
						homeadr.addElement('HOME')
					homeadr.addElement('CTRY', content = unicode(homecountry))
			if homepcode!=None:
				if len(homepcode)!=0:
					if not homeadr:
						homeadr=self.data.addElement('ADR')
						homeadr.addElement('HOME')
					homeadr.addElement('PCODE', content = unicode(homepcode))
			if avatar!=None:
				if not avatar.isNull():
					bytes=QtCore.QByteArray()
					buf=QtCore.QBuffer(bytes)
					buf.open(QtCore.QIODevice.WriteOnly)
					avatar.save(buf, "PNG")
					if not photo:
						photo=self.data.addElement('PHOTO')
					photo.addElement('BINVAL', content = base64.encodestring(str(bytes)))
			if nickname!=None:
				if len(nickname)!=0:
					self.data.addElement('NICKNAME',content = unicode(nickname))
			if fullname!=None:
				if len(fullname)!=0:
					self.data.addElement('FN',content = unicode(fullname))

			#print unicode(self.data),type(self.data)
			#print "NEW",unicode(self.data.toXml())

			self.main.client.setVCard(self.data)
		self.done(1)
