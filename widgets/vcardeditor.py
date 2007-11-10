import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from vcardeditor_ui import *
import base64

class vcardEditorDialog(QtGui.QDialog):
	def __init__(self,main,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_VCardEdit()
		self.ui.setupUi(self)
		self.main=main
		self.data=data
		print data
		self.ui.avatar.setText("")
		text=""
		if data.has_key("N-GIVEN"):
			self.ui.name.setText(data['N-GIVEN'])
		if data.has_key("N-FAMILY"):
			self.ui.surname.setText(data['N-FAMILY'])
		if data.has_key("PHOTO-BINVAL"):
			image=base64.decodestring(str(data["PHOTO-BINVAL"]))
			pixmap=QtGui.QPixmap()
			pixmap.loadFromData(image)
			pixmap=QtGui.QIcon(pixmap)

			self.ui.avatar.setPixmap(pixmap.pixmap(128,128))

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
		self.data["N-GIVEN"]=unicode(self.ui.name.text())
		self.data["N-FAMILY"]=unicode(self.ui.surname.text())
		avatar=self.ui.avatar.pixmap()
		bytes=QtCore.QByteArray()
		buf=QtCore.QBuffer(bytes)
		buf.open(QtCore.QIODevice.WriteOnly)
		avatar.save(buf, "PNG")
		self.data["PHOTO-BINVAL"]=base64.encodestring(str(bytes))
		keys=list(self.data.keys())
		for key in keys:
			if len(self.data[key])==0:
				del self.data[key]
		self.main.client.setVCard(self.data)
		self.done(1)