# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/vcardeditor.ui'
#
# Created: Sun Nov 11 17:01:13 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VCardEdit(object):
    def setupUi(self, VCardEdit):
        VCardEdit.setObjectName("VCardEdit")
        VCardEdit.resize(QtCore.QSize(QtCore.QRect(0,0,336,317).size()).expandedTo(VCardEdit.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(VCardEdit)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(VCardEdit)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.avatar = QtGui.QLabel(self.tab)
        self.avatar.setObjectName("avatar")
        self.gridlayout1.addWidget(self.avatar,4,1,1,1)

        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,4,0,1,1)

        spacerItem = QtGui.QSpacerItem(75,71,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,5,1,1,1)

        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,3,0,1,1)

        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.name = QtGui.QLineEdit(self.tab)
        self.name.setObjectName("name")
        self.gridlayout1.addWidget(self.name,0,1,1,2)

        self.surname = QtGui.QLineEdit(self.tab)
        self.surname.setObjectName("surname")
        self.gridlayout1.addWidget(self.surname,1,1,1,2)

        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.gridlayout1.addWidget(self.label_5,2,0,1,1)

        self.fullname = QtGui.QLineEdit(self.tab)
        self.fullname.setObjectName("fullname")
        self.gridlayout1.addWidget(self.fullname,2,1,1,2)

        self.nickname = QtGui.QLineEdit(self.tab)
        self.nickname.setObjectName("nickname")
        self.gridlayout1.addWidget(self.nickname,3,1,1,2)

        self.setAvatar = QtGui.QPushButton(self.tab)
        self.setAvatar.setObjectName("setAvatar")
        self.gridlayout1.addWidget(self.setAvatar,4,2,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,3)

        spacerItem1 = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,0,1,1)

        self.pushButton_2 = QtGui.QPushButton(VCardEdit)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,1,1,1,1)

        self.pushButton = QtGui.QPushButton(VCardEdit)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,1,2,1,1)

        self.retranslateUi(VCardEdit)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),VCardEdit.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),VCardEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(VCardEdit)

    def retranslateUi(self, VCardEdit):
        VCardEdit.setWindowTitle(QtGui.QApplication.translate("VCardEdit", "VCard Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.avatar.setText(QtGui.QApplication.translate("VCardEdit", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VCardEdit", "Avatar:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VCardEdit", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VCardEdit", "Surname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VCardEdit", "First name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("VCardEdit", "Full name:", None, QtGui.QApplication.UnicodeUTF8))
        self.setAvatar.setText(QtGui.QApplication.translate("VCardEdit", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("VCardEdit", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("VCardEdit", "Home address", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("VCardEdit", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("VCardEdit", "Save", None, QtGui.QApplication.UnicodeUTF8))

