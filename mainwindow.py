# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Mar  1 21:33:38 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,229,481).size()).expandedTo(mainWindow.minimumSizeHint()))
        mainWindow.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.rosterWidget = QtGui.QWidget(self.centralwidget)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout.addWidget(self.rosterWidget,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.showOffline = QtGui.QToolButton(self.centralwidget)
        self.showOffline.setIcon(QtGui.QIcon("images/status/offline.png"))
        self.showOffline.setCheckable(True)
        self.showOffline.setChecked(False)
        self.showOffline.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.showOffline.setObjectName("showOffline")
        self.hboxlayout.addWidget(self.showOffline)

        spacerItem = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.statusButton = QtGui.QToolButton(self.centralwidget)
        self.statusButton.setIcon(QtGui.QIcon("images/status/online.png"))
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.hboxlayout.addWidget(self.statusButton)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)
        mainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,229,28))
        self.menubar.setObjectName("menubar")

        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")

        self.menuJGames = QtGui.QMenu(self.menubar)
        self.menuJGames.setObjectName("menuJGames")

        self.menuAction = QtGui.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        mainWindow.setMenuBar(self.menubar)

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

        self.actionTic_tac_toe = QtGui.QAction(mainWindow)
        self.actionTic_tac_toe.setObjectName("actionTic_tac_toe")
        self.menuPreferences.addAction(self.actionPreferences)
        self.menuAction.addAction(self.actionAdd_contact)
        self.menuAction.addAction(self.actionGroup_Chat)
        self.menuAction.addAction(self.actionService_discovery)
        self.menuAction.addSeparator()
        self.menuAction.addAction(self.actionQuit)
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuJGames.menuAction())
        self.toolBar.addAction(self.actionAdd_contact)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setText(QtGui.QApplication.translate("mainWindow", "Show Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("mainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuJGames.setTitle(QtGui.QApplication.translate("mainWindow", "JGames", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("mainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionService_discovery.setText(QtGui.QApplication.translate("mainWindow", "Service discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("mainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_contact.setText(QtGui.QApplication.translate("mainWindow", "Add contact", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGroup_Chat.setText(QtGui.QApplication.translate("mainWindow", "Group Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTic_tac_toe.setText(QtGui.QApplication.translate("mainWindow", "Tic tac toe", None, QtGui.QApplication.UnicodeUTF8))

