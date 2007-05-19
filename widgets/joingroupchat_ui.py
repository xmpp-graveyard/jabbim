# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'joingroupchat.ui'
#
# Created: Wed Feb 28 05:43:17 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_joingroupchat(object):
    def setupUi(self, joingroupchat):
        joingroupchat.setObjectName("joingroupchat")
        joingroupchat.resize(QtCore.QSize(QtCore.QRect(0,0,285,236).size()).expandedTo(joingroupchat.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(joingroupchat)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(111,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.bookmark = QtGui.QCheckBox(joingroupchat)
        self.bookmark.setChecked(True)
        self.bookmark.setObjectName("bookmark")
        self.gridlayout.addWidget(self.bookmark,1,1,1,1)

        self.line = QtGui.QFrame(joingroupchat)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,2,0,1,2)

        spacerItem1 = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,3,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(joingroupchat)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_3 = QtGui.QLabel(joingroupchat)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)

        self.label_4 = QtGui.QLabel(joingroupchat)
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)

        self.label_2 = QtGui.QLabel(joingroupchat)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.label_5 = QtGui.QLabel(joingroupchat)
        self.label_5.setObjectName("label_5")
        self.vboxlayout.addWidget(self.label_5)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.room = QtGui.QLineEdit(joingroupchat)
        self.room.setObjectName("room")
        self.vboxlayout1.addWidget(self.room)

        self.server = QtGui.QLineEdit(joingroupchat)
        self.server.setObjectName("server")
        self.vboxlayout1.addWidget(self.server)

        self.name = QtGui.QLineEdit(joingroupchat)
        self.name.setObjectName("name")
        self.vboxlayout1.addWidget(self.name)

        self.nickname = QtGui.QLineEdit(joingroupchat)
        self.nickname.setObjectName("nickname")
        self.vboxlayout1.addWidget(self.nickname)

        self.password = QtGui.QLineEdit(joingroupchat)
        self.password.setObjectName("password")
        self.vboxlayout1.addWidget(self.password)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,2)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.pushButton = QtGui.QPushButton(joingroupchat)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout1.addWidget(self.pushButton)

        self.pushButton_2 = QtGui.QPushButton(joingroupchat)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout1.addWidget(self.pushButton_2)
        self.gridlayout.addLayout(self.hboxlayout1,3,1,1,1)

        self.retranslateUi(joingroupchat)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),joingroupchat.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),joingroupchat.reject)
        QtCore.QMetaObject.connectSlotsByName(joingroupchat)

    def retranslateUi(self, joingroupchat):
        joingroupchat.setWindowTitle(QtGui.QApplication.translate("joingroupchat", "Join Group Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark.setText(QtGui.QApplication.translate("joingroupchat", "Bookmark this room", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("joingroupchat", "Room:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("joingroupchat", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("joingroupchat", "Conference name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("joingroupchat", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("joingroupchat", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("joingroupchat", "Join", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("joingroupchat", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

