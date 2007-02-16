# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Fri Feb 16 18:57:12 2007
#      by: PyQt4 UI code generator 4.0.1
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

        self.menuAction = QtGui.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")

        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")
        mainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.actionPreferences = QtGui.QAction(mainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.menuPreferences.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "PyJim", None, QtGui.QApplication.UnicodeUTF8))
        self.addContact.setText(QtGui.QApplication.translate("mainWindow", "Add Contact", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchat.setText(QtGui.QApplication.translate("mainWindow", "Group Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setText(QtGui.QApplication.translate("mainWindow", "Show Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("mainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("mainWindow", "Action", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
