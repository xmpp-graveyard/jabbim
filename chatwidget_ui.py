# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwidget.ui'
#
# Created: Fri Mar  2 21:55:12 2007
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

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.line = QtGui.QLineEdit(chatwidget)
        self.line.setAcceptDrops(True)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.smileys = QtGui.QToolButton(chatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.hboxlayout.addWidget(self.smileys)

        self.sendButton = QtGui.QPushButton(chatwidget)
        self.sendButton.setObjectName("sendButton")
        self.hboxlayout.addWidget(self.sendButton)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.textEdit = QtGui.QTextEdit(chatwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.hboxlayout1.addWidget(self.textEdit)
        self.gridlayout.addLayout(self.hboxlayout1,0,0,1,1)

        self.retranslateUi(chatwidget)
        QtCore.QMetaObject.connectSlotsByName(chatwidget)

    def retranslateUi(self, chatwidget):
        chatwidget.setWindowTitle(QtGui.QApplication.translate("chatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("chatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("chatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))

