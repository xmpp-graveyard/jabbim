# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugins/archive/historyBrowser.ui'
#
# Created: Wed Nov 19 12:32:17 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560,429)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.splitter_3 = QtGui.QSplitter(self.centralwidget)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter = QtGui.QSplitter(self.splitter_3)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.seznam = QtGui.QTreeWidget(self.splitter)
        self.seznam.setRootIsDecorated(False)
        self.seznam.setObjectName("seznam")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridlayout1 = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")
        self.calendarWidget = QtGui.QWidget(self.layoutWidget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridlayout1.addWidget(self.calendarWidget,1,0,1,4)
        self.searchText = QtGui.QLineEdit(self.layoutWidget)
        self.searchText.setObjectName("searchText")
        self.gridlayout1.addWidget(self.searchText,0,0,1,1)
        self.today = QtGui.QPushButton(self.layoutWidget)
        self.today.setObjectName("today")
        self.gridlayout1.addWidget(self.today,0,2,1,1)
        self.search = QtGui.QPushButton(self.layoutWidget)
        self.search.setObjectName("search")
        self.gridlayout1.addWidget(self.search,0,1,1,1)
        self.splitter_2 = QtGui.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.searchList = QtGui.QTreeWidget(self.splitter_2)
        self.searchList.setObjectName("searchList")
        self.text = QtGui.QTextBrowser(self.splitter_2)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.splitter_3,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(MainWindow.translate("MainWindow", "Archive browser", None, QtGui.QApplication.UnicodeUTF8))
        self.seznam.headerItem().setText(0,MainWindow.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.today.setText(MainWindow.translate("MainWindow", "Today", None, QtGui.QApplication.UnicodeUTF8))
        self.search.setText(MainWindow.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.searchList.headerItem().setText(0,MainWindow.translate("MainWindow", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.searchList.headerItem().setText(1,MainWindow.translate("MainWindow", "Message", None, QtGui.QApplication.UnicodeUTF8))

