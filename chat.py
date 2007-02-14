# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created: Sat Feb 10 20:26:16 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_chat(object):
    def setupUi(self, chat):
        chat.setObjectName("chat")
        chat.resize(QtCore.QSize(QtCore.QRect(0,0,469,325).size()).expandedTo(chat.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(chat)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.chatTab = QtGui.QTabWidget(self.centralwidget)
        self.chatTab.setObjectName("chatTab")

        self.chat = QtGui.QWidget()
        self.chat.setObjectName("chat")
        self.chatTab.addTab(self.chat, "")
        self.gridlayout.addWidget(self.chatTab,0,0,1,1)
        chat.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(chat)
        self.menubar.setGeometry(QtCore.QRect(0,0,469,28))
        self.menubar.setObjectName("menubar")
        chat.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(chat)
        self.statusbar.setObjectName("statusbar")
        chat.setStatusBar(self.statusbar)

        self.retranslateUi(chat)
        QtCore.QMetaObject.connectSlotsByName(chat)

    def retranslateUi(self, chat):
        chat.setWindowTitle(QtGui.QApplication.translate("chat", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.chatTab.setTabText(self.chatTab.indexOf(self.chat), QtGui.QApplication.translate("chat", "Chat", None, QtGui.QApplication.UnicodeUTF8))
