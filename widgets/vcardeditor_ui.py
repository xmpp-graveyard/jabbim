# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/vcardeditor.ui'
#
# Created: Sun Nov 11 12:50:16 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VCardEdit(object):
    def setupUi(self, VCardEdit):
        VCardEdit.setObjectName("VCardEdit")
        VCardEdit.resize(QtCore.QSize(QtCore.QRect(0,0,271,241).size()).expandedTo(VCardEdit.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(VCardEdit)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.nickname = QtGui.QLineEdit(VCardEdit)
        self.nickname.setObjectName("nickname")
        self.gridlayout.addWidget(self.nickname,3,1,1,4)

        self.label_4 = QtGui.QLabel(VCardEdit)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.setAvatar = QtGui.QPushButton(VCardEdit)
        self.setAvatar.setObjectName("setAvatar")
        self.gridlayout.addWidget(self.setAvatar,4,4,1,1)

        self.avatar = QtGui.QLabel(VCardEdit)
        self.avatar.setObjectName("avatar")
        self.gridlayout.addWidget(self.avatar,4,2,1,2)

        self.label_3 = QtGui.QLabel(VCardEdit)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,4,0,1,2)

        spacerItem = QtGui.QSpacerItem(75,71,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,5,2,1,1)

        self.fullname = QtGui.QLineEdit(VCardEdit)
        self.fullname.setObjectName("fullname")
        self.gridlayout.addWidget(self.fullname,2,1,1,4)

        spacerItem1 = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,6,0,1,2)

        self.pushButton_2 = QtGui.QPushButton(VCardEdit)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,6,2,1,1)

        self.pushButton = QtGui.QPushButton(VCardEdit)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,6,3,1,2)

        self.label_2 = QtGui.QLabel(VCardEdit)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.label = QtGui.QLabel(VCardEdit)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.name = QtGui.QLineEdit(VCardEdit)
        self.name.setObjectName("name")
        self.gridlayout.addWidget(self.name,0,1,1,4)

        self.surname = QtGui.QLineEdit(VCardEdit)
        self.surname.setObjectName("surname")
        self.gridlayout.addWidget(self.surname,1,1,1,4)

        self.label_5 = QtGui.QLabel(VCardEdit)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,2,0,1,1)

        self.retranslateUi(VCardEdit)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),VCardEdit.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),VCardEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(VCardEdit)

    def retranslateUi(self, VCardEdit):
        VCardEdit.setWindowTitle(QtGui.QApplication.translate("VCardEdit", "VCard Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("VCardEdit", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.setAvatar.setText(QtGui.QApplication.translate("VCardEdit", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.avatar.setText(QtGui.QApplication.translate("VCardEdit", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VCardEdit", "Avatar:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("VCardEdit", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("VCardEdit", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VCardEdit", "Surname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VCardEdit", "First name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("VCardEdit", "Full name:", None, QtGui.QApplication.UnicodeUTF8))

