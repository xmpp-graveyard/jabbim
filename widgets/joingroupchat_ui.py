# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'joingroupchat.ui'
#
# Created: Sun Oct 28 19:13:25 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_joingroupchat(object):
    def setupUi(self, joingroupchat):
        joingroupchat.setObjectName("joingroupchat")
        joingroupchat.resize(QtCore.QSize(QtCore.QRect(0,0,612,264).size()).expandedTo(joingroupchat.minimumSizeHint()))

        self.hboxlayout = QtGui.QHBoxLayout(joingroupchat)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setObjectName("hboxlayout")

        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.bookmark = QtGui.QCheckBox(joingroupchat)
        self.bookmark.setChecked(True)
        self.bookmark.setObjectName("bookmark")
        self.gridlayout.addWidget(self.bookmark,1,1,1,1)

        self.line = QtGui.QFrame(joingroupchat)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,2,0,1,2)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.pushButton = QtGui.QPushButton(joingroupchat)
        self.pushButton.setEnabled(False)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout1.addWidget(self.pushButton)

        self.pushButton_2 = QtGui.QPushButton(joingroupchat)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout1.addWidget(self.pushButton_2)
        self.gridlayout.addLayout(self.hboxlayout1,3,1,1,1)

        spacerItem = QtGui.QSpacerItem(93,23,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(0)
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
        self.hboxlayout2.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(0)
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
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.vboxlayout1.addWidget(self.password)
        self.hboxlayout2.addLayout(self.vboxlayout1)
        self.gridlayout.addLayout(self.hboxlayout2,0,0,1,2)

        spacerItem1 = QtGui.QSpacerItem(93,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem1,3,0,1,1)
        self.hboxlayout.addLayout(self.gridlayout)

        self.roomList = QtGui.QTreeWidget(joingroupchat)
        self.roomList.setFrameShadow(QtGui.QFrame.Sunken)
        self.roomList.setRootIsDecorated(True)
        self.roomList.setColumnCount(1)
        self.roomList.setObjectName("roomList")
        self.hboxlayout.addWidget(self.roomList)

        self.retranslateUi(joingroupchat)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),joingroupchat.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),joingroupchat.reject)
        QtCore.QMetaObject.connectSlotsByName(joingroupchat)

    def retranslateUi(self, joingroupchat):
        joingroupchat.setWindowTitle(QtGui.QApplication.translate("joingroupchat", "Join Group Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark.setToolTip(QtGui.QApplication.translate("joingroupchat", "Adds this room to your bookmarks. Bookmarks <br>are stored on the server.", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark.setText(QtGui.QApplication.translate("joingroupchat", "Bookmark this room", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("joingroupchat", "Join", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("joingroupchat", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("joingroupchat", "Room:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("joingroupchat", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("joingroupchat", "Conference name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("joingroupchat", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("joingroupchat", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.room.setToolTip(QtGui.QApplication.translate("joingroupchat", "Here fill in the name of the room you want to join in", None, QtGui.QApplication.UnicodeUTF8))
        self.server.setToolTip(QtGui.QApplication.translate("joingroupchat", "Server where the chat room is (e.g. conf.netlab.cz)", None, QtGui.QApplication.UnicodeUTF8))
        self.name.setToolTip(QtGui.QApplication.translate("joingroupchat", "This serves only for your orientation", None, QtGui.QApplication.UnicodeUTF8))
        self.nickname.setToolTip(QtGui.QApplication.translate("joingroupchat", "Under what name do you want to be <br>known to other participants", None, QtGui.QApplication.UnicodeUTF8))
        self.password.setToolTip(QtGui.QApplication.translate("joingroupchat", "You need password if the room is locked", None, QtGui.QApplication.UnicodeUTF8))
        self.roomList.headerItem().setText(0,QtGui.QApplication.translate("joingroupchat", "1", None, QtGui.QApplication.UnicodeUTF8))

