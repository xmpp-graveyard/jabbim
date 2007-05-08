# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/mainWindow.ui'
#
# Created: Tue May  8 11:14:31 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,307,694).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.showOffline = QtGui.QToolButton(self.centralwidget)
        self.showOffline.setCheckable(True)
        self.showOffline.setArrowType(QtCore.Qt.NoArrow)
        self.showOffline.setObjectName("showOffline")
        self.hboxlayout.addWidget(self.showOffline)

        spacerItem = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.statusButton = QtGui.QToolButton(self.centralwidget)
        self.statusButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.statusButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.statusButton.setObjectName("statusButton")
        self.hboxlayout.addWidget(self.statusButton)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.rosterTab = QtGui.QWidget()
        self.rosterTab.setObjectName("rosterTab")

        self.gridlayout1 = QtGui.QGridLayout(self.rosterTab)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.rosterStackedWidget = QtGui.QStackedWidget(self.rosterTab)
        self.rosterStackedWidget.setObjectName("rosterStackedWidget")

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout2 = QtGui.QGridLayout(self.page_3)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.line = QtGui.QFrame(self.page_3)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout2.addWidget(self.line,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,331,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,5,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem2 = QtGui.QSpacerItem(121,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem2)

        self.login_savePassword = QtGui.QCheckBox(self.page_3)
        self.login_savePassword.setObjectName("login_savePassword")
        self.hboxlayout1.addWidget(self.login_savePassword)
        self.gridlayout2.addLayout(self.hboxlayout1,3,0,1,1)

        self.label_3 = QtGui.QLabel(self.page_3)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3,0,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.page_3)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_2 = QtGui.QLabel(self.page_3)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.hboxlayout2.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.login_jid = QtGui.QLineEdit(self.page_3)
        self.login_jid.setObjectName("login_jid")
        self.vboxlayout1.addWidget(self.login_jid)

        self.login_password = QtGui.QLineEdit(self.page_3)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.vboxlayout1.addWidget(self.login_password)
        self.hboxlayout2.addLayout(self.vboxlayout1)
        self.gridlayout2.addLayout(self.hboxlayout2,2,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem3 = QtGui.QSpacerItem(151,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem3)

        self.login_connect = QtGui.QPushButton(self.page_3)
        self.login_connect.setObjectName("login_connect")
        self.hboxlayout3.addWidget(self.login_connect)
        self.gridlayout2.addLayout(self.hboxlayout3,4,0,1,1)
        self.rosterStackedWidget.addWidget(self.page_3)

        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")

        self.gridlayout3 = QtGui.QGridLayout(self.page_4)
        self.gridlayout3.setMargin(0)
        self.gridlayout3.setSpacing(0)
        self.gridlayout3.setObjectName("gridlayout3")

        self.rosterWidget = QtGui.QWidget(self.page_4)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout3.addWidget(self.rosterWidget,0,0,1,1)
        self.rosterStackedWidget.addWidget(self.page_4)
        self.gridlayout1.addWidget(self.rosterStackedWidget,0,0,1,1)
        self.tabWidget.addTab(self.rosterTab,"")

        self.bookmarksTab = QtGui.QWidget()
        self.bookmarksTab.setObjectName("bookmarksTab")
        self.tabWidget.addTab(self.bookmarksTab,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,307,29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.rosterStackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.showOffline.setText(QtGui.QApplication.translate("MainWindow", "Show offline", None, QtGui.QApplication.UnicodeUTF8))
        self.statusButton.setText(QtGui.QApplication.translate("MainWindow", "Offline", None, QtGui.QApplication.UnicodeUTF8))
        self.login_savePassword.setText(QtGui.QApplication.translate("MainWindow", "Save Password", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; font-weight:600;\">Connect</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rosterTab), QtGui.QApplication.translate("MainWindow", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bookmarksTab), QtGui.QApplication.translate("MainWindow", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))

