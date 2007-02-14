# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Fri Feb  9 14:44:05 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_login(object):
    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(QtCore.QSize(QtCore.QRect(0,0,274,135).size()).expandedTo(login.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(login)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.close = QtGui.QPushButton(login)
        self.close.setObjectName("close")
        self.gridlayout.addWidget(self.close,2,3,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(login)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_2 = QtGui.QLabel(login)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.jid = QtGui.QLineEdit(login)
        self.jid.setObjectName("jid")
        self.vboxlayout1.addWidget(self.jid)

        self.password = QtGui.QLineEdit(login)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.vboxlayout1.addWidget(self.password)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,4)

        self.connect = QtGui.QPushButton(login)
        self.connect.setObjectName("connect")
        self.gridlayout.addWidget(self.connect,2,1,1,2)

        self.savePassword = QtGui.QCheckBox(login)
        self.savePassword.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.savePassword.setObjectName("savePassword")
        self.gridlayout.addWidget(self.savePassword,1,2,1,2)

        spacerItem1 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,1,0,1,2)

        self.retranslateUi(login)
        QtCore.QObject.connect(self.close,QtCore.SIGNAL("clicked()"),login.reject)
        QtCore.QObject.connect(self.connect,QtCore.SIGNAL("clicked()"),login.accept)
        QtCore.QMetaObject.connectSlotsByName(login)

    def retranslateUi(self, login):
        login.setWindowTitle(QtGui.QApplication.translate("login", "PyJim- Login", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("login", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("login", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("login", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.connect.setText(QtGui.QApplication.translate("login", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.savePassword.setText(QtGui.QApplication.translate("login", "Save password", None, QtGui.QApplication.UnicodeUTF8))
