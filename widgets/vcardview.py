import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from vcardview_ui import *
import base64

class vcardViewDialog(QtGui.QDialog):
	def __init__(self,main,data,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_vcardView()
		self.ui.setupUi(self)
		self.main=main
		print data
		text=""
		if data.has_key("GIVEN"):
			text+="<b>"+self.tr("Name: ")+"</b>"+data['GIVEN']+"<br/>"
		if data.has_key("FAMILY"):
			text+="<b>"+self.tr("Surname: ")+"</b>"+data['FAMILY']+"<br/>"
		if data.has_key("USERID"):
			text+="<b>"+self.tr("JID: ")+"</b>"+data['USERID']+"<br/>"
		if data.has_key("HOME-LOCALITY"):
			text+="<b>"+self.tr("Locality: ")+"</b>"+data["HOME-LOCALITY"]+"<br/>"
		if data.has_key("HOME-CTRY"):
			text+="<b>"+self.tr("Country: ")+"</b>"+data['HOME-CTRY']+"<br/>"
		if data.has_key("HOME-NUMBER"):
			text+="<b>"+self.tr("Home tel. number: ")+"</b>"+data['HOME-NUMBER']+"<br/>"
		
		if data.has_key("BINVAL"):
			image=base64.decodestring(str(data["BINVAL"]))
			pixmap=QtGui.QPixmap()
			pixmap.loadFromData(image)
			pixmap=QtGui.QIcon(pixmap)
			self.ui.avatar.setPixmap(pixmap.pixmap(128,128))


		
		
		self.ui.vcard.setText(text)