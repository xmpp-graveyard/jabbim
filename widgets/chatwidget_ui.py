# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/chatwidget.ui'
#
# Created: Mon May 21 16:21:25 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_chatwidget(object):
    def setupUi(self, chatwidget):
        chatwidget.setObjectName("chatwidget")
        chatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,490,360).size()).expandedTo(chatwidget.minimumSizeHint()))
        chatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(chatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.smileys = QtGui.QToolButton(chatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.gridlayout.addWidget(self.smileys,2,1,1,1)

        self.sendButton = QtGui.QPushButton(chatwidget)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton,2,2,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(chatwidget)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.avatar = QtGui.QLabel(chatwidget)
        self.avatar.setMaximumSize(QtCore.QSize(32,32))
        self.avatar.setObjectName("avatar")
        self.hboxlayout.addWidget(self.avatar)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,3)

        self.textEdit = QtGui.QTextBrowser(chatwidget)
        self.textEdit.setOpenExternalLinks(True)
        self.textEdit.setObjectName("textEdit")
        self.gridlayout.addWidget(self.textEdit,1,0,1,3)

        self.retranslateUi(chatwidget)
        QtCore.QMetaObject.connectSlotsByName(chatwidget)

    def retranslateUi(self, chatwidget):
        chatwidget.setWindowTitle(QtGui.QApplication.translate("chatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("chatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("chatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))

