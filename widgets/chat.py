# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/chat.ui'
#
# Created: Thu May 10 18:18:29 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_chatWindow(object):
    def setupUi(self, chatWindow):
        chatWindow.setObjectName("chatWindow")
        chatWindow.resize(QtCore.QSize(QtCore.QRect(0,0,581,562).size()).expandedTo(chatWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(chatWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.chatTab = QtGui.QTabWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chatTab.sizePolicy().hasHeightForWidth())
        self.chatTab.setSizePolicy(sizePolicy)
        self.chatTab.setObjectName("chatTab")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.chatTab.addTab(self.tab,"")
        self.gridlayout.addWidget(self.chatTab,0,0,1,1)
        chatWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(chatWindow)
        self.chatTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(chatWindow)

    def retranslateUi(self, chatWindow):
        chatWindow.setWindowTitle(QtGui.QApplication.translate("chatWindow", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.chatTab.setTabText(self.chatTab.indexOf(self.tab), QtGui.QApplication.translate("chatWindow", "Tab 1", None, QtGui.QApplication.UnicodeUTF8))

