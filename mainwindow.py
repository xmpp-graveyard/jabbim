# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Mar  3 19:15:47 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,235,510).size()).expandedTo(mainWindow.minimumSizeHint()))
        mainWindow.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.vboxlayout = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.rosterWidget = QtGui.QWidget(self.tab)
        self.rosterWidget.setObjectName("rosterWidget")
        self.vboxlayout.addWidget(self.rosterWidget)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout1 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.line = QtGui.QFrame(self.tab_2)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,3,0,2,2)

        spacerItem = QtGui.QSpacerItem(101,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,5,0,1,1)

        self.addContact = QtGui.QPushButton(self.tab_2)
        self.addContact.setObjectName("addContact")
        self.gridlayout1.addWidget(self.addContact,4,1,2,1)

        spacerItem1 = QtGui.QSpacerItem(20,181,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,2,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.label_2 = QtGui.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.vboxlayout1.addWidget(self.label_3)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.jid = QtGui.QLineEdit(self.tab_2)
        self.jid.setObjectName("jid")
        self.vboxlayout2.addWidget(self.jid)

        self.nickname = QtGui.QLineEdit(self.tab_2)
        self.nickname.setObjectName("nickname")
        self.vboxlayout2.addWidget(self.nickname)

        self.group = QtGui.QComboBox(self.tab_2)
        self.group.setEditable(True)
        self.group.setObjectName("group")
        self.vboxlayout2.addWidget(self.group)
        self.hboxlayout.addLayout(self.vboxlayout2)
        self.gridlayout1.addLayout(self.hboxlayout,1,0,1,2)

        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,0,0,1,1)
        self.tabWidget.addTab(self.tab_2,QtGui.QIcon("images/16x16/actions/add-user.png"),"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.groupchat = QtGui.QTreeWidget(self.tab_3)
        self.groupchat.setAlternatingRowColors(True)
        self.groupchat.setObjectName("groupchat")
        self.gridlayout2.addWidget(self.groupchat,1,0,1,2)

        spacerItem2 = QtGui.QSpacerItem(61,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2,2,0,1,1)

        self.getGroupchatList = QtGui.QPushButton(self.tab_3)
        self.getGroupchatList.setEnabled(False)
        self.getGroupchatList.setIcon(QtGui.QIcon("images/16x16/actions/reload.png"))
        self.getGroupchatList.setObjectName("getGroupchatList")
        self.gridlayout2.addWidget(self.getGroupchatList,2,1,1,1)

        self.label_5 = QtGui.QLabel(self.tab_3)
        self.label_5.setObjectName("label_5")
        self.gridlayout2.addWidget(self.label_5,0,0,1,2)
        self.tabWidget.addTab(self.tab_3,QtGui.QIcon("images/16x16/categories/muc.png"),"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.bookmarks = QtGui.QTreeWidget(self.tab_4)
        self.bookmarks.setAlternatingRowColors(True)
        self.bookmarks.setObjectName("bookmarks")
        self.gridlayout3.addWidget(self.bookmarks,1,0,1,1)

        self.label_6 = QtGui.QLabel(self.tab_4)
        self.label_6.setObjectName("label_6")
        self.gridlayout3.addWidget(self.label_6,0,0,1,1)
        self.tabWidget.addTab(self.tab_4,QtGui.QIcon("images/16x16/categories/bookmarks.png"),"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)

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

        spacerItem3 = QtGui.QSpacerItem(16,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem3)

        self.statusButton = QtGui.QToolButton(self.centralwidget)
        self.statusButton.setIcon(QtGui.QIcon("images/status/online.png"))
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.hboxlayout1.addWidget(self.statusButton)
        self.gridlayout.addLayout(self.hboxlayout1,1,0,1,1)
        mainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,235,28))
        self.menubar.setObjectName("menubar")

        self.menuJGames = QtGui.QMenu(self.menubar)
        self.menuJGames.setObjectName("menuJGames")

        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")

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

        self.actionEvents = QtGui.QAction(mainWindow)
        self.actionEvents.setObjectName("actionEvents")
        self.menuPreferences.addAction(self.actionPreferences)
        self.menuAction.addAction(self.actionAdd_contact)
        self.menuAction.addAction(self.actionGroup_Chat)
        self.menuAction.addAction(self.actionService_discovery)
        self.menuAction.addAction(self.actionEvents)
        self.menuAction.addSeparator()
        self.menuAction.addAction(self.actionQuit)
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())
        self.menubar.addAction(self.menuJGames.menuAction())
        self.toolBar.addAction(self.actionAdd_contact)

        self.retranslateUi(mainWindow)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("mainWindow", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.addContact.setText(QtGui.QApplication.translate("mainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("mainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("mainWindow", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("mainWindow", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("mainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Add contact</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("mainWindow", " ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_2),QtGui.QApplication.translate("mainWindow", "Add contact", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchat.headerItem().setText(0,QtGui.QApplication.translate("mainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchat.headerItem().setText(1,QtGui.QApplication.translate("mainWindow", "Jid", None, QtGui.QApplication.UnicodeUTF8))
        self.getGroupchatList.setText(QtGui.QApplication.translate("mainWindow", "Get groupchat list", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("mainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Browse groupchats</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("mainWindow", " ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_3),QtGui.QApplication.translate("mainWindow", "Browse groupchats", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(0,QtGui.QApplication.translate("mainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(1,QtGui.QApplication.translate("mainWindow", "Jid", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("mainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Bookmarks</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("mainWindow", " ", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_4),QtGui.QApplication.translate("mainWindow", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setText(QtGui.QApplication.translate("mainWindow", "Show Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("mainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.menuJGames.setTitle(QtGui.QApplication.translate("mainWindow", "JGames", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("mainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("mainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionService_discovery.setText(QtGui.QApplication.translate("mainWindow", "Service discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("mainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_contact.setText(QtGui.QApplication.translate("mainWindow", "Add contact", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGroup_Chat.setText(QtGui.QApplication.translate("mainWindow", "Group Chat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTic_tac_toe.setText(QtGui.QApplication.translate("mainWindow", "Tic tac toe", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEvents.setText(QtGui.QApplication.translate("mainWindow", "Events", None, QtGui.QApplication.UnicodeUTF8))

