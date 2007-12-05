# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/vcardeditor.ui'
#
# Created: Wed Dec  5 19:50:11 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VCardEdit(object):
    def setupUi(self, VCardEdit):
        VCardEdit.setObjectName("VCardEdit")
        VCardEdit.resize(QtCore.QSize(QtCore.QRect(0,0,336,336).size()).expandedTo(VCardEdit.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(VCardEdit)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.pushButton_2 = QtGui.QPushButton(VCardEdit)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,2,1,1,1)

        self.pushButton = QtGui.QPushButton(VCardEdit)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,2,2,1,1)

        self.tabWidget = QtGui.QTabWidget(VCardEdit)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.name = QtGui.QLineEdit(self.tab)
        self.name.setObjectName("name")
        self.gridlayout1.addWidget(self.name,0,1,1,1)

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.surname = QtGui.QLineEdit(self.tab)
        self.surname.setObjectName("surname")
        self.gridlayout1.addWidget(self.surname,1,1,1,1)

        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,2,0,1,1)

        self.fullname = QtGui.QLineEdit(self.tab)
        self.fullname.setObjectName("fullname")
        self.gridlayout1.addWidget(self.fullname,2,1,1,1)

        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,3,0,1,1)

        self.nickname = QtGui.QLineEdit(self.tab)
        self.nickname.setObjectName("nickname")
        self.gridlayout1.addWidget(self.nickname,3,1,1,1)

        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,5,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.avatar = QtGui.QLabel(self.tab)
        self.avatar.setObjectName("avatar")
        self.hboxlayout.addWidget(self.avatar)

        self.setAvatar = QtGui.QPushButton(self.tab)
        self.setAvatar.setObjectName("setAvatar")
        self.hboxlayout.addWidget(self.setAvatar)
        self.gridlayout1.addLayout(self.hboxlayout,5,1,1,1)

        self.label_10 = QtGui.QLabel(self.tab)
        self.label_10.setObjectName("label_10")
        self.gridlayout1.addWidget(self.label_10,4,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.homepage_label = QtGui.QLabel(self.tab)
        self.homepage_label.setObjectName("homepage_label")
        self.hboxlayout1.addWidget(self.homepage_label)

        self.homepage_edit = QtGui.QLineEdit(self.tab)
        self.homepage_edit.setObjectName("homepage_edit")
        self.hboxlayout1.addWidget(self.homepage_edit)
        self.gridlayout1.addLayout(self.hboxlayout1,4,1,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem1 = QtGui.QSpacerItem(20,61,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,5,1,1,1)

        self.label_9 = QtGui.QLabel(self.tab_2)
        self.label_9.setObjectName("label_9")
        self.gridlayout2.addWidget(self.label_9,4,0,1,1)

        self.label_8 = QtGui.QLabel(self.tab_2)
        self.label_8.setObjectName("label_8")
        self.gridlayout2.addWidget(self.label_8,3,0,1,1)

        self.homepcode = QtGui.QLineEdit(self.tab_2)
        self.homepcode.setObjectName("homepcode")
        self.gridlayout2.addWidget(self.homepcode,4,1,1,1)

        self.homecountry = QtGui.QLineEdit(self.tab_2)
        self.homecountry.setObjectName("homecountry")
        self.gridlayout2.addWidget(self.homecountry,3,1,1,1)

        self.homelocality = QtGui.QLineEdit(self.tab_2)
        self.homelocality.setObjectName("homelocality")
        self.gridlayout2.addWidget(self.homelocality,2,1,1,1)

        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName("label_7")
        self.gridlayout2.addWidget(self.label_7,2,0,1,1)

        self.homestreet = QtGui.QLineEdit(self.tab_2)
        self.homestreet.setObjectName("homestreet")
        self.gridlayout2.addWidget(self.homestreet,0,1,1,1)

        self.homeextadd = QtGui.QLineEdit(self.tab_2)
        self.homeextadd.setObjectName("homeextadd")
        self.gridlayout2.addWidget(self.homeextadd,1,1,1,1)

        self.label_6 = QtGui.QLabel(self.tab_2)
        self.label_6.setObjectName("label_6")
        self.gridlayout2.addWidget(self.label_6,0,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout3.setObjectName("gridlayout3")

        self.about = QtGui.QTextEdit(self.tab_4)
        self.about.setObjectName("about")
        self.gridlayout3.addWidget(self.about,0,0,1,1)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout4.setObjectName("gridlayout4")

        self.ver_label_name = QtGui.QLabel(self.tab_3)
        self.ver_label_name.setObjectName("ver_label_name")
        self.gridlayout4.addWidget(self.ver_label_name,0,0,1,1)

        self.ver_name = QtGui.QLineEdit(self.tab_3)
        self.ver_name.setReadOnly(True)
        self.ver_name.setObjectName("ver_name")
        self.gridlayout4.addWidget(self.ver_name,0,1,1,1)

        self.ver_label_version = QtGui.QLabel(self.tab_3)
        self.ver_label_version.setObjectName("ver_label_version")
        self.gridlayout4.addWidget(self.ver_label_version,1,0,1,1)

        self.ver_version = QtGui.QLineEdit(self.tab_3)
        self.ver_version.setReadOnly(True)
        self.ver_version.setObjectName("ver_version")
        self.gridlayout4.addWidget(self.ver_version,1,1,1,1)

        self.ver_label_os = QtGui.QLabel(self.tab_3)
        self.ver_label_os.setObjectName("ver_label_os")
        self.gridlayout4.addWidget(self.ver_label_os,2,0,1,1)

        self.ver_os = QtGui.QLineEdit(self.tab_3)
        self.ver_os.setReadOnly(True)
        self.ver_os.setObjectName("ver_os")
        self.gridlayout4.addWidget(self.ver_os,2,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem2,3,1,1,1)
        self.tabWidget.addTab(self.tab_3,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,3)

        self.download = QtGui.QLabel(VCardEdit)
        self.download.setAlignment(QtCore.Qt.AlignCenter)
        self.download.setObjectName("download")
        self.gridlayout.addWidget(self.download,1,0,1,3)

        self.retranslateUi(VCardEdit)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),VCardEdit.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),VCardEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(VCardEdit)
        VCardEdit.setTabOrder(self.tabWidget,self.name)
        VCardEdit.setTabOrder(self.name,self.surname)
        VCardEdit.setTabOrder(self.surname,self.fullname)
        VCardEdit.setTabOrder(self.fullname,self.nickname)
        VCardEdit.setTabOrder(self.nickname,self.setAvatar)
        VCardEdit.setTabOrder(self.setAvatar,self.homestreet)
        VCardEdit.setTabOrder(self.homestreet,self.homeextadd)
        VCardEdit.setTabOrder(self.homeextadd,self.homelocality)
        VCardEdit.setTabOrder(self.homelocality,self.homecountry)
        VCardEdit.setTabOrder(self.homecountry,self.homepcode)
        VCardEdit.setTabOrder(self.homepcode,self.pushButton_2)
        VCardEdit.setTabOrder(self.pushButton_2,self.pushButton)

    def retranslateUi(self, VCardEdit):
        self.pushButton_2.setText(QtGui.QApplication.translate("VCardEdit", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("VCardEdit", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VCardEdit", "First name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VCardEdit", "Surname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("VCardEdit", "Full name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VCardEdit", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VCardEdit", "Avatar:", None, QtGui.QApplication.UnicodeUTF8))
        self.avatar.setText(QtGui.QApplication.translate("VCardEdit", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.setAvatar.setText(QtGui.QApplication.translate("VCardEdit", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("VCardEdit", "Homepage:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("VCardEdit", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("VCardEdit", "Post code:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("VCardEdit", "Country:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("VCardEdit", "Locality:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("VCardEdit", "Street:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("VCardEdit", "Home address", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("VCardEdit", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.ver_label_name.setText(QtGui.QApplication.translate("VCardEdit", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.ver_label_version.setText(QtGui.QApplication.translate("VCardEdit", "Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.ver_label_os.setText(QtGui.QApplication.translate("VCardEdit", "Operating system:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("VCardEdit", "Software info", None, QtGui.QApplication.UnicodeUTF8))
        self.download.setText(QtGui.QApplication.translate("VCardEdit", "Downloading vCard...", None, QtGui.QApplication.UnicodeUTF8))

