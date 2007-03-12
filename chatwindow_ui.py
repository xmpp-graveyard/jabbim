# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatwindow.ui'
#
# Created: Mon Mar 12 08:15:36 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_chat(object):
    def setupUi(self, chat):
        chat.setObjectName("chat")
        chat.resize(QtCore.QSize(QtCore.QRect(0,0,469,325).size()).expandedTo(chat.minimumSizeHint()))
        chat.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(chat)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        chat.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(chat)
        self.menubar.setGeometry(QtCore.QRect(0,0,469,28))
        self.menubar.setObjectName("menubar")
        chat.setMenuBar(self.menubar)

        self.retranslateUi(chat)
        QtCore.QMetaObject.connectSlotsByName(chat)

    def retranslateUi(self, chat):
        chat.setWindowTitle(QtGui.QApplication.translate("chat", "Chat", None, QtGui.QApplication.UnicodeUTF8))

