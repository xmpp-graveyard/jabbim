try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from vcard_ui import *
import base64

class vcardWindow(QtGui.QDialog):
	def __init__(self,parent=None,vcard=None,readonly=True):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(False)
		self.ui=Ui_vcard()
		self.ui.setupUi(self)
		#print vcard
		for k,v in vcard.iteritems():
			if k!="PHOTO":
				print k,v
			if k=="URL":
				self.ui.website.setText(unicode(v))
			elif k=="NICKNAME":
				self.ui.nickname.setText(unicode(v))
			elif k=="FN":
				self.ui.fullname.setText(unicode(v))
			elif k=="DESC":
				self.ui.about.setText(unicode(v))
			elif k=="EMAIL":
				if v.has_key("USERID"):
					self.ui.email.setText(unicode(v["USERID"]))
			elif k=="TEL":
				if v.has_key("NUMBER"):
					self.ui.home.setText(unicode(v["NUMBER"]))
			elif k=="BDAY":
				self.ui.birthday.setText(unicode(v))
			elif k=="N":
				if v.has_key("GIVEN"):
					self.ui.name.setText(unicode(v["GIVEN"]))
				if v.has_key("FAMILLY"):
					self.ui.famillyname.setText(unicode(v["FAMILLY"]))
			elif k=="PHOTO":
				if v.has_key("BINVAL"):
					pixmap=QtGui.QPixmap()
					image=base64.decodestring(str(v["BINVAL"]))
					pixmap.loadFromData(image)
					self.ui.photo.setPixmap(pixmap)
