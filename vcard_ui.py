# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vcard.ui'
#
# Created: Sat Feb 24 13:15:06 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_vcard(object):
    def setupUi(self, vcard):
        vcard.setObjectName("vcard")
        vcard.resize(QtCore.QSize(QtCore.QRect(0,0,396,492).size()).expandedTo(vcard.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(vcard)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(431,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.pushButton = QtGui.QPushButton(vcard)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,1,1,1,1)

        self.orgname = QtGui.QTabWidget(vcard)
        self.orgname.setObjectName("orgname")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout1 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout.setMargin(6)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)

        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.vboxlayout.addWidget(self.label_5)

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.vboxlayout.addWidget(self.label_6)

        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.vboxlayout.addWidget(self.label_7)

        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.vboxlayout.addWidget(self.label_8)
        self.hboxlayout1.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
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
        self.hboxlayout1.addLayout(self.vboxlayout1)
        self.hboxlayout.addLayout(self.hboxlayout1)
        self.gridlayout1.addWidget(self.groupBox,0,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName("groupBox_2")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.hboxlayout2.setMargin(6)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.vboxlayout2.addWidget(self.label_10)

        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.vboxlayout2.addWidget(self.label_9)

        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setObjectName("label_11")
        self.vboxlayout2.addWidget(self.label_11)

        self.label_12 = QtGui.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.vboxlayout2.addWidget(self.label_12)
        self.hboxlayout3.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
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
        self.hboxlayout3.addLayout(self.vboxlayout3)
        self.hboxlayout2.addLayout(self.hboxlayout3)
        self.gridlayout1.addWidget(self.groupBox_2,1,0,1,1)
        self.orgname.addTab(self.tab_2,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout2 = QtGui.QGridLayout(self.tab)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout4.setMargin(6)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setMargin(0)
        self.vboxlayout5.setSpacing(2)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.label_25 = QtGui.QLabel(self.groupBox_3)
        self.label_25.setObjectName("label_25")
        self.vboxlayout5.addWidget(self.label_25)

        self.label_13 = QtGui.QLabel(self.groupBox_3)
        self.label_13.setObjectName("label_13")
        self.vboxlayout5.addWidget(self.label_13)

        self.label_14 = QtGui.QLabel(self.groupBox_3)
        self.label_14.setObjectName("label_14")
        self.vboxlayout5.addWidget(self.label_14)

        self.label_15 = QtGui.QLabel(self.groupBox_3)
        self.label_15.setObjectName("label_15")
        self.vboxlayout5.addWidget(self.label_15)

        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setObjectName("label_16")
        self.vboxlayout5.addWidget(self.label_16)

        self.label_18 = QtGui.QLabel(self.groupBox_3)
        self.label_18.setObjectName("label_18")
        self.vboxlayout5.addWidget(self.label_18)

        self.label_19 = QtGui.QLabel(self.groupBox_3)
        self.label_19.setObjectName("label_19")
        self.vboxlayout5.addWidget(self.label_19)

        self.label_20 = QtGui.QLabel(self.groupBox_3)
        self.label_20.setObjectName("label_20")
        self.vboxlayout5.addWidget(self.label_20)

        self.label_21 = QtGui.QLabel(self.groupBox_3)
        self.label_21.setObjectName("label_21")
        self.vboxlayout5.addWidget(self.label_21)

        self.label_23 = QtGui.QLabel(self.groupBox_3)
        self.label_23.setObjectName("label_23")
        self.vboxlayout5.addWidget(self.label_23)

        self.label_22 = QtGui.QLabel(self.groupBox_3)
        self.label_22.setObjectName("label_22")
        self.vboxlayout5.addWidget(self.label_22)

        self.label_17 = QtGui.QLabel(self.groupBox_3)
        self.label_17.setObjectName("label_17")
        self.vboxlayout5.addWidget(self.label_17)

        self.label_24 = QtGui.QLabel(self.groupBox_3)
        self.label_24.setObjectName("label_24")
        self.vboxlayout5.addWidget(self.label_24)
        self.hboxlayout4.addLayout(self.vboxlayout5)

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

        self.vide = QtGui.QLineEdit(self.groupBox_3)
        self.vide.setObjectName("vide")
        self.vboxlayout6.addWidget(self.vide)

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
        self.hboxlayout4.addLayout(self.vboxlayout6)
        self.vboxlayout4.addLayout(self.hboxlayout4)
        self.gridlayout2.addWidget(self.groupBox_3,0,0,1,1)
        self.orgname.addTab(self.tab,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        spacerItem2 = QtGui.QSpacerItem(20,111,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem2,2,0,1,1)

        self.groupBox_5 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName("groupBox_5")

        self.hboxlayout5 = QtGui.QHBoxLayout(self.groupBox_5)
        self.hboxlayout5.setMargin(6)
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setMargin(0)
        self.hboxlayout6.setSpacing(6)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.vboxlayout7 = QtGui.QVBoxLayout()
        self.vboxlayout7.setMargin(0)
        self.vboxlayout7.setSpacing(2)
        self.vboxlayout7.setObjectName("vboxlayout7")

        self.label_32 = QtGui.QLabel(self.groupBox_5)
        self.label_32.setObjectName("label_32")
        self.vboxlayout7.addWidget(self.label_32)

        self.label_33 = QtGui.QLabel(self.groupBox_5)
        self.label_33.setObjectName("label_33")
        self.vboxlayout7.addWidget(self.label_33)
        self.hboxlayout6.addLayout(self.vboxlayout7)

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
        self.hboxlayout6.addLayout(self.vboxlayout8)
        self.hboxlayout5.addLayout(self.hboxlayout6)
        self.gridlayout3.addWidget(self.groupBox_5,1,0,1,1)

        self.groupBox_4 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_4.setObjectName("groupBox_4")

        self.vboxlayout9 = QtGui.QVBoxLayout(self.groupBox_4)
        self.vboxlayout9.setMargin(6)
        self.vboxlayout9.setSpacing(6)
        self.vboxlayout9.setObjectName("vboxlayout9")

        self.hboxlayout7 = QtGui.QHBoxLayout()
        self.hboxlayout7.setMargin(0)
        self.hboxlayout7.setSpacing(6)
        self.hboxlayout7.setObjectName("hboxlayout7")

        self.vboxlayout10 = QtGui.QVBoxLayout()
        self.vboxlayout10.setMargin(0)
        self.vboxlayout10.setSpacing(2)
        self.vboxlayout10.setObjectName("vboxlayout10")

        self.label_26 = QtGui.QLabel(self.groupBox_4)
        self.label_26.setObjectName("label_26")
        self.vboxlayout10.addWidget(self.label_26)

        self.label_27 = QtGui.QLabel(self.groupBox_4)
        self.label_27.setObjectName("label_27")
        self.vboxlayout10.addWidget(self.label_27)

        self.label_28 = QtGui.QLabel(self.groupBox_4)
        self.label_28.setObjectName("label_28")
        self.vboxlayout10.addWidget(self.label_28)

        self.label_29 = QtGui.QLabel(self.groupBox_4)
        self.label_29.setObjectName("label_29")
        self.vboxlayout10.addWidget(self.label_29)

        self.label_30 = QtGui.QLabel(self.groupBox_4)
        self.label_30.setObjectName("label_30")
        self.vboxlayout10.addWidget(self.label_30)

        self.label_31 = QtGui.QLabel(self.groupBox_4)
        self.label_31.setObjectName("label_31")
        self.vboxlayout10.addWidget(self.label_31)
        self.hboxlayout7.addLayout(self.vboxlayout10)

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
        self.hboxlayout7.addLayout(self.vboxlayout11)
        self.vboxlayout9.addLayout(self.hboxlayout7)
        self.gridlayout3.addWidget(self.groupBox_4,0,0,1,1)
        self.orgname.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_5)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.groupBox_31 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_31.setObjectName("groupBox_31")

        self.vboxlayout12 = QtGui.QVBoxLayout(self.groupBox_31)
        self.vboxlayout12.setMargin(6)
        self.vboxlayout12.setSpacing(6)
        self.vboxlayout12.setObjectName("vboxlayout12")

        self.hboxlayout8 = QtGui.QHBoxLayout()
        self.hboxlayout8.setMargin(0)
        self.hboxlayout8.setSpacing(6)
        self.hboxlayout8.setObjectName("hboxlayout8")

        self.vboxlayout13 = QtGui.QVBoxLayout()
        self.vboxlayout13.setMargin(0)
        self.vboxlayout13.setSpacing(2)
        self.vboxlayout13.setObjectName("vboxlayout13")

        self.label_34 = QtGui.QLabel(self.groupBox_31)
        self.label_34.setObjectName("label_34")
        self.vboxlayout13.addWidget(self.label_34)

        self.label_35 = QtGui.QLabel(self.groupBox_31)
        self.label_35.setObjectName("label_35")
        self.vboxlayout13.addWidget(self.label_35)
        self.hboxlayout8.addLayout(self.vboxlayout13)

        self.vboxlayout14 = QtGui.QVBoxLayout()
        self.vboxlayout14.setMargin(0)
        self.vboxlayout14.setSpacing(2)
        self.vboxlayout14.setObjectName("vboxlayout14")

        self.lineEdit_36 = QtGui.QLineEdit(self.groupBox_31)
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.vboxlayout14.addWidget(self.lineEdit_36)

        self.orgunit = QtGui.QLineEdit(self.groupBox_31)
        self.orgunit.setObjectName("orgunit")
        self.vboxlayout14.addWidget(self.orgunit)
        self.hboxlayout8.addLayout(self.vboxlayout14)
        self.vboxlayout12.addLayout(self.hboxlayout8)
        self.gridlayout4.addWidget(self.groupBox_31,0,0,1,1)

        self.groupBox_28 = QtGui.QGroupBox(self.tab_5)
        self.groupBox_28.setObjectName("groupBox_28")

        self.vboxlayout15 = QtGui.QVBoxLayout(self.groupBox_28)
        self.vboxlayout15.setMargin(6)
        self.vboxlayout15.setSpacing(6)
        self.vboxlayout15.setObjectName("vboxlayout15")

        self.hboxlayout9 = QtGui.QHBoxLayout()
        self.hboxlayout9.setMargin(0)
        self.hboxlayout9.setSpacing(6)
        self.hboxlayout9.setObjectName("hboxlayout9")

        self.vboxlayout16 = QtGui.QVBoxLayout()
        self.vboxlayout16.setMargin(0)
        self.vboxlayout16.setSpacing(2)
        self.vboxlayout16.setObjectName("vboxlayout16")

        self.label_37 = QtGui.QLabel(self.groupBox_28)
        self.label_37.setObjectName("label_37")
        self.vboxlayout16.addWidget(self.label_37)

        self.label_36 = QtGui.QLabel(self.groupBox_28)
        self.label_36.setObjectName("label_36")
        self.vboxlayout16.addWidget(self.label_36)
        self.hboxlayout9.addLayout(self.vboxlayout16)

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
        self.hboxlayout9.addLayout(self.vboxlayout17)
        self.vboxlayout15.addLayout(self.hboxlayout9)
        self.gridlayout4.addWidget(self.groupBox_28,1,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem3,2,0,1,1)
        self.orgname.addTab(self.tab_5,"")

        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName("tab_6")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_6)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.groupBox_32 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_32.setObjectName("groupBox_32")

        self.gridlayout6 = QtGui.QGridLayout(self.groupBox_32)
        self.gridlayout6.setMargin(6)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.hboxlayout10 = QtGui.QHBoxLayout()
        self.hboxlayout10.setMargin(0)
        self.hboxlayout10.setSpacing(6)
        self.hboxlayout10.setObjectName("hboxlayout10")

        self.vboxlayout18 = QtGui.QVBoxLayout()
        self.vboxlayout18.setMargin(0)
        self.vboxlayout18.setSpacing(2)
        self.vboxlayout18.setObjectName("vboxlayout18")

        self.label_38 = QtGui.QLabel(self.groupBox_32)
        self.label_38.setObjectName("label_38")
        self.vboxlayout18.addWidget(self.label_38)
        self.hboxlayout10.addLayout(self.vboxlayout18)

        self.vboxlayout19 = QtGui.QVBoxLayout()
        self.vboxlayout19.setMargin(0)
        self.vboxlayout19.setSpacing(2)
        self.vboxlayout19.setObjectName("vboxlayout19")

        self.birthday = QtGui.QLineEdit(self.groupBox_32)
        self.birthday.setObjectName("birthday")
        self.vboxlayout19.addWidget(self.birthday)
        self.hboxlayout10.addLayout(self.vboxlayout19)
        self.gridlayout6.addLayout(self.hboxlayout10,0,0,1,1)
        self.gridlayout5.addWidget(self.groupBox_32,1,0,1,1)

        self.groupBox_33 = QtGui.QGroupBox(self.tab_6)
        self.groupBox_33.setObjectName("groupBox_33")

        self.gridlayout7 = QtGui.QGridLayout(self.groupBox_33)
        self.gridlayout7.setMargin(6)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.about = QtGui.QTextEdit(self.groupBox_33)
        self.about.setObjectName("about")
        self.gridlayout7.addWidget(self.about,0,0,1,1)
        self.gridlayout5.addWidget(self.groupBox_33,2,0,1,1)

        self.photo = QtGui.QLabel(self.tab_6)
        self.photo.setObjectName("photo")
        self.gridlayout5.addWidget(self.photo,0,0,1,1)
        self.orgname.addTab(self.tab_6,"")
        self.gridlayout.addWidget(self.orgname,0,0,1,2)

        self.retranslateUi(vcard)
        self.orgname.setCurrentIndex(4)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),vcard.reject)
        QtCore.QMetaObject.connectSlotsByName(vcard)

    def retranslateUi(self, vcard):
        vcard.setWindowTitle(QtGui.QApplication.translate("vcard", "User Information", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("vcard", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("vcard", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("vcard", "Full name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("vcard", "Familly name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("vcard", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("vcard", "Middle name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("vcard", "Prefix:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("vcard", "Suffix:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("vcard", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("vcard", "Information", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("vcard", "Email:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("vcard", "Web site:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("vcard", "JID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("vcard", "UID:", None, QtGui.QApplication.UnicodeUTF8))
        self.orgname.setTabText(self.orgname.indexOf(self.tab_2), QtGui.QApplication.translate("vcard", "Personal", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("vcard", "Telephone numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_25.setText(QtGui.QApplication.translate("vcard", "Preferred:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("vcard", "Home:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("vcard", "Work:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("vcard", "Voice:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("vcard", "Fax:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("vcard", "Pager:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("vcard", "Message recorder:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("vcard", "Cell:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_21.setText(QtGui.QApplication.translate("vcard", "Video:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_23.setText(QtGui.QApplication.translate("vcard", "BBS:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_22.setText(QtGui.QApplication.translate("vcard", "Modem:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("vcard", "ISDN:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_24.setText(QtGui.QApplication.translate("vcard", "PCS:", None, QtGui.QApplication.UnicodeUTF8))
        self.orgname.setTabText(self.orgname.indexOf(self.tab), QtGui.QApplication.translate("vcard", "Phones", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("vcard", "Geographical position", None, QtGui.QApplication.UnicodeUTF8))
        self.label_32.setText(QtGui.QApplication.translate("vcard", "Latitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_33.setText(QtGui.QApplication.translate("vcard", "Logitude:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("vcard", "Address", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("vcard", "Address:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_27.setText(QtGui.QApplication.translate("vcard", "Address 2:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_28.setText(QtGui.QApplication.translate("vcard", "City:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_29.setText(QtGui.QApplication.translate("vcard", "State:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_30.setText(QtGui.QApplication.translate("vcard", "Postal code:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_31.setText(QtGui.QApplication.translate("vcard", "Country:", None, QtGui.QApplication.UnicodeUTF8))
        self.orgname.setTabText(self.orgname.indexOf(self.tab_4), QtGui.QApplication.translate("vcard", "Location", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_31.setTitle(QtGui.QApplication.translate("vcard", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.label_34.setText(QtGui.QApplication.translate("vcard", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_35.setText(QtGui.QApplication.translate("vcard", "Unit:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_28.setTitle(QtGui.QApplication.translate("vcard", "Personal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_37.setText(QtGui.QApplication.translate("vcard", "Title:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_36.setText(QtGui.QApplication.translate("vcard", "Role:", None, QtGui.QApplication.UnicodeUTF8))
        self.orgname.setTabText(self.orgname.indexOf(self.tab_5), QtGui.QApplication.translate("vcard", "Organization", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_32.setTitle(QtGui.QApplication.translate("vcard", "Birthday", None, QtGui.QApplication.UnicodeUTF8))
        self.label_38.setText(QtGui.QApplication.translate("vcard", "Birthday:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_33.setTitle(QtGui.QApplication.translate("vcard", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.photo.setText(QtGui.QApplication.translate("vcard", "No Photo", None, QtGui.QApplication.UnicodeUTF8))
        self.orgname.setTabText(self.orgname.indexOf(self.tab_6), QtGui.QApplication.translate("vcard", "About", None, QtGui.QApplication.UnicodeUTF8))

