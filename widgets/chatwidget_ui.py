# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/chatwidget.ui'
#
# Created: Fri Oct 19 14:46:08 2007
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

        spacerItem = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,1,1,1)

        self.chatstate = QtGui.QLabel(chatwidget)
        self.chatstate.setObjectName("chatstate")
        self.gridlayout.addWidget(self.chatstate,1,0,1,1)

        self.splitter_2 = QtGui.QSplitter(chatwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.viewWidget = QtGui.QWidget(self.splitter)
        self.viewWidget.setMinimumSize(QtCore.QSize(0,10))
        self.viewWidget.setObjectName("viewWidget")

        self.lineWidget = QtGui.QWidget(self.splitter)
        self.lineWidget.setMinimumSize(QtCore.QSize(0,10))
        self.lineWidget.setObjectName("lineWidget")

        self.widget = QtGui.QWidget(self.splitter_2)
        self.widget.setObjectName("widget")

        self.vboxlayout = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(128,16777215))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.avatar = QtGui.QLabel(self.widget)
        self.avatar.setAlignment(QtCore.Qt.AlignCenter)
        self.avatar.setObjectName("avatar")
        self.vboxlayout.addWidget(self.avatar)

        spacerItem1 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem1)
        self.gridlayout.addWidget(self.splitter_2,0,0,1,3)

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
        self.gridlayout.addLayout(self.hboxlayout,1,2,1,1)

        self.retranslateUi(chatwidget)
        QtCore.QMetaObject.connectSlotsByName(chatwidget)

    def retranslateUi(self, chatwidget):
        chatwidget.setWindowTitle(QtGui.QApplication.translate("chatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("chatwidget", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("chatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("chatwidget", "&Send", None, QtGui.QApplication.UnicodeUTF8))

