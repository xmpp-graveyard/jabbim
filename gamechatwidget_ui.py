# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gamechatwidget.ui'
#
# Created: Thu Mar  1 20:14:27 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_gamechatwidget(object):
    def setupUi(self, gamechatwidget):
        gamechatwidget.setObjectName("gamechatwidget")
        gamechatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,491,383).size()).expandedTo(gamechatwidget.minimumSizeHint()))
        gamechatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(gamechatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.toolButton = QtGui.QToolButton(gamechatwidget)
        self.toolButton.setCheckable(True)
        self.toolButton.setArrowType(QtCore.Qt.DownArrow)
        self.toolButton.setObjectName("toolButton")
        self.gridlayout1.addWidget(self.toolButton,0,1,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.info = QtGui.QLineEdit(gamechatwidget)
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
        self.vboxlayout.addWidget(self.info)

        self.info_big = QtGui.QTextBrowser(gamechatwidget)
        self.info_big.setMaximumSize(QtCore.QSize(16777215,70))
        self.info_big.setObjectName("info_big")
        self.vboxlayout.addWidget(self.info_big)
        self.gridlayout1.addLayout(self.vboxlayout,0,0,2,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,2)

        self.textEdit = QtGui.QTextEdit(gamechatwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridlayout.addWidget(self.textEdit,1,0,1,1)

        self.listWidget = QtGui.QListWidget(gamechatwidget)
        self.listWidget.setMaximumSize(QtCore.QSize(130,16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,1,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.line = QtGui.QLineEdit(gamechatwidget)
        self.line.setAcceptDrops(True)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.smileys = QtGui.QToolButton(gamechatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/smileys/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.hboxlayout.addWidget(self.smileys)

        self.startGame = QtGui.QPushButton(gamechatwidget)
        self.startGame.setObjectName("startGame")
        self.hboxlayout.addWidget(self.startGame)

        self.sendButton = QtGui.QPushButton(gamechatwidget)
        self.sendButton.setObjectName("sendButton")
        self.hboxlayout.addWidget(self.sendButton)
        self.gridlayout.addLayout(self.hboxlayout,2,0,1,2)

        self.retranslateUi(gamechatwidget)
        QtCore.QObject.connect(self.toolButton,QtCore.SIGNAL("toggled(bool)"),self.info_big.setShown)
        QtCore.QObject.connect(self.toolButton,QtCore.SIGNAL("toggled(bool)"),self.info.setHidden)
        QtCore.QObject.connect(self.info,QtCore.SIGNAL("textChanged(QString)"),self.info_big.setText)
        QtCore.QMetaObject.connectSlotsByName(gamechatwidget)

    def retranslateUi(self, gamechatwidget):
        gamechatwidget.setWindowTitle(QtGui.QApplication.translate("gamechatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("gamechatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("gamechatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.startGame.setText(QtGui.QApplication.translate("gamechatwidget", "Start Game", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("gamechatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))

