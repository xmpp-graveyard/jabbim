# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/mainWindow.ui'
#
# Created: Sat Nov  3 17:19:11 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,268,536).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.rosterStackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.rosterStackedWidget.setObjectName("rosterStackedWidget")

        self.login = QtGui.QWidget()
        self.login.setObjectName("login")

        self.gridlayout1 = QtGui.QGridLayout(self.login)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.login_jidLabel = QtGui.QLabel(self.login)
        self.login_jidLabel.setObjectName("login_jidLabel")
        self.vboxlayout.addWidget(self.login_jidLabel)

        self.login_passwordLabel = QtGui.QLabel(self.login)
        self.login_passwordLabel.setObjectName("login_passwordLabel")
        self.vboxlayout.addWidget(self.login_passwordLabel)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.login_jid = QtGui.QLineEdit(self.login)
        self.login_jid.setObjectName("login_jid")
        self.vboxlayout1.addWidget(self.login_jid)

        self.login_password = QtGui.QLineEdit(self.login)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.vboxlayout1.addWidget(self.login_password)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout1.addLayout(self.hboxlayout,3,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.registerButton = QtGui.QPushButton(self.login)
        self.registerButton.setObjectName("registerButton")
        self.hboxlayout1.addWidget(self.registerButton)

        self.login_connect = QtGui.QPushButton(self.login)
        self.login_connect.setObjectName("login_connect")
        self.hboxlayout1.addWidget(self.login_connect)

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.gridlayout1.addLayout(self.hboxlayout1,5,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem2)

        self.loginAvatar = QtGui.QLabel(self.login)
        self.loginAvatar.setMinimumSize(QtCore.QSize(128,128))
        self.loginAvatar.setMaximumSize(QtCore.QSize(128,128))
        self.loginAvatar.setObjectName("loginAvatar")
        self.hboxlayout2.addWidget(self.loginAvatar)

        spacerItem3 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem3)
        self.gridlayout1.addLayout(self.hboxlayout2,2,0,1,1)

        spacerItem4 = QtGui.QSpacerItem(20,331,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem4,6,0,1,1)

        self.line = QtGui.QFrame(self.login)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,1)

        self.login_headerLabel = QtGui.QLabel(self.login)
        self.login_headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.login_headerLabel.setObjectName("login_headerLabel")
        self.gridlayout1.addWidget(self.login_headerLabel,0,0,1,1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem5 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem5,0,0,2,1)

        self.login_savePassword_2 = QtGui.QCheckBox(self.login)
        self.login_savePassword_2.setObjectName("login_savePassword_2")
        self.gridlayout2.addWidget(self.login_savePassword_2,1,1,1,1)

        self.login_savePassword = QtGui.QCheckBox(self.login)
        self.login_savePassword.setObjectName("login_savePassword")
        self.gridlayout2.addWidget(self.login_savePassword,0,1,1,1)
        self.gridlayout1.addLayout(self.gridlayout2,4,0,1,1)

        self.login_logoLabel = QtGui.QLabel(self.login)
        self.login_logoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.login_logoLabel.setObjectName("login_logoLabel")
        self.gridlayout1.addWidget(self.login_logoLabel,8,0,1,1)

        self.label = QtGui.QLabel(self.login)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,7,0,1,1)
        self.rosterStackedWidget.addWidget(self.login)

        self.roster = QtGui.QWidget()
        self.roster.setObjectName("roster")

        self.gridlayout3 = QtGui.QGridLayout(self.roster)
        self.gridlayout3.setMargin(0)
        self.gridlayout3.setSpacing(0)
        self.gridlayout3.setObjectName("gridlayout3")

        self.tabWidget = QtGui.QTabWidget(self.roster)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName("tabWidget")

        self.rosterTab = QtGui.QWidget()
        self.rosterTab.setObjectName("rosterTab")

        self.gridlayout4 = QtGui.QGridLayout(self.rosterTab)
        self.gridlayout4.setMargin(0)
        self.gridlayout4.setSpacing(0)
        self.gridlayout4.setObjectName("gridlayout4")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setMargin(3)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.rosterSearchLabel = QtGui.QLabel(self.rosterTab)
        self.rosterSearchLabel.setObjectName("rosterSearchLabel")
        self.hboxlayout3.addWidget(self.rosterSearchLabel)

        self.rosterSearch = QtGui.QLineEdit(self.rosterTab)
        self.rosterSearch.setObjectName("rosterSearch")
        self.hboxlayout3.addWidget(self.rosterSearch)
        self.gridlayout4.addLayout(self.hboxlayout3,3,0,1,1)

        self.selectedItemStyle = QtGui.QWidget(self.rosterTab)
        self.selectedItemStyle.setObjectName("selectedItemStyle")
        self.gridlayout4.addWidget(self.selectedItemStyle,0,0,1,1)

        self.rosterWidget = QtGui.QWidget(self.rosterTab)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout4.addWidget(self.rosterWidget,4,0,1,1)

        self.groupStyleWidget = QtGui.QWidget(self.rosterTab)
        self.groupStyleWidget.setObjectName("groupStyleWidget")
        self.gridlayout4.addWidget(self.groupStyleWidget,1,0,1,1)

        self.userStyleWidget = QtGui.QWidget(self.rosterTab)
        self.userStyleWidget.setObjectName("userStyleWidget")
        self.gridlayout4.addWidget(self.userStyleWidget,2,0,1,1)
        self.tabWidget.addTab(self.rosterTab,QtGui.QIcon("images/16x16/categories/system-users.png"),"")

        self.bookmarksTab = QtGui.QWidget()
        self.bookmarksTab.setObjectName("bookmarksTab")

        self.gridlayout5 = QtGui.QGridLayout(self.bookmarksTab)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.bookmarks = QtGui.QTreeWidget(self.bookmarksTab)
        self.bookmarks.setAlternatingRowColors(True)
        self.bookmarks.setRootIsDecorated(False)
        self.bookmarks.setObjectName("bookmarks")
        self.gridlayout5.addWidget(self.bookmarks,1,0,1,2)

        spacerItem6 = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem6,2,0,1,1)

        self.mucBrowserButton = QtGui.QPushButton(self.bookmarksTab)
        self.mucBrowserButton.setObjectName("mucBrowserButton")
        self.gridlayout5.addWidget(self.mucBrowserButton,2,1,1,1)

        self.bookmarks_headerLabel = QtGui.QLabel(self.bookmarksTab)
        self.bookmarks_headerLabel.setObjectName("bookmarks_headerLabel")
        self.gridlayout5.addWidget(self.bookmarks_headerLabel,0,0,1,1)
        self.tabWidget.addTab(self.bookmarksTab,QtGui.QIcon("images/16x16/categories/bookmarks.png"),"")

        self.eventsTab = QtGui.QWidget()
        self.eventsTab.setObjectName("eventsTab")

        self.gridlayout6 = QtGui.QGridLayout(self.eventsTab)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.eventsListWidget = QtGui.QListWidget(self.eventsTab)
        self.eventsListWidget.setObjectName("eventsListWidget")
        self.gridlayout6.addWidget(self.eventsListWidget,0,0,1,1)
        self.tabWidget.addTab(self.eventsTab,QtGui.QIcon("images/16x16/categories/event.png"),"")
        self.gridlayout3.addWidget(self.tabWidget,1,0,1,1)

        self.frame = QtGui.QFrame(self.roster)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")

        self.gridlayout7 = QtGui.QGridLayout(self.frame)
        self.gridlayout7.setMargin(0)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        spacerItem7 = QtGui.QSpacerItem(161,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout7.addItem(spacerItem7,1,1,1,2)

        self.statusButton = QtGui.QToolButton(self.frame)
        self.statusButton.setMaximumSize(QtCore.QSize(16777215,20))
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.gridlayout7.addWidget(self.statusButton,1,5,1,1)

        self.selfAvatar = QtGui.QLabel(self.frame)
        self.selfAvatar.setMargin(2)
        self.selfAvatar.setObjectName("selfAvatar")
        self.gridlayout7.addWidget(self.selfAvatar,0,0,2,1)

        self.showOffline = QtGui.QToolButton(self.frame)
        self.showOffline.setMaximumSize(QtCore.QSize(16777215,20))
        self.showOffline.setIcon(QtGui.QIcon("images/16x16/status/jabber-not_in_roster.png"))
        self.showOffline.setCheckable(True)
        self.showOffline.setArrowType(QtCore.Qt.NoArrow)
        self.showOffline.setObjectName("showOffline")
        self.gridlayout7.addWidget(self.showOffline,1,4,1,1)

        self.selfName = QtGui.QLabel(self.frame)
        self.selfName.setObjectName("selfName")
        self.gridlayout7.addWidget(self.selfName,0,1,1,4)

        self.toggleInvisible = QtGui.QToolButton(self.frame)
        self.toggleInvisible.setMaximumSize(QtCore.QSize(16777215,20))
        self.toggleInvisible.setIcon(QtGui.QIcon("images/16x16/status/jabber-invisible.png"))
        self.toggleInvisible.setCheckable(True)
        self.toggleInvisible.setArrowType(QtCore.Qt.NoArrow)
        self.toggleInvisible.setObjectName("toggleInvisible")
        self.gridlayout7.addWidget(self.toggleInvisible,1,3,1,1)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setObjectName("hboxlayout4")
        self.gridlayout7.addLayout(self.hboxlayout4,2,0,1,6)
        self.gridlayout3.addWidget(self.frame,0,0,1,1)
        self.rosterStackedWidget.addWidget(self.roster)

        self.splash = QtGui.QWidget()
        self.splash.setObjectName("splash")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.splash)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.splashImage = QtGui.QLabel(self.splash)
        self.splashImage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.splashImage.setObjectName("splashImage")
        self.vboxlayout2.addWidget(self.splashImage)

        self.splashProgress = QtGui.QProgressBar(self.splash)
        self.splashProgress.setProperty("value",QtCore.QVariant(0))
        self.splashProgress.setTextVisible(False)
        self.splashProgress.setOrientation(QtCore.Qt.Horizontal)
        self.splashProgress.setInvertedAppearance(False)
        self.splashProgress.setObjectName("splashProgress")
        self.vboxlayout2.addWidget(self.splashProgress)
        self.rosterStackedWidget.addWidget(self.splash)
        self.gridlayout.addWidget(self.rosterStackedWidget,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,268,29))
        self.menubar.setObjectName("menubar")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuPlugins = QtGui.QMenu(self.menubar)
        self.menuPlugins.setObjectName("menuPlugins")

        self.menuAkce = QtGui.QMenu(self.menubar)
        self.menuAkce.setObjectName("menuAkce")
        MainWindow.setMenuBar(self.menubar)

        self.actionShow_XML = QtGui.QAction(MainWindow)
        self.actionShow_XML.setObjectName("actionShow_XML")

        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionJoin_Groupchat = QtGui.QAction(MainWindow)
        self.actionJoin_Groupchat.setIcon(QtGui.QIcon("images/16x16/categories/muc.png"))
        self.actionJoin_Groupchat.setObjectName("actionJoin_Groupchat")

        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.actionAdd_Contact = QtGui.QAction(MainWindow)
        self.actionAdd_Contact.setIcon(QtGui.QIcon("images/16x16/actions/add-user.png"))
        self.actionAdd_Contact.setObjectName("actionAdd_Contact")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.actionService_Discovery = QtGui.QAction(MainWindow)
        self.actionService_Discovery.setObjectName("actionService_Discovery")

        self.actionMUC_Browser = QtGui.QAction(MainWindow)
        self.actionMUC_Browser.setObjectName("actionMUC_Browser")
        self.menuHelp.addAction(self.actionAbout)
        self.menuAkce.addAction(self.actionJoin_Groupchat)
        self.menuAkce.addAction(self.actionAdd_Contact)
        self.menuAkce.addAction(self.actionService_Discovery)
        self.menuAkce.addAction(self.actionShow_XML)
        self.menuAkce.addSeparator()
        self.menuAkce.addAction(self.actionPreferences)
        self.menuAkce.addSeparator()
        self.menuAkce.addAction(self.actionQuit)
        self.menubar.addAction(self.menuAkce.menuAction())
        self.menubar.addAction(self.menuPlugins.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.rosterStackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.login_password,QtCore.SIGNAL("returnPressed()"),self.login_connect.click)
        QtCore.QObject.connect(self.login_jid,QtCore.SIGNAL("returnPressed()"),self.login_connect.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.login_jidLabel.setText(QtGui.QApplication.translate("MainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.login_passwordLabel.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.registerButton.setText(QtGui.QApplication.translate("MainWindow", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_headerLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; font-weight:600;\">Connect</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword_2.setText(QtGui.QApplication.translate("MainWindow", "Auto connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword.setText(QtGui.QApplication.translate("MainWindow", "Save Password", None, QtGui.QApplication.UnicodeUTF8))
        self.rosterSearchLabel.setText(QtGui.QApplication.translate("MainWindow", "User search:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rosterTab), QtGui.QApplication.translate("MainWindow", " r", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.rosterTab),QtGui.QApplication.translate("MainWindow", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Jid", None, QtGui.QApplication.UnicodeUTF8))
        self.mucBrowserButton.setText(QtGui.QApplication.translate("MainWindow", "MUC Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks_headerLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'DejaVu Sans\';\"><span style=\" font-size:12pt; font-weight:600;\">Bookmarks</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bookmarksTab), QtGui.QApplication.translate("MainWindow", "b", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.bookmarksTab),QtGui.QApplication.translate("MainWindow", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.eventsTab), QtGui.QApplication.translate("MainWindow", "Events", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.eventsTab),QtGui.QApplication.translate("MainWindow", "Events", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Here you can change your status", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setToolTip(QtGui.QApplication.translate("MainWindow", "You can show/hide contats that are unavailable", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleInvisible.setToolTip(QtGui.QApplication.translate("MainWindow", "Toggle Invisibility", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlugins.setTitle(QtGui.QApplication.translate("MainWindow", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAkce.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_XML.setText(QtGui.QApplication.translate("MainWindow", "Show XML", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJoin_Groupchat.setText(QtGui.QApplication.translate("MainWindow", "Join Groupchat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Contact.setText(QtGui.QApplication.translate("MainWindow", "Add Contact", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionService_Discovery.setText(QtGui.QApplication.translate("MainWindow", "Service Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMUC_Browser.setText(QtGui.QApplication.translate("MainWindow", "MUC Browser", None, QtGui.QApplication.UnicodeUTF8))

