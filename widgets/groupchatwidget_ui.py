# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/groupchatwidget.ui'
#
# Created: Sat May 19 13:39:47 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_groupchatwidget(object):
    def setupUi(self, groupchatwidget):
        groupchatwidget.setObjectName("groupchatwidget")
        groupchatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,487,351).size()).expandedTo(groupchatwidget.minimumSizeHint()))
        groupchatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(groupchatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.smileys = QtGui.QToolButton(groupchatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.gridlayout.addWidget(self.smileys,3,1,1,1)

        self.sendButton = QtGui.QPushButton(groupchatwidget)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton,3,2,1,1)

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.toolButton = QtGui.QToolButton(groupchatwidget)
        self.toolButton.setCheckable(True)
        self.toolButton.setArrowType(QtCore.Qt.DownArrow)
        self.toolButton.setObjectName("toolButton")
        self.gridlayout1.addWidget(self.toolButton,0,1,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.info = QtGui.QLineEdit(groupchatwidget)
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
        self.vboxlayout.addWidget(self.info)

        self.info_big = QtGui.QTextBrowser(groupchatwidget)
        self.info_big.setMaximumSize(QtCore.QSize(16777215,70))
        self.info_big.setObjectName("info_big")
        self.vboxlayout.addWidget(self.info_big)
        self.gridlayout1.addLayout(self.vboxlayout,0,0,2,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,3)

        self.users = QtGui.QTreeWidget(groupchatwidget)
        self.users.setMaximumSize(QtCore.QSize(141,16777215))
        self.users.setAlternatingRowColors(True)
        self.users.setRootIsDecorated(False)
        self.users.setObjectName("users")
        self.gridlayout.addWidget(self.users,1,1,1,2)

        self.admin = QtGui.QWidget(groupchatwidget)
        self.admin.setObjectName("admin")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.admin)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.roomAdmin = QtGui.QPushButton(self.admin)
        self.roomAdmin.setObjectName("roomAdmin")
        self.vboxlayout1.addWidget(self.roomAdmin)

        self.roomConfig = QtGui.QPushButton(self.admin)
        self.roomConfig.setObjectName("roomConfig")
        self.vboxlayout1.addWidget(self.roomConfig)
        self.gridlayout.addWidget(self.admin,2,1,1,2)

        self.textEdit = QtGui.QTextBrowser(groupchatwidget)
        self.textEdit.setOpenExternalLinks(True)
        self.textEdit.setObjectName("textEdit")
        self.gridlayout.addWidget(self.textEdit,1,0,2,1)

        self.line = QtGui.QLineEdit(groupchatwidget)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,3,0,1,1)

        self.retranslateUi(groupchatwidget)
        QtCore.QObject.connect(self.toolButton,QtCore.SIGNAL("toggled(bool)"),self.info_big.setShown)
        QtCore.QObject.connect(self.toolButton,QtCore.SIGNAL("toggled(bool)"),self.info.setHidden)
        QtCore.QObject.connect(self.info,QtCore.SIGNAL("textChanged(QString)"),self.info_big.setText)
        QtCore.QMetaObject.connectSlotsByName(groupchatwidget)

    def retranslateUi(self, groupchatwidget):
        groupchatwidget.setWindowTitle(QtGui.QApplication.translate("groupchatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("groupchatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("groupchatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("groupchatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(0,QtGui.QApplication.translate("groupchatwidget", "user", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(1,QtGui.QApplication.translate("groupchatwidget", "jid", None, QtGui.QApplication.UnicodeUTF8))
        self.roomAdmin.setText(QtGui.QApplication.translate("groupchatwidget", "Room administration", None, QtGui.QApplication.UnicodeUTF8))
        self.roomConfig.setText(QtGui.QApplication.translate("groupchatwidget", "Room configuration", None, QtGui.QApplication.UnicodeUTF8))

