# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwidget.ui'
#
# Created: Thu Mar 15 11:04:18 2007
#      by: PyQt4 UI code generator 4.1.1
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

        self.line = QtGui.QTextEdit(chatwidget)
        self.line.setMaximumSize(QtCore.QSize(16777215,30))
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,2,0,1,1)

        self.sendButton = QtGui.QPushButton(chatwidget)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton,2,2,1,1)

        self.smileys = QtGui.QToolButton(chatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.gridlayout.addWidget(self.smileys,2,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.textEdit = QtGui.QTextEdit(chatwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.hboxlayout.addWidget(self.textEdit)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,3)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(chatwidget)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.avatar = QtGui.QLabel(chatwidget)
        self.avatar.setMaximumSize(QtCore.QSize(32,32))
        self.avatar.setObjectName("avatar")
        self.hboxlayout1.addWidget(self.avatar)
        self.gridlayout.addLayout(self.hboxlayout1,0,0,1,3)

        self.retranslateUi(chatwidget)
        QtCore.QMetaObject.connectSlotsByName(chatwidget)

    def retranslateUi(self, chatwidget):
        chatwidget.setWindowTitle(QtGui.QApplication.translate("chatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("chatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("chatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))

