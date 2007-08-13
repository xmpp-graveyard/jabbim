# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logWindow.ui'
#
# Created: Mon Aug 13 15:44:26 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_DebugLogWindow(object):
    def setupUi(self, DebugLogWindow):
        DebugLogWindow.setObjectName("DebugLogWindow")
        DebugLogWindow.resize(QtCore.QSize(QtCore.QRect(0,0,363,408).size()).expandedTo(DebugLogWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(DebugLogWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.clearButton = QtGui.QPushButton(self.centralwidget)
        self.clearButton.setFlat(False)
        self.clearButton.setObjectName("clearButton")
        self.gridlayout.addWidget(self.clearButton,1,1,1,1)

        self.enableBox = QtGui.QCheckBox(self.centralwidget)
        self.enableBox.setObjectName("enableBox")
        self.gridlayout.addWidget(self.enableBox,1,0,1,1)

        self.logView = QtGui.QTextBrowser(self.centralwidget)
        self.logView.setObjectName("logView")
        self.gridlayout.addWidget(self.logView,0,0,1,2)
        DebugLogWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(DebugLogWindow)
        self.statusbar.setObjectName("statusbar")
        DebugLogWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DebugLogWindow)
        QtCore.QMetaObject.connectSlotsByName(DebugLogWindow)

    def retranslateUi(self, DebugLogWindow):
        DebugLogWindow.setWindowTitle(QtGui.QApplication.translate("DebugLogWindow", "Debug log", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("DebugLogWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.enableBox.setText(QtGui.QApplication.translate("DebugLogWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))

