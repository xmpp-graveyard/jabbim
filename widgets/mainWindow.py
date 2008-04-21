# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/mainWindow.ui'
#
# Created: Mon Apr 21 15:16:53 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,335,682).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.rosterStackedWidget = QtGui.QStackedWidget(self.splitter)
        self.rosterStackedWidget.setObjectName("rosterStackedWidget")

        self.login = QtGui.QWidget()
        self.login.setObjectName("login")

        self.gridlayout1 = QtGui.QGridLayout(self.login)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,5,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)

        self.login_connect = QtGui.QPushButton(self.login)
        self.login_connect.setObjectName("login_connect")
        self.hboxlayout.addWidget(self.login_connect)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)
        self.gridlayout1.addLayout(self.hboxlayout,4,0,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(15)
        self.vboxlayout.setObjectName("vboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(2)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.login)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.login_jid = QtGui.QLineEdit(self.login)
        self.login_jid.setObjectName("login_jid")
        self.vboxlayout1.addWidget(self.login_jid)

        self.label_2 = QtGui.QLabel(self.login)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)

        self.login_password = QtGui.QLineEdit(self.login)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.vboxlayout1.addWidget(self.login_password)

        self.label_3 = QtGui.QLabel(self.login)
        self.label_3.setObjectName("label_3")
        self.vboxlayout1.addWidget(self.label_3)

        self.loginStatus = QtGui.QComboBox(self.login)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginStatus.sizePolicy().hasHeightForWidth())
        self.loginStatus.setSizePolicy(sizePolicy)
        self.loginStatus.setObjectName("loginStatus")
        self.vboxlayout1.addWidget(self.loginStatus)
        self.vboxlayout.addLayout(self.vboxlayout1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem3 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem3,0,0,2,1)

        self.login_autoconnect = QtGui.QCheckBox(self.login)
        self.login_autoconnect.setObjectName("login_autoconnect")
        self.gridlayout2.addWidget(self.login_autoconnect,1,1,1,1)

        self.login_savePassword = QtGui.QCheckBox(self.login)
        self.login_savePassword.setObjectName("login_savePassword")
        self.gridlayout2.addWidget(self.login_savePassword,0,1,1,1)
        self.vboxlayout.addLayout(self.gridlayout2)
        self.gridlayout1.addLayout(self.vboxlayout,3,0,1,1)

        self.profilesLine = QtGui.QFrame(self.login)
        self.profilesLine.setFrameShape(QtGui.QFrame.HLine)
        self.profilesLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.profilesLine.setObjectName("profilesLine")
        self.gridlayout1.addWidget(self.profilesLine,7,0,1,1)

        self.line = QtGui.QFrame(self.login)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem4)

        self.loginAvatar = QtGui.QLabel(self.login)
        self.loginAvatar.setMinimumSize(QtCore.QSize(128,128))
        self.loginAvatar.setMaximumSize(QtCore.QSize(128,128))
        self.loginAvatar.setObjectName("loginAvatar")
        self.hboxlayout1.addWidget(self.loginAvatar)

        spacerItem5 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem5)
        self.gridlayout1.addLayout(self.hboxlayout1,2,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem6 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem6)

        self.registerButton = QtGui.QPushButton(self.login)
        self.registerButton.setObjectName("registerButton")
        self.hboxlayout2.addWidget(self.registerButton)

        spacerItem7 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem7)
        self.gridlayout1.addLayout(self.hboxlayout2,9,0,1,1)

        self.login_headerLabel = QtGui.QLabel(self.login)
        self.login_headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.login_headerLabel.setObjectName("login_headerLabel")
        self.gridlayout1.addWidget(self.login_headerLabel,0,0,1,1)

        self.profilesHeader = QtGui.QLabel(self.login)
        self.profilesHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.profilesHeader.setObjectName("profilesHeader")
        self.gridlayout1.addWidget(self.profilesHeader,6,0,1,1)

        self.profilesList = QtGui.QComboBox(self.login)
        self.profilesList.setIconSize(QtCore.QSize(22,22))
        self.profilesList.setObjectName("profilesList")
        self.gridlayout1.addWidget(self.profilesList,8,0,1,1)
        self.rosterStackedWidget.addWidget(self.login)

        self.roster = QtGui.QWidget()
        self.roster.setObjectName("roster")

        self.gridlayout3 = QtGui.QGridLayout(self.roster)
        self.gridlayout3.setMargin(0)
        self.gridlayout3.setSpacing(0)
        self.gridlayout3.setObjectName("gridlayout3")

        self.frame = QtGui.QFrame(self.roster)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName("frame")

        self.gridlayout4 = QtGui.QGridLayout(self.frame)
        self.gridlayout4.setMargin(0)
        self.gridlayout4.setSpacing(4)
        self.gridlayout4.setObjectName("gridlayout4")

        self.selfAvatarWidget = QtGui.QWidget(self.frame)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selfAvatarWidget.sizePolicy().hasHeightForWidth())
        self.selfAvatarWidget.setSizePolicy(sizePolicy)
        self.selfAvatarWidget.setObjectName("selfAvatarWidget")
        self.gridlayout4.addWidget(self.selfAvatarWidget,0,0,3,1)

        self.statusWidget2 = QtGui.QWidget(self.frame)
        self.statusWidget2.setObjectName("statusWidget2")

        self.hboxlayout3 = QtGui.QHBoxLayout(self.statusWidget2)
        self.hboxlayout3.setSpacing(0)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.statusMessage = QtGui.QToolButton(self.statusWidget2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusMessage.sizePolicy().hasHeightForWidth())
        self.statusMessage.setSizePolicy(sizePolicy)
        self.statusMessage.setMaximumSize(QtCore.QSize(16777215,20))
        self.statusMessage.setIcon(QtGui.QIcon("images/16x16/status/jabber-not_in_roster.png"))
        self.statusMessage.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusMessage.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusMessage.setAutoRaise(True)
        self.statusMessage.setArrowType(QtCore.Qt.NoArrow)
        self.statusMessage.setObjectName("statusMessage")
        self.hboxlayout3.addWidget(self.statusMessage)
        self.gridlayout4.addWidget(self.statusWidget2,1,1,1,1)

        self.statusWidget = QtGui.QToolButton(self.frame)
        self.statusWidget.setMaximumSize(QtCore.QSize(16777215,20))
        self.statusWidget.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusWidget.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusWidget.setAutoRaise(True)
        self.statusWidget.setArrowType(QtCore.Qt.DownArrow)
        self.statusWidget.setObjectName("statusWidget")
        self.gridlayout4.addWidget(self.statusWidget,1,3,1,1)

        self.selfName = QtGui.QLabel(self.frame)
        self.selfName.setObjectName("selfName")
        self.gridlayout4.addWidget(self.selfName,0,1,1,4)

        self.hboxlayout4 = QtGui.QHBoxLayout()
        self.hboxlayout4.setSpacing(0)
        self.hboxlayout4.setMargin(0)
        self.hboxlayout4.setObjectName("hboxlayout4")

        spacerItem8 = QtGui.QSpacerItem(50,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout4.addItem(spacerItem8)

        self.offlineButton = QtGui.QToolButton(self.frame)
        self.offlineButton.setMaximumSize(QtCore.QSize(16777215,20))
        self.offlineButton.setIcon(QtGui.QIcon("images/16x16/status/jabber-offline.png"))
        self.offlineButton.setCheckable(True)
        self.offlineButton.setArrowType(QtCore.Qt.NoArrow)
        self.offlineButton.setObjectName("offlineButton")
        self.hboxlayout4.addWidget(self.offlineButton)

        self.toggleInvisible = QtGui.QToolButton(self.frame)
        self.toggleInvisible.setMaximumSize(QtCore.QSize(16777215,20))
        self.toggleInvisible.setIcon(QtGui.QIcon("images/16x16/status/jabber-invisible.png"))
        self.toggleInvisible.setCheckable(True)
        self.toggleInvisible.setArrowType(QtCore.Qt.NoArrow)
        self.toggleInvisible.setObjectName("toggleInvisible")
        self.hboxlayout4.addWidget(self.toggleInvisible)

        self.showOffline = QtGui.QToolButton(self.frame)
        self.showOffline.setMaximumSize(QtCore.QSize(16777215,20))
        self.showOffline.setIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))
        self.showOffline.setCheckable(True)
        self.showOffline.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.showOffline.setArrowType(QtCore.Qt.NoArrow)
        self.showOffline.setObjectName("showOffline")
        self.hboxlayout4.addWidget(self.showOffline)

        self.moodButton = QtGui.QToolButton(self.frame)
        self.moodButton.setMaximumSize(QtCore.QSize(16777215,20))
        self.moodButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.moodButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.moodButton.setObjectName("moodButton")
        self.hboxlayout4.addWidget(self.moodButton)

        self.statusButton = QtGui.QToolButton(self.frame)
        self.statusButton.setMaximumSize(QtCore.QSize(16777215,20))
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.hboxlayout4.addWidget(self.statusButton)
        self.gridlayout4.addLayout(self.hboxlayout4,2,1,1,3)

        self.statusLine = QtGui.QLineEdit(self.frame)
        self.statusLine.setObjectName("statusLine")
        self.gridlayout4.addWidget(self.statusLine,1,2,1,1)
        self.gridlayout3.addWidget(self.frame,0,0,1,1)

        self.tabWidget = QtGui.QTabWidget(self.roster)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName("tabWidget")

        self.rosterTab = QtGui.QWidget()
        self.rosterTab.setObjectName("rosterTab")

        self.gridlayout5 = QtGui.QGridLayout(self.rosterTab)
        self.gridlayout5.setMargin(0)
        self.gridlayout5.setSpacing(0)
        self.gridlayout5.setObjectName("gridlayout5")

        self.hboxlayout5 = QtGui.QHBoxLayout()
        self.hboxlayout5.setSpacing(6)
        self.hboxlayout5.setMargin(0)
        self.hboxlayout5.setObjectName("hboxlayout5")

        self.rosterSearchLabel = QtGui.QLabel(self.rosterTab)
        self.rosterSearchLabel.setObjectName("rosterSearchLabel")
        self.hboxlayout5.addWidget(self.rosterSearchLabel)

        self.rosterSearch = QtGui.QLineEdit(self.rosterTab)
        self.rosterSearch.setObjectName("rosterSearch")
        self.hboxlayout5.addWidget(self.rosterSearch)
        self.gridlayout5.addLayout(self.hboxlayout5,3,0,1,1)

        self.selectedItemStyle = QtGui.QWidget(self.rosterTab)
        self.selectedItemStyle.setObjectName("selectedItemStyle")
        self.gridlayout5.addWidget(self.selectedItemStyle,0,0,1,1)

        self.rosterWidget = QtGui.QWidget(self.rosterTab)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout5.addWidget(self.rosterWidget,4,0,1,1)

        self.groupStyleWidget = QtGui.QWidget(self.rosterTab)
        self.groupStyleWidget.setObjectName("groupStyleWidget")
        self.gridlayout5.addWidget(self.groupStyleWidget,1,0,1,1)

        self.userStyleWidget = QtGui.QWidget(self.rosterTab)
        self.userStyleWidget.setObjectName("userStyleWidget")
        self.gridlayout5.addWidget(self.userStyleWidget,2,0,1,1)
        self.tabWidget.addTab(self.rosterTab,QtGui.QIcon("images/16x16/categories/system-users.png"),"")

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

        spacerItem9 = QtGui.QSpacerItem(131,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout6.addItem(spacerItem9,2,0,1,1)

        self.mucBrowserButton = QtGui.QPushButton(self.bookmarksTab)
        self.mucBrowserButton.setObjectName("mucBrowserButton")
        self.gridlayout6.addWidget(self.mucBrowserButton,2,1,1,1)

        self.bookmarks_headerLabel = QtGui.QLabel(self.bookmarksTab)
        self.bookmarks_headerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.bookmarks_headerLabel.setObjectName("bookmarks_headerLabel")
        self.gridlayout6.addWidget(self.bookmarks_headerLabel,0,0,1,2)
        self.tabWidget.addTab(self.bookmarksTab,QtGui.QIcon("images/16x16/categories/bookmarks.png"),"")

        self.eventsTab = QtGui.QWidget()
        self.eventsTab.setObjectName("eventsTab")

        self.gridlayout7 = QtGui.QGridLayout(self.eventsTab)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.eventsListWidget = QtGui.QListWidget(self.eventsTab)
        self.eventsListWidget.setObjectName("eventsListWidget")
        self.gridlayout7.addWidget(self.eventsListWidget,1,0,1,1)

        self.eventsLabel = QtGui.QLabel(self.eventsTab)
        self.eventsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.eventsLabel.setObjectName("eventsLabel")
        self.gridlayout7.addWidget(self.eventsLabel,0,0,1,1)
        self.tabWidget.addTab(self.eventsTab,QtGui.QIcon("images/16x16/categories/event.png"),"")
        self.gridlayout3.addWidget(self.tabWidget,1,0,1,1)
        self.rosterStackedWidget.addWidget(self.roster)

        self.splash = QtGui.QWidget()
        self.splash.setObjectName("splash")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.splash)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setObjectName("vboxlayout2")

        spacerItem10 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout2.addItem(spacerItem10)

        self.splashImage = QtGui.QLabel(self.splash)
        self.splashImage.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.splashImage.setObjectName("splashImage")
        self.vboxlayout2.addWidget(self.splashImage)

        self.loginInfo = QtGui.QLabel(self.splash)
        self.loginInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.loginInfo.setObjectName("loginInfo")
        self.vboxlayout2.addWidget(self.loginInfo)

        self.hboxlayout6 = QtGui.QHBoxLayout()
        self.hboxlayout6.setSpacing(6)
        self.hboxlayout6.setMargin(0)
        self.hboxlayout6.setObjectName("hboxlayout6")

        self.splashProgress = QtGui.QProgressBar(self.splash)
        self.splashProgress.setProperty("value",QtCore.QVariant(0))
        self.splashProgress.setTextVisible(False)
        self.splashProgress.setOrientation(QtCore.Qt.Horizontal)
        self.splashProgress.setInvertedAppearance(False)
        self.splashProgress.setObjectName("splashProgress")
        self.hboxlayout6.addWidget(self.splashProgress)

        self.login_cancel = QtGui.QPushButton(self.splash)
        self.login_cancel.setObjectName("login_cancel")
        self.hboxlayout6.addWidget(self.login_cancel)
        self.vboxlayout2.addLayout(self.hboxlayout6)
        self.rosterStackedWidget.addWidget(self.splash)

        self.mdiWidget = QtGui.QWidget(self.splitter)
        self.mdiWidget.setObjectName("mdiWidget")
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,335,27))
        self.menubar.setObjectName("menubar")

        self.menuPlugins = QtGui.QMenu(self.menubar)
        self.menuPlugins.setObjectName("menuPlugins")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuAkce = QtGui.QMenu(self.menubar)
        self.menuAkce.setObjectName("menuAkce")

        self.menuGroupchat = QtGui.QMenu(self.menuAkce)
        self.menuGroupchat.setObjectName("menuGroupchat")
        MainWindow.setMenuBar(self.menubar)

        self.actionShow_XML = QtGui.QAction(MainWindow)
        self.actionShow_XML.setIcon(QtGui.QIcon("images/16x16/actions/xml-konzole.png"))
        self.actionShow_XML.setObjectName("actionShow_XML")

        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setIcon(QtGui.QIcon("images/16x16/categories/gtk-preferences.png"))
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setIcon(QtGui.QIcon("images/16x16/actions/gtk-quit.png"))
        self.actionQuit.setObjectName("actionQuit")

        self.actionAdd_Contact = QtGui.QAction(MainWindow)
        self.actionAdd_Contact.setIcon(QtGui.QIcon("images/16x16/actions/gtk-add.png"))
        self.actionAdd_Contact.setObjectName("actionAdd_Contact")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setIcon(QtGui.QIcon("images/16x16/actions/about.png"))
        self.actionAbout.setObjectName("actionAbout")

        self.actionService_Discovery = QtGui.QAction(MainWindow)
        self.actionService_Discovery.setIcon(QtGui.QIcon("images/16x16/actions/service-discovery.png"))
        self.actionService_Discovery.setObjectName("actionService_Discovery")

        self.actionMUC_Browser = QtGui.QAction(MainWindow)
        self.actionMUC_Browser.setObjectName("actionMUC_Browser")

        self.actionPrivacy_list_editor = QtGui.QAction(MainWindow)
        self.actionPrivacy_list_editor.setObjectName("actionPrivacy_list_editor")

        self.actionIdentity = QtGui.QAction(MainWindow)
        self.actionIdentity.setIcon(QtGui.QIcon("images/16x16/categories/v-card.png"))
        self.actionIdentity.setObjectName("actionIdentity")

        self.actionProfiles = QtGui.QAction(MainWindow)
        self.actionProfiles.setObjectName("actionProfiles")

        self.actionJoin_groupchat = QtGui.QAction(MainWindow)
        self.actionJoin_groupchat.setObjectName("actionJoin_groupchat")

        self.actionBrowse_rooms = QtGui.QAction(MainWindow)
        self.actionBrowse_rooms.setObjectName("actionBrowse_rooms")

        self.actionSupport = QtGui.QAction(MainWindow)
        self.actionSupport.setObjectName("actionSupport")

        self.actionStart_Chat = QtGui.QAction(MainWindow)
        self.actionStart_Chat.setObjectName("actionStart_Chat")
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionSupport)
        self.menuGroupchat.addAction(self.actionJoin_groupchat)
        self.menuGroupchat.addAction(self.actionBrowse_rooms)
        self.menuAkce.addAction(self.menuGroupchat.menuAction())
        self.menuAkce.addAction(self.actionAdd_Contact)
        self.menuAkce.addAction(self.actionStart_Chat)
        self.menuAkce.addAction(self.actionService_Discovery)
        self.menuAkce.addAction(self.actionShow_XML)
        self.menuAkce.addAction(self.actionPrivacy_list_editor)
        self.menuAkce.addAction(self.actionIdentity)
        self.menuAkce.addSeparator()
        self.menuAkce.addAction(self.actionPreferences)
        self.menuAkce.addAction(self.actionProfiles)
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
        QtCore.QObject.connect(self.login_savePassword,QtCore.SIGNAL("clicked(bool)"),self.login_autoconnect.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setAccessibleName(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setAccessibleDescription(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.login_password.setAccessibleName(QtGui.QApplication.translate("MainWindow", "Password", None, QtGui.QApplication.UnicodeUTF8))
        self.login_password.setAccessibleDescription(QtGui.QApplication.translate("MainWindow", "Type your password here", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.loginStatus.setAccessibleName(QtGui.QApplication.translate("MainWindow", "Status for connection", None, QtGui.QApplication.UnicodeUTF8))
        self.loginStatus.setAccessibleDescription(QtGui.QApplication.translate("MainWindow", "Choose your status which will be used after connection", None, QtGui.QApplication.UnicodeUTF8))
        self.login_autoconnect.setAccessibleName(QtGui.QApplication.translate("MainWindow", "Auto connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_autoconnect.setAccessibleDescription(QtGui.QApplication.translate("MainWindow", "Auto connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_autoconnect.setText(QtGui.QApplication.translate("MainWindow", "Auto connect", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword.setAccessibleName(QtGui.QApplication.translate("MainWindow", "Save password", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword.setAccessibleDescription(QtGui.QApplication.translate("MainWindow", "Save password", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword.setText(QtGui.QApplication.translate("MainWindow", "Save Password", None, QtGui.QApplication.UnicodeUTF8))
        self.registerButton.setText(QtGui.QApplication.translate("MainWindow", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.login_headerLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; font-weight:600;\">Connect</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.profilesHeader.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><span style=\" font-size:13pt; font-weight:600;\">Profiles</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.profilesList.setAccessibleName(QtGui.QApplication.translate("MainWindow", "Profiles list", None, QtGui.QApplication.UnicodeUTF8))
        self.profilesList.setAccessibleDescription(QtGui.QApplication.translate("MainWindow", "You can choose profile here", None, QtGui.QApplication.UnicodeUTF8))
        self.statusMessage.setText(QtGui.QApplication.translate("MainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.statusWidget.setToolTip(QtGui.QApplication.translate("MainWindow", "Here you can change your status", None, QtGui.QApplication.UnicodeUTF8))
        self.offlineButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Show offline contacts", None, QtGui.QApplication.UnicodeUTF8))
        self.toggleInvisible.setToolTip(QtGui.QApplication.translate("MainWindow", "Toggle Invisibility", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setToolTip(QtGui.QApplication.translate("MainWindow", "You can show/hide contats that are unavailable", None, QtGui.QApplication.UnicodeUTF8))
        self.moodButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Here you can change your mood", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setToolTip(QtGui.QApplication.translate("MainWindow", "Here you can change your status", None, QtGui.QApplication.UnicodeUTF8))
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
        self.eventsLabel.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:8pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:9pt;\"><span style=\" font-size:12pt; font-weight:600;\">Events</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.eventsTab), QtGui.QApplication.translate("MainWindow", "Events", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.eventsTab),QtGui.QApplication.translate("MainWindow", "Events", None, QtGui.QApplication.UnicodeUTF8))
        self.login_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.menuPlugins.setTitle(QtGui.QApplication.translate("MainWindow", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAkce.setTitle(QtGui.QApplication.translate("MainWindow", "Actions", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGroupchat.setTitle(QtGui.QApplication.translate("MainWindow", "Groupchat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionShow_XML.setText(QtGui.QApplication.translate("MainWindow", "Show XML", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd_Contact.setText(QtGui.QApplication.translate("MainWindow", "Add Contact", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionService_Discovery.setText(QtGui.QApplication.translate("MainWindow", "Service Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMUC_Browser.setText(QtGui.QApplication.translate("MainWindow", "MUC Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrivacy_list_editor.setText(QtGui.QApplication.translate("MainWindow", "Privacy list editor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIdentity.setText(QtGui.QApplication.translate("MainWindow", "Identity", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProfiles.setText(QtGui.QApplication.translate("MainWindow", "Profiles", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJoin_groupchat.setText(QtGui.QApplication.translate("MainWindow", "Join groupchat", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBrowse_rooms.setText(QtGui.QApplication.translate("MainWindow", "Browse rooms", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSupport.setText(QtGui.QApplication.translate("MainWindow", "Support", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart_Chat.setText(QtGui.QApplication.translate("MainWindow", "Start Chat", None, QtGui.QApplication.UnicodeUTF8))

