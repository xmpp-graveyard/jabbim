# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'discovery.ui'
#
# Created: Sat Feb 24 06:31:04 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_discovery(object):
    def setupUi(self, discovery):
        discovery.setObjectName("discovery")
        discovery.resize(QtCore.QSize(QtCore.QRect(0,0,622,427).size()).expandedTo(discovery.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(discovery)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.services = QtGui.QTreeWidget(discovery)
        self.services.setObjectName("services")
        self.gridlayout.addWidget(self.services,0,0,1,1)

        self.retranslateUi(discovery)
        QtCore.QMetaObject.connectSlotsByName(discovery)

    def retranslateUi(self, discovery):
        discovery.setWindowTitle(QtGui.QApplication.translate("discovery", "Jabbim - Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.services.headerItem().setText(0,QtGui.QApplication.translate("discovery", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.services.headerItem().setText(1,QtGui.QApplication.translate("discovery", "Jid", None, QtGui.QApplication.UnicodeUTF8))

