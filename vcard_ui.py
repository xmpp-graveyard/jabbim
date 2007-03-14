# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vcard.ui'
#
# Created: Wed Mar 14 06:18:56 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_vcard(object):
    def setupUi(self, vcard):
        vcard.setObjectName("vcard")
        vcard.resize(QtCore.QSize(QtCore.QRect(0,0,479,474).size()).expandedTo(vcard.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(vcard)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.pushButton = QtGui.QPushButton(vcard)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(431,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.tab = QtGui.QTabWidget(vcard)
        self.tab.setObjectName("tab")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout1 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.photo = QtGui.QLabel(self.groupBox)
        self.photo.setMaximumSize(QtCore.QSize(211,211))
        self.photo.setObjectName("photo")
        self.gridlayout2.addWidget(self.photo,0,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.fullnamelabel = QtGui.QLabel(self.groupBox)
        self.fullnamelabel.setObjectName("fullnamelabel")
        self.vboxlayout.addWidget(self.fullnamelabel)

        self.famillynamelabel = QtGui.QLabel(self.groupBox)
        self.famillynamelabel.setObjectName("famillynamelabel")
        self.vboxlayout.addWidget(self.famillynamelabel)

        self.namelabel = QtGui.QLabel(self.groupBox)
        self.namelabel.setObjectName("namelabel")
        self.vboxlayout.addWidget(self.namelabel)

        self.middlenamelabel = QtGui.QLabel(self.groupBox)
        self.middlenamelabel.setObjectName("middlenamelabel")
        self.vboxlayout.addWidget(self.middlenamelabel)

        self.prefixlabel = QtGui.QLabel(self.groupBox)
        self.prefixlabel.setObjectName("prefixlabel")
        self.vboxlayout.addWidget(self.prefixlabel)

        self.suffixlabel = QtGui.QLabel(self.groupBox)
        self.suffixlabel.setObjectName("suffixlabel")
        self.vboxlayout.addWidget(self.suffixlabel)

        self.nicknamelabel = QtGui.QLabel(self.groupBox)
        self.nicknamelabel.setObjectName("nicknamelabel")
        self.vboxlayout.addWidget(self.nicknamelabel)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(0)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.fullname = QtGui.QLineEdit(self.groupBox)
        self.fullname.setObjectName("fullname")
        self.vboxlayout1.addWidget(self.fullname)

        self.famillyname = QtGui.QLineEdit(self.groupBox)
        self.famillyname.setObjectName("famillyname")
        self.vboxlayout1.addWidget(self.famillyname)

        self.name = QtGui.QLineEdit(self.groupBox)
        self.name.setObjectName("name")
        self.vboxlayout1.addWidget(self.name)

        self.middlename = QtGui.QLineEdit(self.groupBox)
        self.middlename.setObjectName("middlename")
        self.vboxlayout1.addWidget(self.middlename)

        self.prefix = QtGui.QLineEdit(self.groupBox)
        self.prefix.setObjectName("prefix")
        self.vboxlayout1.addWidget(self.prefix)

        self.suffix = QtGui.QLineEdit(self.groupBox)
        self.suffix.setObjectName("suffix")
        self.vboxlayout1.addWidget(self.suffix)

        self.nickname = QtGui.QLineEdit(self.groupBox)
        self.nickname.setObjectName("nickname")
        self.vboxlayout1.addWidget(self.nickname)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout2.addLayout(self.hboxlayout,0,0,1,1)
        self.gridlayout1.addWidget(self.groupBox,0,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName("groupBox_2")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.groupBox_2)
        self.hboxlayout1.setMargin(6)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(0)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.emaillabel = QtGui.QLabel(self.groupBox_2)
        self.emaillabel.setObjectName("emaillabel")
        self.vboxlayout2.addWidget(self.emaillabel)

        self.websitelabel = QtGui.QLabel(self.groupBox_2)
        self.websitelabel.setObjectName("websitelabel")
        self.vboxlayout2.addWidget(self.websitelabel)

        self.jidlabel = QtGui.QLabel(self.groupBox_2)
        self.jidlabel.setObjectName("jidlabel")
        self.vboxlayout2.addWidget(self.jidlabel)

        self.uidlabel = QtGui.QLabel(self.groupBox_2)
        self.uidlabel.setObjectName("uidlabel")
        self.vboxlayout2.addWidget(self.uidlabel)
        self.hboxlayout2.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(0)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.email = QtGui.QLineEdit(self.groupBox_2)
        self.email.setObjectName("email")
        self.vboxlayout3.addWidget(self.email)

        self.website = QtGui.QLineEdit(self.groupBox_2)
        self.website.setObjectName("website")
        self.vboxlayout3.addWidget(self.website)

        self.jid = QtGui.QLineEdit(self.groupBox_2)
        self.jid.setObjectName("jid")
        self.vboxlayout3.addWidget(self.jid)

        self.uid = QtGui.QLineEdit(self.groupBox_2)
        self.uid.setObjectName("uid")
        self.vboxlayout3.addWidget(self.uid)
        self.hboxlayout2.addLayout(self.vboxlayout3)
        self.hboxlayout1.addLayout(self.hboxlayout2)
        self.gridlayout1.addWidget(self.groupBox_2,1,0,1,1)
        self.tab.addTab(self.tab_2,"")

        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")

        self.gridlayout3 = QtGui.QGridLayout(self.tab1)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem1,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.tab1)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout4.setMargin(6)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setMargin(0)
        self.vboxlayout5.setSpacing(2)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.preferredlabel = QtGui.QLabel(self.groupBox_3)
        self.preferredlabel.setObjectName("preferredlabel")
        self.vboxlayout5.addWidget(self.preferredlabel)

        self.homelabel = QtGui.QLabel(self.groupBox_3)
        self.homelabel.setObjectName("homelabel")
        self.vboxlayout5.addWidget(self.homelabel)

        self.worklabel = QtGui.QLabel(self.groupBox_3)
        self.worklabel.setObjectName("worklabel")
        self.vboxlayout5.addWidget(self.worklabel)

        self.voicelabel = QtGui.QLabel(self.groupBox_3)
        self.voicelabel.setObjectName("voicelabel")
        self.vboxlayout5.addWidget(self.voicelabel)

        self.faxlabel = QtGui.QLabel(self.groupBox_3)
        self.faxlabel.setObjectName("faxlabel")
        self.vboxlayout5.addWidget(self.faxlabel)

        self.pagerlabel = QtGui.QLabel(self.groupBox_3)
        self.pagerlabel.setObjectName("pagerlabel")
        self.vboxlayout5.addWidget(self.pagerlabel)

        self.messagerecorderlabel = QtGui.QLabel(self.groupBox_3)
        self.messagerecorderlabel.setObjectName("messagerecorderlabel")
        self.vboxlayout5.addWidget(self.messagerecorderlabel)

        self.celllabel = QtGui.QLabel(self.groupBox_3)
        self.celllabel.setObjectName("celllabel")
        self.vboxlayout5.addWidget(self.celllabel)

        self.videolabel = QtGui.QLabel(self.groupBox_3)
        self.videolabel.setObjectName("videolabel")
        self.vboxlayout5.addWidget(self.videolabel)

        self.bbslabel = QtGui.QLabel(self.groupBox_3)
        self.bbslabel.setObjectName("bbslabel")
        self.vboxlayout5.addWidget(self.bbslabel)

        self.modemlabel = QtGui.QLabel(self.groupBox_3)
        self.modemlabel.setObjectName("modemlabel")
        self.vboxlayout5.addWidget(self.modemlabel)

        self.isdnlabel = QtGui.QLabel(self.groupBox_3)
        self.isdnlabel.setObjectName("isdnlabel")
        self.vboxlayout5.addWidget(self.isdnlabel)

        self.pcslabel = QtGui.QLabel(self.groupBox_3)
        self.pcslabel.setObjectName("pcslabel")
        self.vboxlayout5.addWidget(self.pcslabel)
        self.hboxlayout3.addLayout(self.vboxlayout5)

        self.vboxlayout6 = QtGui.QVBoxLayout()
        self.vboxlayout6.setMargin(0)
        self.vboxlayout6.setSpacing(2)
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.preferred = QtGui.QLineEdit(self.groupBox_3)
        self.preferred.setObjectName("preferred")
        self.vboxlayout6.addWidget(self.preferred)

        self.home = QtGui.QLineEdit(self.groupBox_3)
        self.home.setObjectName("home")
        self.vboxlayout6.addWidget(self.home)

        self.work = QtGui.QLineEdit(self.groupBox_3)
        self.work.setObjectName("work")
        self.vboxlayout6.addWidget(self.work)

        self.voice = QtGui.QLineEdit(self.groupBox_3)
        self.voice.setObjectName("voice")
        self.vboxlayout6.addWidget(self.voice)

        self.fax = QtGui.QLineEdit(self.groupBox_3)
        self.fax.setObjectName("fax")
        self.vboxlayout6.addWidget(self.fax)

        self.pager = QtGui.QLineEdit(self.groupBox_3)
        self.pager.setObjectName("pager")
        self.vboxlayout6.addWidget(self.pager)

        self.messagerecorder = QtGui.QLineEdit(self.groupBox_3)
        self.messagerecorder.setObjectName("messagerecorder")
        self.vboxlayout6.addWidget(self.messagerecorder)

        self.cell = QtGui.QLineEdit(self.groupBox_3)
        self.cell.setObjectName("cell")
        self.vboxlayout6.addWidget(self.cell)

        self.video = QtGui.QLineEdit(self.groupBox_3)
        self.video.setObjectName("video")
        self.vboxlayout6.addWidget(self.video)

        self.bbs = QtGui.QLineEdit(self.groupBox_3)
        self.bbs.setObjectName("bbs")
        self.vboxlayout6.addWidget(self.bbs)

        self.modem = QtGui.QLineEdit(self.groupBox_3)
        self.modem.setObjectName("modem")
        self.vboxlayout6.addWidget(self.modem)

        self.isdn = QtGui.QLineEdit(self.groupBox_3)
        self.isdn.setObjectName("isdn")
        self.vboxlayout6.addWidget(self.isdn)

        self.pcs = QtGui.QLineEdit(self.groupBox_3)
        self.pcs.setObjectName("pcs")
        self.vboxlayout6.addWidget(self.pcs)
        self.hboxlayout3.addLayout(self.vboxlayout6)
        self.vboxlayout4.addLayout(self.hboxlayout3)
        self.gridlayout3.addWidget(self.groupBox_3,0,0,1,1)
        self.tab.addTab(self.tab1,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        spacerItem2 = QtGui.QSpacerItem(20,111,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem2,2,0,1,1)

        self.groupBox_5 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName("groupBox_5")

        self.hboxlayout4 = QtGui.QHBoxLayout(self.groupBox_5)
        self.hboxlayout4.setMargin(6)
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setMargin(0)
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.vboxlayout7 = QtGui.QVBoxLayout()
        self.vboxlayout7.setMargin(0)
        self.vboxlayout7.setSpacing(2)
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.latitudelabel = QtGui.QLabel(self.groupBox_5)
        self.latitudelabel.setObjectName("latitudelabel")
        self.vboxlayout7.addWidget(self.latitudelabel)

        self.logitudelabel = QtGui.QLabel(self.groupBox_5)
        self.logitudelabel.setObjectName("logitudelabel")
        self.vboxlayout7.addWidget(self.logitudelabel)
        self.hboxlayout5.addLayout(self.vboxlayout7)

        self.vboxlayout8 = QtGui.QVBoxLayout()
        self.vboxlayout8.setMargin(0)
        self.vboxlayout8.setSpacing(2)
        self.vboxlayout8.setObjectName("vboxlayout8")

        self.latitude = QtGui.QLineEdit(self.groupBox_5)
        self.latitude.setObjectName("latitude")
        self.vboxlayout8.addWidget(self.latitude)

        self.logitude = QtGui.QLineEdit(self.groupBox_5)
        self.logitude.setObjectName("logitude")
        self.vboxlayout8.addWidget(self.logitude)
        self.hboxlayout5.addLayout(self.vboxlayout8)
        self.hboxlayout4.addLayout(self.hboxlayout5)
        self.gridlayout4.addWidget(self.groupBox_5,1,0,1,1)

        self.groupBox_4 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_4.setObjectName("groupBox_4")

        self.vboxlayout9 = QtGui.QVBoxLayout(self.groupBox_4)
        self.vboxlayout9.setMargin(6)
        self.vboxlayout9.setSpacing(6)
        self.vboxlayout9.setObjectName("vboxlayout9")

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setMargin(0)
        self.hboxlayout6.setSpacing(6)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.vboxlayout10 = QtGui.QVBoxLayout()
        self.vboxlayout10.setMargin(0)
        self.vboxlayout10.setSpacing(2)
        self.vboxlayout10.setObjectName("vboxlayout10")

        self.addresslabel = QtGui.QLabel(self.groupBox_4)
        self.addresslabel.setObjectName("addresslabel")
        self.vboxlayout10.addWidget(self.addresslabel)

        self.address2label = QtGui.QLabel(self.groupBox_4)
        self.address2label.setObjectName("address2label")
        self.vboxlayout10.addWidget(self.address2label)

        self.citylabel = QtGui.QLabel(self.groupBox_4)
        self.citylabel.setObjectName("citylabel")
        self.vboxlayout10.addWidget(self.citylabel)

        self.statelabel = QtGui.QLabel(self.groupBox_4)
        self.statelabel.setObjectName("statelabel")
        self.vboxlayout10.addWidget(self.statelabel)

        self.postalcodelabel = QtGui.QLabel(self.groupBox_4)
        self.postalcodelabel.setObjectName("postalcodelabel")
        self.vboxlayout10.addWidget(self.postalcodelabel)

        self.countrylabel = QtGui.QLabel(self.groupBox_4)
        self.countrylabel.setObjectName("countrylabel")
        self.vboxlayout10.addWidget(self.countrylabel)
        self.hboxlayout6.addLayout(self.vboxlayout10)

        self.vboxlayout11 = QtGui.QVBoxLayout()
        self.vboxlayout11.setMargin(0)
        self.vboxlayout11.setSpacing(2)
        self.vboxlayout11.setObjectName("vboxlayout11")

        self.address = QtGui.QLineEdit(self.groupBox_4)
        self.address.setObjectName("address")
        self.vboxlayout11.addWidget(self.address)

        self.address2 = QtGui.QLineEdit(self.groupBox_4)
        self.address2.setObjectName("address2")
        self.vboxlayout11.addWidget(self.address2)

        self.city = QtGui.QLineEdit(self.groupBox_4)
        self.city.setObjectName("city")
        self.vboxlayout11.addWidget(self.city)

        self.state = QtGui.QLineEdit(self.groupBox_4)
        self.state.setObjectName("state")
        self.vboxlayout11.addWidget(self.state)

        self.postalcode = QtGui.QLineEdit(self.groupBox_4)
        self.postalcode.setObjectName("postalcode")
        self.vboxlayout11.addWidget(self.postalcode)

        self.country = QtGui.QLineEdit(self.groupBox_4)
        self.country.setObjectName("country")
        self.vboxlayout11.addWidget(self.country)
        self.hboxlayout6.addLayout(self.vboxlayout11)
        self.vboxlayout9.addLayout(self.hboxlayout6)
        self.gridlayout4.addWidget(self.groupBox_4,0,0,1,1)
        self.tab.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_5)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.groupBox_31 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_31.setObjectName("groupBox_31")

        self.vboxlayout12 = QtGui.QVBoxLayout(self.groupBox_31)
        self.vboxlayout12.setMargin(6)
        self.vboxlayout12.setSpacing(6)
        self.vboxlayout12.setObjectName("vboxlayout12")

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setMargin(0)
        self.hboxlayout7.setSpacing(6)
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.vboxlayout13 = QtGui.QVBoxLayout()
        self.vboxlayout13.setMargin(0)
        self.vboxlayout13.setSpacing(2)
        self.vboxlayout13.setObjectName("vboxlayout13")

        self.orgnamelabel = QtGui.QLabel(self.groupBox_31)
        self.orgnamelabel.setObjectName("orgnamelabel")
        self.vboxlayout13.addWidget(self.orgnamelabel)

        self.orgunitlabel = QtGui.QLabel(self.groupBox_31)
        self.orgunitlabel.setObjectName("orgunitlabel")
        self.vboxlayout13.addWidget(self.orgunitlabel)
        self.hboxlayout7.addLayout(self.vboxlayout13)

        self.vboxlayout14 = QtGui.QVBoxLayout()
        self.vboxlayout14.setMargin(0)
        self.vboxlayout14.setSpacing(2)
        self.vboxlayout14.setObjectName("vboxlayout14")

        self.orgname = QtGui.QLineEdit(self.groupBox_31)
        self.orgname.setObjectName("orgname")
        self.vboxlayout14.addWidget(self.orgname)

        self.orgunit = QtGui.QLineEdit(self.groupBox_31)
        self.orgunit.setObjectName("orgunit")
        self.vboxlayout14.addWidget(self.orgunit)
        self.hboxlayout7.addLayout(self.vboxlayout14)
        self.vboxlayout12.addLayout(self.hboxlayout7)
        self.gridlayout5.addWidget(self.groupBox_31,0,0,1,1)

        self.groupBox_28 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_28.setObjectName("groupBox_28")

        self.vboxlayout15 = QtGui.QVBoxLayout(self.groupBox_28)
        self.vboxlayout15.setMargin(6)
        self.vboxlayout15.setSpacing(6)
        self.vboxlayout15.setObjectName("vboxlayout15")

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setMargin(0)
        self.hboxlayout8.setSpacing(6)
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.vboxlayout16 = QtGui.QVBoxLayout()
        self.vboxlayout16.setMargin(0)
        self.vboxlayout16.setSpacing(2)
        self.vboxlayout16.setObjectName("vboxlayout16")

        self.orgtitlelabel = QtGui.QLabel(self.groupBox_28)
        self.orgtitlelabel.setObjectName("orgtitlelabel")
        self.vboxlayout16.addWidget(self.orgtitlelabel)

        self.orgrolelabel = QtGui.QLabel(self.groupBox_28)
        self.orgrolelabel.setObjectName("orgrolelabel")
        self.vboxlayout16.addWidget(self.orgrolelabel)
        self.hboxlayout8.addLayout(self.vboxlayout16)

        self.vboxlayout17 = QtGui.QVBoxLayout()
        self.vboxlayout17.setMargin(0)
        self.vboxlayout17.setSpacing(2)
        self.vboxlayout17.setObjectName("vboxlayout17")

        self.orgtitle = QtGui.QLineEdit(self.groupBox_28)
        self.orgtitle.setObjectName("orgtitle")
        self.vboxlayout17.addWidget(self.orgtitle)

        self.orgrole = QtGui.QLineEdit(self.groupBox_28)
        self.orgrole.setObjectName("orgrole")
        self.vboxlayout17.addWidget(self.orgrole)
        self.hboxlayout8.addLayout(self.vboxlayout17)
        self.vboxlayout15.addLayout(self.hboxlayout8)
        self.gridlayout5.addWidget(self.groupBox_28,1,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem3,2,0,1,1)
        self.tab.addTab(self.tab_5,"")

        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")

        self.gridlayout6 = QtGui.QGridLayout(self.tab_6)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.groupBox_33 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_33.setObjectName("groupBox_33")

        self.gridlayout7 = QtGui.QGridLayout(self.groupBox_33)
        self.gridlayout7.setMargin(6)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.about = QtGui.QTextEdit(self.groupBox_33)
        self.about.setObjectName("about")
        self.gridlayout7.addWidget(self.about,0,0,1,1)
        self.gridlayout6.addWidget(self.groupBox_33,1,0,1,1)

        self.groupBox_32 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_32.setObjectName("groupBox_32")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_32)
        self.gridlayout8.setMargin(6)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setMargin(0)
        self.hboxlayout9.setSpacing(6)
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.vboxlayout18 = QtGui.QVBoxLayout()
        self.vboxlayout18.setMargin(0)
        self.vboxlayout18.setSpacing(2)
        self.vboxlayout18.setObjectName("vboxlayout18")

        self.birthdaylabel = QtGui.QLabel(self.groupBox_32)
        self.birthdaylabel.setObjectName("birthdaylabel")
        self.vboxlayout18.addWidget(self.birthdaylabel)
        self.hboxlayout9.addLayout(self.vboxlayout18)

        self.vboxlayout19 = QtGui.QVBoxLayout()
        self.vboxlayout19.setMargin(0)
        self.vboxlayout19.setSpacing(2)
        self.vboxlayout19.setObjectName("vboxlayout19")

        self.birthday = QtGui.QLineEdit(self.groupBox_32)
        self.birthday.setObjectName("birthday")
        self.vboxlayout19.addWidget(self.birthday)
        self.hboxlayout9.addLayout(self.vboxlayout19)
        self.gridlayout8.addLayout(self.hboxlayout9,0,0,1,1)
        self.gridlayout6.addWidget(self.groupBox_32,0,0,1,1)
        self.tab.addTab(self.tab_6,"")
        self.gridlayout.addWidget(self.tab,0,0,1,2)

        self.retranslateUi(vcard)
        self.tab.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),vcard.reject)
        QtCore.QMetaObject.connectSlotsByName(vcard)

    def retranslateUi(self, vcard):
        vcard.setWindowTitle(QtGui.QApplication.translate("vcard", "User Information", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("vcard", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("vcard", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.photo.setText(QtGui.QApplication.translate("vcard", "No Photo", None, QtGui.QApplication.UnicodeUTF8))
        self.fullnamelabel.setText(QtGui.QApplication.translate("vcard", "Full name:", None, QtGui.QApplication.UnicodeUTF8))
        self.famillynamelabel.setText(QtGui.QApplication.translate("vcard", "Familly name:", None, QtGui.QApplication.UnicodeUTF8))
        self.namelabel.setText(QtGui.QApplication.translate("vcard", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.middlenamelabel.setText(QtGui.QApplication.translate("vcard", "Middle name:", None, QtGui.QApplication.UnicodeUTF8))
        self.prefixlabel.setText(QtGui.QApplication.translate("vcard", "Prefix:", None, QtGui.QApplication.UnicodeUTF8))
        self.suffixlabel.setText(QtGui.QApplication.translate("vcard", "Suffix:", None, QtGui.QApplication.UnicodeUTF8))
        self.nicknamelabel.setText(QtGui.QApplication.translate("vcard", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("vcard", "Information", None, QtGui.QApplication.UnicodeUTF8))
        self.emaillabel.setText(QtGui.QApplication.translate("vcard", "Email:", None, QtGui.QApplication.UnicodeUTF8))
        self.websitelabel.setText(QtGui.QApplication.translate("vcard", "Web site:", None, QtGui.QApplication.UnicodeUTF8))
        self.jidlabel.setText(QtGui.QApplication.translate("vcard", "JID:", None, QtGui.QApplication.UnicodeUTF8))
        self.uidlabel.setText(QtGui.QApplication.translate("vcard", "UID:", None, QtGui.QApplication.UnicodeUTF8))
        self.tab.setTabText(self.tab.indexOf(self.tab_2), QtGui.QApplication.translate("vcard", "Personal", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("vcard", "Telephone numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.preferredlabel.setText(QtGui.QApplication.translate("vcard", "Preferred:", None, QtGui.QApplication.UnicodeUTF8))
        self.homelabel.setText(QtGui.QApplication.translate("vcard", "Home:", None, QtGui.QApplication.UnicodeUTF8))
        self.worklabel.setText(QtGui.QApplication.translate("vcard", "Work:", None, QtGui.QApplication.UnicodeUTF8))
        self.voicelabel.setText(QtGui.QApplication.translate("vcard", "Voice:", None, QtGui.QApplication.UnicodeUTF8))
        self.faxlabel.setText(QtGui.QApplication.translate("vcard", "Fax:", None, QtGui.QApplication.UnicodeUTF8))
        self.pagerlabel.setText(QtGui.QApplication.translate("vcard", "Pager:", None, QtGui.QApplication.UnicodeUTF8))
        self.messagerecorderlabel.setText(QtGui.QApplication.translate("vcard", "Message recorder:", None, QtGui.QApplication.UnicodeUTF8))
        self.celllabel.setText(QtGui.QApplication.translate("vcard", "Cell:", None, QtGui.QApplication.UnicodeUTF8))
        self.videolabel.setText(QtGui.QApplication.translate("vcard", "Video:", None, QtGui.QApplication.UnicodeUTF8))
        self.bbslabel.setText(QtGui.QApplication.translate("vcard", "BBS:", None, QtGui.QApplication.UnicodeUTF8))
        self.modemlabel.setText(QtGui.QApplication.translate("vcard", "Modem:", None, QtGui.QApplication.UnicodeUTF8))
        self.isdnlabel.setText(QtGui.QApplication.translate("vcard", "ISDN:", None, QtGui.QApplication.UnicodeUTF8))
        self.pcslabel.setText(QtGui.QApplication.translate("vcard", "PCS:", None, QtGui.QApplication.UnicodeUTF8))
        self.tab.setTabText(self.tab.indexOf(self.tab1), QtGui.QApplication.translate("vcard", "Phones", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("vcard", "Geographical position", None, QtGui.QApplication.UnicodeUTF8))
        self.latitudelabel.setText(QtGui.QApplication.translate("vcard", "Latitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.logitudelabel.setText(QtGui.QApplication.translate("vcard", "Logitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("vcard", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.addresslabel.setText(QtGui.QApplication.translate("vcard", "Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.address2label.setText(QtGui.QApplication.translate("vcard", "Address 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.citylabel.setText(QtGui.QApplication.translate("vcard", "City:", None, QtGui.QApplication.UnicodeUTF8))
        self.statelabel.setText(QtGui.QApplication.translate("vcard", "State:", None, QtGui.QApplication.UnicodeUTF8))
        self.postalcodelabel.setText(QtGui.QApplication.translate("vcard", "Postal code:", None, QtGui.QApplication.UnicodeUTF8))
        self.countrylabel.setText(QtGui.QApplication.translate("vcard", "Country:", None, QtGui.QApplication.UnicodeUTF8))
        self.tab.setTabText(self.tab.indexOf(self.tab_4), QtGui.QApplication.translate("vcard", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_31.setTitle(QtGui.QApplication.translate("vcard", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.orgnamelabel.setText(QtGui.QApplication.translate("vcard", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.orgunitlabel.setText(QtGui.QApplication.translate("vcard", "Unit:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_28.setTitle(QtGui.QApplication.translate("vcard", "Personal", None, QtGui.QApplication.UnicodeUTF8))
        self.orgtitlelabel.setText(QtGui.QApplication.translate("vcard", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.orgrolelabel.setText(QtGui.QApplication.translate("vcard", "Role:", None, QtGui.QApplication.UnicodeUTF8))
        self.tab.setTabText(self.tab.indexOf(self.tab_5), QtGui.QApplication.translate("vcard", "Organization", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_33.setTitle(QtGui.QApplication.translate("vcard", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_32.setTitle(QtGui.QApplication.translate("vcard", "Birthday", None, QtGui.QApplication.UnicodeUTF8))
        self.birthdaylabel.setText(QtGui.QApplication.translate("vcard", "Birthday:", None, QtGui.QApplication.UnicodeUTF8))
        self.tab.setTabText(self.tab.indexOf(self.tab_6), QtGui.QApplication.translate("vcard", "About", None, QtGui.QApplication.UnicodeUTF8))

