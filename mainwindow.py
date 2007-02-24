# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Feb 24 15:15:45 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,229,481).size()).expandedTo(mainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.addContact = QtGui.QToolButton(self.centralwidget)
        self.addContact.setObjectName("addContact")
        self.hboxlayout.addWidget(self.addContact)

        spacerItem = QtGui.QSpacerItem(121,25,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.groupchat = QtGui.QToolButton(self.centralwidget)
        self.groupchat.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.groupchat.setObjectName("groupchat")
        self.hboxlayout.addWidget(self.groupchat)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.showOffline = QtGui.QToolButton(self.centralwidget)
        self.showOffline.setIcon(QtGui.QIcon("images/status/offline.png"))
        self.showOffline.setCheckable(True)
        self.showOffline.setChecked(False)
        self.showOffline.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.showOffline.setObjectName("showOffline")
        self.hboxlayout1.addWidget(self.showOffline)

        spacerItem1 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)

        self.statusButton = QtGui.QToolButton(self.centralwidget)
        self.statusButton.setIcon(QtGui.QIcon("images/status/online.png"))
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.hboxlayout1.addWidget(self.statusButton)
        self.gridlayout.addLayout(self.hboxlayout1,2,0,1,1)

        self.rosterWidget = QtGui.QWidget(self.centralwidget)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout.addWidget(self.rosterWidget,1,0,1,1)
        mainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,229,28))
        self.menubar.setObjectName("menubar")

        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")

        self.menuAction = QtGui.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        mainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtGui.QToolBar(mainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        mainWindow.addToolBar(self.toolBar)

        self.actionPreferences = QtGui.QAction(mainWindow)
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionService_discovery = QtGui.QAction(mainWindow)
        self.actionService_discovery.setObjectName("actionService_discovery")

        self.actionQuit = QtGui.QAction(mainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.actionAdd_contact = QtGui.QAction(mainWindow)
        self.actionAdd_contact.setObjectName("actionAdd_contact")

        self.actionGroup_Chat = QtGui.QAction(mainWindow)
        self.actionGroup_Chat.setObjectName("actionGroup_Chat")
        self.menuPreferences.addAction(self.actionPreferences)
        self.menuAction.addAction(self.actionAdd_contact)
        self.menuAction.addAction(self.actionGroup_Chat)
        self.menuAction.addAction(self.actionService_discovery)
        self.menuAction.addSeparator()
        self.menuAction.addAction(self.actionQuit)
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.toolBar.addAction(self.actionAdd_contact)
        self.toolBar.addAction(self.actionGroup_Chat)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.addContact.setText(QtGui.QApplication.translate("mainWindow", "Add Contact", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchat.setText(QtGui.QApplication.translate("mainWindow", "Group Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setText(QtGui.QApplication.translate("mainWindow", "Show Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("mainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("mainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionService_discovery.setText(QtGui.QApplication.translate("mainWindow", "Service discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("mainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_contact.setText(QtGui.QApplication.translate("mainWindow", "Add contact", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGroup_Chat.setText(QtGui.QApplication.translate("mainWindow", "Group Chat", None, QtGui.QApplication.UnicodeUTF8))

