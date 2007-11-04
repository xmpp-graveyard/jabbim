# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'historyBrowser.ui'
#
# Created: Sun Nov  4 04:55:01 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,560,429).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.calendarWidget = QtGui.QWidget(self.centralwidget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridlayout.addWidget(self.calendarWidget,1,0,1,1)

        self.seznam = QtGui.QListWidget(self.centralwidget)
        self.seznam.setObjectName("seznam")
        self.gridlayout.addWidget(self.seznam,0,0,1,1)

        self.text = QtGui.QTextBrowser(self.centralwidget)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.text,0,1,2,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,560,29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Archive browser", None, QtGui.QApplication.UnicodeUTF8))

