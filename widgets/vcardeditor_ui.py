# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/vcardeditor.ui'
#
# Created: Fri Nov  9 23:03:52 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VCardEdit(object):
    def setupUi(self, VCardEdit):
        VCardEdit.setObjectName("VCardEdit")
        VCardEdit.resize(QtCore.QSize(QtCore.QRect(0,0,294,223).size()).expandedTo(VCardEdit.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(VCardEdit)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.name = QtGui.QLineEdit(VCardEdit)
        self.name.setObjectName("name")
        self.gridlayout1.addWidget(self.name,0,1,1,2)

        self.label_3 = QtGui.QLabel(VCardEdit)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,2,0,1,1)

        self.setAvatar = QtGui.QPushButton(VCardEdit)
        self.setAvatar.setObjectName("setAvatar")
        self.gridlayout1.addWidget(self.setAvatar,2,2,1,1)

        self.surname = QtGui.QLineEdit(VCardEdit)
        self.surname.setObjectName("surname")
        self.gridlayout1.addWidget(self.surname,1,1,1,2)

        self.avatar = QtGui.QLabel(VCardEdit)
        self.avatar.setObjectName("avatar")
        self.gridlayout1.addWidget(self.avatar,2,1,1,1)

        self.label_2 = QtGui.QLabel(VCardEdit)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,1,0,1,1)

        self.label = QtGui.QLabel(VCardEdit)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,3)

        spacerItem = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.pushButton_2 = QtGui.QPushButton(VCardEdit)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,2,1,1,1)

        self.pushButton = QtGui.QPushButton(VCardEdit)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,2,2,1,1)

        spacerItem1 = QtGui.QSpacerItem(75,51,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,1,1,1,1)

        self.retranslateUi(VCardEdit)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),VCardEdit.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),VCardEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(VCardEdit)

    def retranslateUi(self, VCardEdit):
        VCardEdit.setWindowTitle(QtGui.QApplication.translate("VCardEdit", "VCard Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("VCardEdit", "Avatar:", None, QtGui.QApplication.UnicodeUTF8))
        self.setAvatar.setText(QtGui.QApplication.translate("VCardEdit", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.avatar.setText(QtGui.QApplication.translate("VCardEdit", "Avatar", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("VCardEdit", "Surname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VCardEdit", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("VCardEdit", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("VCardEdit", "Save", None, QtGui.QApplication.UnicodeUTF8))

