# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugins/archive/historyBrowser.ui'
#
# Created: Thu Apr 10 19:14:15 2008
#      by: PyQt4 UI code generator 4.3.1
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

        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.seznam = QtGui.QTreeWidget(self.splitter)
        self.seznam.setRootIsDecorated(False)
        self.seznam.setObjectName("seznam")

        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.search = QtGui.QPushButton(self.widget)
        self.search.setObjectName("search")
        self.gridlayout1.addWidget(self.search,0,1,1,1)

        self.calendarWidget = QtGui.QWidget(self.widget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridlayout1.addWidget(self.calendarWidget,1,0,1,2)

        self.searchText = QtGui.QLineEdit(self.widget)
        self.searchText.setObjectName("searchText")
        self.gridlayout1.addWidget(self.searchText,0,0,1,1)

        self.text = QtGui.QTextBrowser(self.splitter_2)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.splitter_2,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,560,24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Archive browser", None, QtGui.QApplication.UnicodeUTF8))
        self.search.setText(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))

