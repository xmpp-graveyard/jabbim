# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gameslist.ui'
#
# Created: Wed Feb 28 15:44:36 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_gameslist(object):
    def setupUi(self, gameslist):
        gameslist.setObjectName("gameslist")
        gameslist.resize(QtCore.QSize(QtCore.QRect(0,0,399,240).size()).expandedTo(gameslist.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(gameslist)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(331,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.refreshButton = QtGui.QPushButton(self.centralwidget)
        self.refreshButton.setObjectName("refreshButton")
        self.gridlayout.addWidget(self.refreshButton,1,1,1,1)

        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setObjectName("treeWidget")
        self.gridlayout.addWidget(self.treeWidget,0,0,1,2)
        gameslist.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(gameslist)
        self.statusbar.setObjectName("statusbar")
        gameslist.setStatusBar(self.statusbar)

        self.retranslateUi(gameslist)
        QtCore.QMetaObject.connectSlotsByName(gameslist)

    def retranslateUi(self, gameslist):
        gameslist.setWindowTitle(QtGui.QApplication.translate("gameslist", "Games list", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("gameslist", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0,QtGui.QApplication.translate("gameslist", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(1,QtGui.QApplication.translate("gameslist", "# Players", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(2,QtGui.QApplication.translate("gameslist", "Open", None, QtGui.QApplication.UnicodeUTF8))

