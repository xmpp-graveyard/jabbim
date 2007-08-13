# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugins/archive/historyBrowser.ui'
#
# Created: Mon Aug 13 11:45:13 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_HistoryBrowser(object):
    def setupUi(self, HistoryBrowser):
        HistoryBrowser.setObjectName("HistoryBrowser")
        HistoryBrowser.resize(QtCore.QSize(QtCore.QRect(0,0,582,609).size()).expandedTo(HistoryBrowser.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(HistoryBrowser)
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

        self.calendar = QtGui.QCalendarWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(254)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setGridVisible(False)
        self.calendar.setHeaderVisible(True)
        self.calendar.setObjectName("calendar")

        self.seznam = QtGui.QListWidget(self.splitter)
        self.seznam.setObjectName("seznam")

        self.text = QtGui.QTextBrowser(self.splitter_2)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.splitter_2,0,0,1,1)
        HistoryBrowser.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(HistoryBrowser)
        self.menubar.setGeometry(QtCore.QRect(0,0,582,25))
        self.menubar.setObjectName("menubar")
        HistoryBrowser.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(HistoryBrowser)
        self.statusbar.setObjectName("statusbar")
        HistoryBrowser.setStatusBar(self.statusbar)

        self.retranslateUi(HistoryBrowser)
        QtCore.QMetaObject.connectSlotsByName(HistoryBrowser)

    def retranslateUi(self, HistoryBrowser):
        HistoryBrowser.setWindowTitle(QtGui.QApplication.translate("HistoryBrowser", "Archive browser", None, QtGui.QApplication.UnicodeUTF8))

