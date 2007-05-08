# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'status.ui'
#
# Created: Tue Jan 23 20:35:55 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_status(object):
    def setupUi(self, status):
        status.setObjectName("status")
        status.resize(QtCore.QSize(QtCore.QRect(0,0,256,227).size()).expandedTo(status.minimumSizeHint()))
        status.setWindowIcon(QtGui.QIcon("images/16x16/jgames.png"))

        self.gridlayout = QtGui.QGridLayout(status)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(101,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.set = QtGui.QPushButton(status)
        self.set.setObjectName("set")
        self.gridlayout.addWidget(self.set,2,2,1,1)

        self.time = QtGui.QLabel(status)
        self.time.setObjectName("time")
        self.gridlayout.addWidget(self.time,1,0,1,3)

        self.status = QtGui.QTextBrowser(status)
        self.status.setReadOnly(False)
        self.status.setObjectName("status")
        self.gridlayout.addWidget(self.status,0,0,1,3)

        self.retranslateUi(status)
        QtCore.QObject.connect(self.set,QtCore.SIGNAL("clicked()"),status.accept)
        QtCore.QMetaObject.connectSlotsByName(status)

    def retranslateUi(self, status):
        status.setWindowTitle(QtGui.QApplication.translate("status", "Set status message", None, QtGui.QApplication.UnicodeUTF8))
        self.set.setText(QtGui.QApplication.translate("status", "Set", None, QtGui.QApplication.UnicodeUTF8))
