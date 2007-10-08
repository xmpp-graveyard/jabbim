# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwidget.ui'
#
# Created: Mon Oct  8 07:44:20 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_chatwidget(object):
    def setupUi(self, chatwidget):
        chatwidget.setObjectName("chatwidget")
        chatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,515,414).size()).expandedTo(chatwidget.minimumSizeHint()))
        chatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(chatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.chatstate = QtGui.QLabel(chatwidget)
        self.chatstate.setObjectName("chatstate")
        self.gridlayout.addWidget(self.chatstate,2,0,1,1)

        spacerItem = QtGui.QSpacerItem(311,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.smileys = QtGui.QToolButton(chatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.hboxlayout.addWidget(self.smileys)

        self.sendButton = QtGui.QPushButton(chatwidget)
        self.sendButton.setObjectName("sendButton")
        self.hboxlayout.addWidget(self.sendButton)
        self.gridlayout.addLayout(self.hboxlayout,2,2,1,1)

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

        self.splitter = QtGui.QSplitter(chatwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.viewWidget = QtGui.QWidget(self.splitter)
        self.viewWidget.setMinimumSize(QtCore.QSize(0,10))
        self.viewWidget.setObjectName("viewWidget")

        self.lineWidget = QtGui.QWidget(self.splitter)
        self.lineWidget.setMinimumSize(QtCore.QSize(0,10))
        self.lineWidget.setObjectName("lineWidget")
        self.gridlayout.addWidget(self.splitter,1,0,1,3)

        self.retranslateUi(chatwidget)
        QtCore.QMetaObject.connectSlotsByName(chatwidget)

    def retranslateUi(self, chatwidget):
        chatwidget.setWindowTitle(QtGui.QApplication.translate("chatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("chatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("chatwidget", "&Send", None, QtGui.QApplication.UnicodeUTF8))

