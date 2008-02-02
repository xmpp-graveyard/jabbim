# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/chat.ui'
#
# Created: Mon Nov 26 19:22:04 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_chatWindow(object):
    def setupUi(self, chatWindow):
        chatWindow.setObjectName("chatWindow")
        chatWindow.resize(QtCore.QSize(QtCore.QRect(0,0,581,562).size()).expandedTo(chatWindow.minimumSizeHint()))
        chatWindow.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(chatWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.chatTab = QtGui.QTabWidget(self.centralwidget)
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

