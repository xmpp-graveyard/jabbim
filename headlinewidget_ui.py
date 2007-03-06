# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'headlinewidget.ui'
#
# Created: Tue Mar  6 17:08:32 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_headlinewidget(object):
    def setupUi(self, headlinewidget):
        headlinewidget.setObjectName("headlinewidget")
        headlinewidget.resize(QtCore.QSize(QtCore.QRect(0,0,490,521).size()).expandedTo(headlinewidget.minimumSizeHint()))
        headlinewidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(headlinewidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.text = QtGui.QTextEdit(headlinewidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.text.sizePolicy().hasHeightForWidth())
        self.text.setSizePolicy(sizePolicy)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.text,1,0,1,1)

        self.messages = QtGui.QTreeWidget(headlinewidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.messages.sizePolicy().hasHeightForWidth())
        self.messages.setSizePolicy(sizePolicy)
        self.messages.setAlternatingRowColors(True)
        self.messages.setSortingEnabled(True)
        self.messages.setAllColumnsShowFocus(True)
        self.messages.setObjectName("messages")
        self.gridlayout.addWidget(self.messages,0,0,1,1)

        self.retranslateUi(headlinewidget)
        QtCore.QMetaObject.connectSlotsByName(headlinewidget)

    def retranslateUi(self, headlinewidget):
        headlinewidget.setWindowTitle(QtGui.QApplication.translate("headlinewidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.messages.headerItem().setText(0,QtGui.QApplication.translate("headlinewidget", "Subject", None, QtGui.QApplication.UnicodeUTF8))
        self.messages.headerItem().setText(1,QtGui.QApplication.translate("headlinewidget", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.messages.headerItem().setText(2,QtGui.QApplication.translate("headlinewidget", "Date", None, QtGui.QApplication.UnicodeUTF8))
        self.messages.headerItem().setText(3,QtGui.QApplication.translate("headlinewidget", "Text", None, QtGui.QApplication.UnicodeUTF8))

