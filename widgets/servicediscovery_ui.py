# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/servicediscovery.ui'
#
# Created: Sun Oct 21 17:06:22 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_serviceDiscovery(object):
    def setupUi(self, serviceDiscovery):
        serviceDiscovery.setObjectName("serviceDiscovery")
        serviceDiscovery.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(serviceDiscovery.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(serviceDiscovery)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tree = QtGui.QTreeWidget(serviceDiscovery)
        self.tree.setIconSize(QtCore.QSize(48,48))
        self.tree.setObjectName("tree")
        self.gridlayout.addWidget(self.tree,0,0,1,1)

        self.retranslateUi(serviceDiscovery)
        QtCore.QMetaObject.connectSlotsByName(serviceDiscovery)

    def retranslateUi(self, serviceDiscovery):
        serviceDiscovery.setWindowTitle(QtGui.QApplication.translate("serviceDiscovery", "Service Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0,QtGui.QApplication.translate("serviceDiscovery", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(1,QtGui.QApplication.translate("serviceDiscovery", "jid", None, QtGui.QApplication.UnicodeUTF8))

