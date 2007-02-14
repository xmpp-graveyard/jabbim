# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'roster.ui'
#
# Created: Wed Feb 14 18:10:25 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_roster(object):
    def setupUi(self, roster):
        roster.setObjectName("roster")
        roster.resize(QtCore.QSize(QtCore.QRect(0,0,239,418).size()).expandedTo(roster.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(roster)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName("gridlayout")

        self.roster = QtGui.QTreeWidget(roster)
        self.roster.setDragEnabled(True)
        self.roster.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.roster.setAlternatingRowColors(True)
        self.roster.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.roster.setIconSize(QtCore.QSize(16,16))
        self.roster.setRootIsDecorated(False)
        self.roster.setObjectName("roster")
        self.gridlayout.addWidget(self.roster,0,0,1,1)

        self.retranslateUi(roster)
        QtCore.QMetaObject.connectSlotsByName(roster)

    def retranslateUi(self, roster):
        roster.setWindowTitle(QtGui.QApplication.translate("roster", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.roster.headerItem().setText(0,QtGui.QApplication.translate("roster", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.roster.headerItem().setText(1,QtGui.QApplication.translate("roster", "id", None, QtGui.QApplication.UnicodeUTF8))
