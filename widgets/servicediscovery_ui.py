# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'servicediscovery.ui'
#
# Created: Wed Feb 13 16:36:39 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_serviceDiscovery(object):
    def setupUi(self, serviceDiscovery):
        serviceDiscovery.setObjectName("serviceDiscovery")
        serviceDiscovery.resize(QtCore.QSize(QtCore.QRect(0,0,439,407).size()).expandedTo(serviceDiscovery.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(serviceDiscovery)
        self.gridlayout.setObjectName("gridlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(serviceDiscovery)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.server = QtGui.QComboBox(serviceDiscovery)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.server.sizePolicy().hasHeightForWidth())
        self.server.setSizePolicy(sizePolicy)
        self.server.setEditable(True)
        self.server.setObjectName("server")
        self.hboxlayout.addWidget(self.server)

        self.reload = QtGui.QPushButton(serviceDiscovery)
        self.reload.setObjectName("reload")
        self.hboxlayout.addWidget(self.reload)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,2)

        self.tree = QtGui.QTreeWidget(serviceDiscovery)
        self.tree.setIconSize(QtCore.QSize(48,48))
        self.tree.setObjectName("tree")
        self.gridlayout.addWidget(self.tree,1,0,1,2)

        spacerItem = QtGui.QSpacerItem(621,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.close = QtGui.QPushButton(serviceDiscovery)
        self.close.setObjectName("close")
        self.gridlayout.addWidget(self.close,2,1,1,1)

        self.retranslateUi(serviceDiscovery)
        QtCore.QObject.connect(self.close,QtCore.SIGNAL("clicked()"),serviceDiscovery.reject)
        QtCore.QMetaObject.connectSlotsByName(serviceDiscovery)

    def retranslateUi(self, serviceDiscovery):
        serviceDiscovery.setWindowTitle(QtGui.QApplication.translate("serviceDiscovery", "Service Discovery", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("serviceDiscovery", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.reload.setText(QtGui.QApplication.translate("serviceDiscovery", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0,QtGui.QApplication.translate("serviceDiscovery", "name", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(1,QtGui.QApplication.translate("serviceDiscovery", "search", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(2,QtGui.QApplication.translate("serviceDiscovery", "register", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(3,QtGui.QApplication.translate("serviceDiscovery", "jid", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(4,QtGui.QApplication.translate("serviceDiscovery", "commands", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("serviceDiscovery", "Close", None, QtGui.QApplication.UnicodeUTF8))

