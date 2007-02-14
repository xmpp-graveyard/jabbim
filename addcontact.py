# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addcontact.ui'
#
# Created: Wed Feb 14 19:40:03 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_addContact(object):
    def setupUi(self, addContact):
        addContact.setObjectName("addContact")
        addContact.resize(QtCore.QSize(QtCore.QRect(0,0,285,146).size()).expandedTo(addContact.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(addContact)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.line = QtGui.QFrame(addContact)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,1,0,1,2)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton = QtGui.QPushButton(addContact)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)

        self.pushButton_2 = QtGui.QPushButton(addContact)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout.addWidget(self.pushButton_2)
        self.gridlayout.addLayout(self.hboxlayout,2,1,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(addContact)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_2 = QtGui.QLabel(addContact)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(addContact)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)
        self.hboxlayout1.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.jid = QtGui.QLineEdit(addContact)
        self.jid.setObjectName("jid")
        self.vboxlayout1.addWidget(self.jid)

        self.nickname = QtGui.QLineEdit(addContact)
        self.nickname.setObjectName("nickname")
        self.vboxlayout1.addWidget(self.nickname)

        self.group = QtGui.QComboBox(addContact)
        self.group.setEditable(True)
        self.group.setObjectName("group")
        self.vboxlayout1.addWidget(self.group)
        self.hboxlayout1.addLayout(self.vboxlayout1)
        self.gridlayout.addLayout(self.hboxlayout1,0,0,1,2)

        spacerItem = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.retranslateUi(addContact)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),addContact.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),addContact.reject)
        QtCore.QMetaObject.connectSlotsByName(addContact)

    def retranslateUi(self, addContact):
        addContact.setWindowTitle(QtGui.QApplication.translate("addContact", "Add Contact", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("addContact", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("addContact", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("addContact", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("addContact", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("addContact", "Group:", None, QtGui.QApplication.UnicodeUTF8))
