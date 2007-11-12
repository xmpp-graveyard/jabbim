import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from vcardeditor_ui import *
import base64

class vcardEditorDialog(QtGui.QDialog):
	def __init__(self,main,data,parent=None,editable=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_VCardEdit()
		self.ui.setupUi(self)
		self.main=main
		self.data=data
		
		for x in self.data.elements():
			name=unicode(x.name)
			if name=="NICKNAME":
				self.ui.nickname.setText(unicode(x))
			elif name=="FN":
				self.ui.fullname.setText(unicode(x))
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
		else:
			QtCore.QObject.connect(self.ui.setAvatar, QtCore.SIGNAL("clicked()"),self.setAvatar)
	
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
		if self.editable:
			
			for x in self.data.elements():
				name=unicode(x.name)
				if name=="NICKNAME":
					x.children = []
					x.children.append(unicode(self.ui.name.text()))
					#x.addElement('value', content = unicode(widget.text()))
				elif name=="FN":
					x.children = []
					x.children.append(unicode(self.ui.fullname.text()))
				else:
					for y in x.elements():
						child=unicode(y.name)
						if name=="N" and child=="GIVEN":
							y.children = []
							y.children.append(unicode(self.ui.name.text()))
							#self.ui.name.setText(unicode(y))
						elif name=="N" and child=="FAMILY":
							y.children = []
							y.children.append(unicode(self.ui.surname.text()))
						elif name=="PHOTO" and child=="BINVAL":
							avatar=self.ui.avatar.pixmap()
							bytes=QtCore.QByteArray()
							buf=QtCore.QBuffer(bytes)
							buf.open(QtCore.QIODevice.WriteOnly)
							avatar.save(buf, "PNG")
							y.children = []
							y.children.append(base64.encodestring(str(bytes)))
			#print unicode(self.data),type(self.data)
			#print unicode(self.data.toXml())
			
			#self.data["N-GIVEN"]=unicode(self.ui.name.text())
			#self.data["N-FAMILY"]=unicode(self.ui.surname.text())
			#self.data["FN"]=unicode(self.ui.fullname.text())
			#self.data["NICKNAME"]=unicode(self.ui.nickname.text())
			#avatar=self.ui.avatar.pixmap()
			#bytes=QtCore.QByteArray()
			#buf=QtCore.QBuffer(bytes)
			#buf.open(QtCore.QIODevice.WriteOnly)
			#avatar.save(buf, "PNG")
			#self.data["PHOTO-BINVAL"]=base64.encodestring(str(bytes))
			#keys=list(self.data.keys())
			#print self.data
			#for key in keys:
				#if len(self.data[key])==0:
					#del self.data[key]
			#print self.data
			self.main.client.setVCard(self.data)
		self.done(1)