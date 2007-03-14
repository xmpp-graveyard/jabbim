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
		self.ui.fullname.hide()
		self.ui.nickname.hide()
		self.ui.famillyname.hide()
		self.ui.middlename.hide()
		self.ui.prefix.hide()
		self.ui.suffix.hide()
		self.ui.email.hide()
		self.ui.website.hide()
		self.ui.jid.hide()
		self.ui.uid.hide()
		self.ui.preferred.hide()
		self.ui.home.hide()
		self.ui.work.hide()
		self.ui.voice.hide()
		self.ui.fax.hide()
		self.ui.pager.hide()
		self.ui.messagerecorder.hide()
		self.ui.cell.hide()
		self.ui.video.hide()
		self.ui.bbs.hide()
		self.ui.modem.hide()
		self.ui.isdn.hide()
		self.ui.pcs.hide()
		self.ui.address.hide()
		self.ui.address2.hide()
		self.ui.city.hide()
		self.ui.state.hide()
		self.ui.postalcode.hide()
		self.ui.country.hide()
		self.ui.latitude.hide()
		self.ui.logitude.hide()
		self.ui.orgname.hide()
		self.ui.orgunit.hide()
		self.ui.orgtitle.hide()
		self.ui.orgrole.hide()
		self.ui.fullnamelabel.hide()
		self.ui.nicknamelabel.hide()
		self.ui.famillynamelabel.hide()
		self.ui.middlenamelabel.hide()
		self.ui.prefixlabel.hide()
		self.ui.suffixlabel.hide()
		self.ui.emaillabel.hide()
		self.ui.websitelabel.hide()
		self.ui.jidlabel.hide()
		self.ui.uidlabel.hide()
		self.ui.preferredlabel.hide()
		self.ui.homelabel.hide()
		self.ui.worklabel.hide()
		self.ui.voicelabel.hide()
		self.ui.faxlabel.hide()
		self.ui.pagerlabel.hide()
		self.ui.messagerecorderlabel.hide()
		self.ui.celllabel.hide()
		self.ui.videolabel.hide()
		self.ui.bbslabel.hide()
		self.ui.modemlabel.hide()
		self.ui.isdnlabel.hide()
		self.ui.pcslabel.hide()
		self.ui.addresslabel.hide()
		self.ui.address2label.hide()
		self.ui.citylabel.hide()
		self.ui.statelabel.hide()
		self.ui.postalcodelabel.hide()
		self.ui.countrylabel.hide()
		self.ui.latitudelabel.hide()
		self.ui.logitudelabel.hide()
		self.ui.orgnamelabel.hide()
		self.ui.orgunitlabel.hide()
		self.ui.orgtitlelabel.hide()
		self.ui.orgrolelabel.hide()
		#print vcard
		for k,v in vcard.iteritems():
			if k!="PHOTO":
				print k,v
			if k=="URL":
				self.ui.website.setText(unicode(v))
				self.ui.website.show()
				self.ui.websitelabel.show()
			elif k=="NICKNAME":
				self.ui.nickname.setText(unicode(v))
				self.ui.nickname.show()
				self.ui.nicknamelabel.show()
			elif k=="FN":
				self.ui.fullname.setText(unicode(v))
				self.ui.fullname.show()
				self.ui.fullnamelabel.show()
			elif k=="DESC":
				self.ui.about.setText(unicode(v))
				self.ui.about.show()
				self.ui.aboutlabel.show()
			elif k=="EMAIL":
				if v.has_key("USERID"):
					self.ui.email.setText(unicode(v["USERID"]))
					self.ui.email.show()
					self.ui.emaillabel.show()
			elif k=="TEL":
				if v.has_key("NUMBER"):
					self.ui.home.setText(unicode(v["NUMBER"]))
					self.ui.home.show()
					self.ui.homelabel.show()
			elif k=="BDAY":
				self.ui.birthday.setText(unicode(v))
				self.ui.birthday.show()
				self.ui.birthdaylabel.show()
			elif k=="N":
				if v.has_key("GIVEN"):
					self.ui.name.setText(unicode(v["GIVEN"]))
					self.ui.name.show()
					self.ui.namelabel.show()
				if v.has_key("FAMILLY"):
					self.ui.famillyname.setText(unicode(v["FAMILLY"]))
					self.ui.famillyname.show()
					self.ui.famillynamelabel.show()
			elif k=="PHOTO":
				if v.has_key("BINVAL"):
					pixmap=QtGui.QPixmap()
					image=base64.decodestring(str(v["BINVAL"]))
					pixmap.loadFromData(image)
					self.ui.photo.setPixmap(pixmap)
