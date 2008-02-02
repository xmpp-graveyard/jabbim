# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logWindow.ui'
#
# Created: Wed Aug 15 07:34:04 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,363,408).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Debug log", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.enableBox.setText(QtGui.QApplication.translate("MainWindow", "Enable", None, QtGui.QApplication.UnicodeUTF8))

