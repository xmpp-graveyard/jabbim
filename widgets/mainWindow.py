# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/mainWindow.ui'
#
# Created: Thu Jul 26 12:48:47 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,299,694).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.rosterStackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.rosterStackedWidget.setObjectName("rosterStackedWidget")

        self.login = QtGui.QWidget()
        self.login.setObjectName("login")

        self.gridlayout1 = QtGui.QGridLayout(self.login)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(20,331,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,5,0,1,1)

        self.login_logoLabel = QtGui.QLabel(self.login)
        self.login_logoLabel.setPixmap(QtGui.QPixmap("images/logo.png"))
        self.login_logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.login_logoLabel.setObjectName("login_logoLabel")
        self.gridlayout1.addWidget(self.login_logoLabel,6,0,1,1)

        self.login_headerLabel = QtGui.QLabel(self.login)
        self.login_headerLabel.setObjectName("login_headerLabel")
        self.gridlayout1.addWidget(self.login_headerLabel,0,0,1,1)

        self.line = QtGui.QFrame(self.login)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.login_jidLabel = QtGui.QLabel(self.login)
        self.login_jidLabel.setObjectName("login_jidLabel")
        self.vboxlayout.addWidget(self.login_jidLabel)

        self.login_passwordLabel = QtGui.QLabel(self.login)
        self.login_passwordLabel.setObjectName("login_passwordLabel")
        self.vboxlayout.addWidget(self.login_passwordLabel)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.login_jid = QtGui.QLineEdit(self.login)
        self.login_jid.setObjectName("login_jid")
        self.vboxlayout1.addWidget(self.login_jid)

        self.login_password = QtGui.QLineEdit(self.login)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.vboxlayout1.addWidget(self.login_password)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout1.addLayout(self.hboxlayout,2,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem1 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)

        self.login_savePassword = QtGui.QCheckBox(self.login)
        self.login_savePassword.setObjectName("login_savePassword")
        self.hboxlayout1.addWidget(self.login_savePassword)
        self.gridlayout1.addLayout(self.hboxlayout1,3,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem2 = QtGui.QSpacerItem(151,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem2)

        self.login_connect = QtGui.QPushButton(self.login)
        self.login_connect.setObjectName("login_connect")
        self.hboxlayout2.addWidget(self.login_connect)
        self.gridlayout1.addLayout(self.hboxlayout2,4,0,1,1)
        self.rosterStackedWidget.addWidget(self.login)

        self.roster = QtGui.QWidget()
        self.roster.setObjectName("roster")

        self.gridlayout2 = QtGui.QGridLayout(self.roster)
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(0)
        self.gridlayout2.setObjectName("gridlayout2")

        self.tabWidget = QtGui.QTabWidget(self.roster)
        self.tabWidget.setObjectName("tabWidget")

        self.rosterTab = QtGui.QWidget()
        self.rosterTab.setObjectName("rosterTab")

        self.gridlayout3 = QtGui.QGridLayout(self.rosterTab)
        self.gridlayout3.setMargin(0)
        self.gridlayout3.setSpacing(0)
        self.gridlayout3.setObjectName("gridlayout3")

        self.groupStyleWidget = QtGui.QWidget(self.rosterTab)
        self.groupStyleWidget.setObjectName("groupStyleWidget")
        self.gridlayout3.addWidget(self.groupStyleWidget,0,0,1,1)

        self.rosterWidget = QtGui.QWidget(self.rosterTab)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout3.addWidget(self.rosterWidget,2,0,1,1)

        self.userStyleWidget = QtGui.QWidget(self.rosterTab)
        self.userStyleWidget.setObjectName("userStyleWidget")
        self.gridlayout3.addWidget(self.userStyleWidget,1,0,1,1)
        self.tabWidget.addTab(self.rosterTab,QtGui.QIcon("images/16x16/categories/system-users.png"),"")

        self.addContactTab = QtGui.QWidget()
        self.addContactTab.setObjectName("addContactTab")

        self.gridlayout4 = QtGui.QGridLayout(self.addContactTab)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        spacerItem3 = QtGui.QSpacerItem(20,261,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem3,3,0,1,1)

        self.gridlayout5 = QtGui.QGridLayout()
        self.gridlayout5.setMargin(0)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.add_messageLabel = QtGui.QLabel(self.addContactTab)
        self.add_messageLabel.setObjectName("add_messageLabel")
        self.gridlayout5.addWidget(self.add_messageLabel,0,0,1,1)

        self.add_message = QtGui.QTextEdit(self.addContactTab)
        self.add_message.setObjectName("add_message")
        self.gridlayout5.addWidget(self.add_message,1,0,1,2)

        spacerItem4 = QtGui.QSpacerItem(191,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem4,0,1,1,1)
        self.gridlayout4.addLayout(self.gridlayout5,2,0,1,2)

        self.addContactLine = QtGui.QFrame(self.addContactTab)
        self.addContactLine.setFrameShape(QtGui.QFrame.HLine)
        self.addContactLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.addContactLine.setObjectName("addContactLine")
        self.gridlayout4.addWidget(self.addContactLine,4,0,2,2)

        spacerItem5 = QtGui.QSpacerItem(101,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem5,6,0,1,1)

        self.addContact = QtGui.QPushButton(self.addContactTab)
        self.addContact.setObjectName("addContact")
        self.gridlayout4.addWidget(self.addContact,5,1,2,1)

        self.addContact_headerLabel = QtGui.QLabel(self.addContactTab)
        self.addContact_headerLabel.setObjectName("addContact_headerLabel")
        self.gridlayout4.addWidget(self.addContact_headerLabel,0,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.add_jidLabel = QtGui.QLabel(self.addContactTab)
        self.add_jidLabel.setObjectName("add_jidLabel")
        self.vboxlayout2.addWidget(self.add_jidLabel)

        self.add_nicknameLabel = QtGui.QLabel(self.addContactTab)
        self.add_nicknameLabel.setObjectName("add_nicknameLabel")
        self.vboxlayout2.addWidget(self.add_nicknameLabel)

        self.add_groupLabel = QtGui.QLabel(self.addContactTab)
        self.add_groupLabel.setObjectName("add_groupLabel")
        self.vboxlayout2.addWidget(self.add_groupLabel)
        self.hboxlayout3.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.add_jid = QtGui.QLineEdit(self.addContactTab)
        self.add_jid.setObjectName("add_jid")
        self.vboxlayout3.addWidget(self.add_jid)

        self.add_nickname = QtGui.QLineEdit(self.addContactTab)
        self.add_nickname.setObjectName("add_nickname")
        self.vboxlayout3.addWidget(self.add_nickname)

        self.add_group = QtGui.QComboBox(self.addContactTab)
        self.add_group.setEditable(True)
        self.add_group.setObjectName("add_group")
        self.vboxlayout3.addWidget(self.add_group)
        self.hboxlayout3.addLayout(self.vboxlayout3)
        self.gridlayout4.addLayout(self.hboxlayout3,1,0,1,2)
        self.tabWidget.addTab(self.addContactTab,QtGui.QIcon("images/16x16/actions/add-user.png"),"")

        self.bookmarksTab = QtGui.QWidget()
        self.bookmarksTab.setObjectName("bookmarksTab")

        self.gridlayout6 = QtGui.QGridLayout(self.bookmarksTab)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.bookmarks = QtGui.QTreeWidget(self.bookmarksTab)
        self.bookmarks.setAlternatingRowColors(True)
        self.bookmarks.setRootIsDecorated(False)
        self.bookmarks.setObjectName("bookmarks")
        self.gridlayout6.addWidget(self.bookmarks,1,0,1,2)

        spacerItem6 = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem6,2,0,1,1)

        self.newBookmark = QtGui.QPushButton(self.bookmarksTab)
        self.newBookmark.setObjectName("newBookmark")
        self.gridlayout6.addWidget(self.newBookmark,2,1,1,1)

        self.bookmarks_headerLabel = QtGui.QLabel(self.bookmarksTab)
        self.bookmarks_headerLabel.setObjectName("bookmarks_headerLabel")
        self.gridlayout6.addWidget(self.bookmarks_headerLabel,0,0,1,1)
        self.tabWidget.addTab(self.bookmarksTab,QtGui.QIcon("images/16x16/categories/bookmarks.png"),"")

        self.eventsTab = QtGui.QWidget()
        self.eventsTab.setObjectName("eventsTab")

        self.gridlayout7 = QtGui.QGridLayout(self.eventsTab)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.eventsListWidget = QtGui.QListWidget(self.eventsTab)
        self.eventsListWidget.setObjectName("eventsListWidget")
        self.gridlayout7.addWidget(self.eventsListWidget,0,0,1,1)
        self.tabWidget.addTab(self.eventsTab,QtGui.QIcon("images/16x16/categories/event.png"),"")
        self.gridlayout2.addWidget(self.tabWidget,0,0,1,1)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setSpacing(6)
        self.hboxlayout4.setObjectName("hboxlayout4")

        self.showOffline = QtGui.QToolButton(self.roster)
        self.showOffline.setCheckable(True)
        self.showOffline.setArrowType(QtCore.Qt.NoArrow)
        self.showOffline.setObjectName("showOffline")
        self.hboxlayout4.addWidget(self.showOffline)

        spacerItem7 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem7)

        self.statusButton = QtGui.QToolButton(self.roster)
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.hboxlayout4.addWidget(self.statusButton)
        self.gridlayout2.addLayout(self.hboxlayout4,1,0,1,1)
        self.rosterStackedWidget.addWidget(self.roster)
        self.gridlayout.addWidget(self.rosterStackedWidget,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,299,29))
        self.menubar.setObjectName("menubar")

        self.menuPreferences = QtGui.QMenu(self.menubar)
        self.menuPreferences.setObjectName("menuPreferences")

        self.menuAkce = QtGui.QMenu(self.menubar)
        self.menuAkce.setObjectName("menuAkce")

        self.menuPlugins = QtGui.QMenu(self.menubar)
        self.menuPlugins.setObjectName("menuPlugins")
        MainWindow.setMenuBar(self.menubar)

        self.actionShow_XML = QtGui.QAction(MainWindow)
        self.actionShow_XML.setObjectName("actionShow_XML")

        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionJoin_Groupchat = QtGui.QAction(MainWindow)
        self.actionJoin_Groupchat.setObjectName("actionJoin_Groupchat")

        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuPreferences.addAction(self.actionPreferences)
        self.menuAkce.addAction(self.actionJoin_Groupchat)
        self.menuAkce.addAction(self.actionShow_XML)
        self.menuAkce.addSeparator()
        self.menuAkce.addAction(self.actionQuit)
        self.menubar.addAction(self.menuAkce.menuAction())
        self.menubar.addAction(self.menuPlugins.menuAction())
        self.menubar.addAction(self.menuPreferences.menuAction())

        self.retranslateUi(MainWindow)
        self.rosterStackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.login_headerLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; font-weight:600;\">Connect</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.login_jidLabel.setText(QtGui.QApplication.translate("MainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.login_passwordLabel.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword.setText(QtGui.QApplication.translate("MainWindow", "Save Password", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rosterTab), QtGui.QApplication.translate("MainWindow", " r", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.rosterTab),QtGui.QApplication.translate("MainWindow", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.add_messageLabel.setText(QtGui.QApplication.translate("MainWindow", "Message:", None, QtGui.QApplication.UnicodeUTF8))
        self.addContact.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.addContact_headerLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Add contact</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.add_jidLabel.setText(QtGui.QApplication.translate("MainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.add_nicknameLabel.setText(QtGui.QApplication.translate("MainWindow", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.add_groupLabel.setText(QtGui.QApplication.translate("MainWindow", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.addContactTab), QtGui.QApplication.translate("MainWindow", "a", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.addContactTab),QtGui.QApplication.translate("MainWindow", "Add Contact", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Jid", None, QtGui.QApplication.UnicodeUTF8))
        self.newBookmark.setText(QtGui.QApplication.translate("MainWindow", "New bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks_headerLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'DejaVu Sans\';\"><span style=\" font-size:12pt; font-weight:600;\">Bookmarks</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bookmarksTab), QtGui.QApplication.translate("MainWindow", "b", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.bookmarksTab),QtGui.QApplication.translate("MainWindow", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.eventsTab), QtGui.QApplication.translate("MainWindow", "Events", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setText(QtGui.QApplication.translate("MainWindow", "Show offline", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("MainWindow", "Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPreferences.setTitle(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAkce.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlugins.setTitle(QtGui.QApplication.translate("MainWindow", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_XML.setText(QtGui.QApplication.translate("MainWindow", "Show XML", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJoin_Groupchat.setText(QtGui.QApplication.translate("MainWindow", "Join Groupchat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

