# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/mainWindow.ui'
#
# Created: Mon May  7 20:10:07 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,281,606).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.rosterTab = QtGui.QWidget()
        self.rosterTab.setObjectName("rosterTab")

        self.vboxlayout = QtGui.QVBoxLayout(self.rosterTab)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.rosterStackedWidget = QtGui.QStackedWidget(self.rosterTab)
        self.rosterStackedWidget.setObjectName("rosterStackedWidget")

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout1 = QtGui.QGridLayout(self.page_3)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(151,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.login_connect = QtGui.QPushButton(self.page_3)
        self.login_connect.setObjectName("login_connect")
        self.hboxlayout.addWidget(self.login_connect)
        self.gridlayout1.addLayout(self.hboxlayout,3,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,331,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,4,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label = QtGui.QLabel(self.page_3)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.label_2 = QtGui.QLabel(self.page_3)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)
        self.hboxlayout1.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.login_jid = QtGui.QLineEdit(self.page_3)
        self.login_jid.setObjectName("login_jid")
        self.vboxlayout2.addWidget(self.login_jid)

        self.login_password = QtGui.QLineEdit(self.page_3)
        self.login_password.setEchoMode(QtGui.QLineEdit.Password)
        self.login_password.setObjectName("login_password")
        self.vboxlayout2.addWidget(self.login_password)
        self.hboxlayout1.addLayout(self.vboxlayout2)
        self.gridlayout1.addLayout(self.hboxlayout1,2,0,1,1)

        self.line = QtGui.QFrame(self.page_3)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,1)

        self.label_3 = QtGui.QLabel(self.page_3)
        self.label_3.setObjectName("label_3")
        self.gridlayout1.addWidget(self.label_3,0,0,1,1)
        self.rosterStackedWidget.addWidget(self.page_3)

        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")

        self.gridlayout2 = QtGui.QGridLayout(self.page_4)
        self.gridlayout2.setMargin(0)
        self.gridlayout2.setSpacing(0)
        self.gridlayout2.setObjectName("gridlayout2")

        self.rosterWidget = QtGui.QWidget(self.page_4)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout2.addWidget(self.rosterWidget,0,0,1,1)
        self.rosterStackedWidget.addWidget(self.page_4)
        self.vboxlayout.addWidget(self.rosterStackedWidget)
        self.tabWidget.addTab(self.rosterTab,"")

        self.bookmarksTab = QtGui.QWidget()
        self.bookmarksTab.setObjectName("bookmarksTab")
        self.tabWidget.addTab(self.bookmarksTab,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,281,29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.rosterStackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.login_connect.setText(QtGui.QApplication.translate("MainWindow", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; font-weight:600;\">Connect</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.rosterTab), QtGui.QApplication.translate("MainWindow", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bookmarksTab), QtGui.QApplication.translate("MainWindow", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))

