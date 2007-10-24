# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/groupchatadmin.ui'
#
# Created: Wed Oct 24 03:34:51 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_groupchatAdmin(object):
    def setupUi(self, groupchatAdmin):
        groupchatAdmin.setObjectName("groupchatAdmin")
        groupchatAdmin.resize(QtCore.QSize(QtCore.QRect(0,0,415,354).size()).expandedTo(groupchatAdmin.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(groupchatAdmin)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.groupchatAdminTab = QtGui.QTabWidget(groupchatAdmin)
        self.groupchatAdminTab.setObjectName("groupchatAdminTab")

        self.config = QtGui.QWidget()
        self.config.setObjectName("config")
        self.groupchatAdminTab.addTab(self.config,"")

        self.affiliation = QtGui.QWidget()
        self.affiliation.setObjectName("affiliation")
        self.groupchatAdminTab.addTab(self.affiliation,"")
        self.gridlayout.addWidget(self.groupchatAdminTab,0,0,1,3)

        self.pushButton = QtGui.QPushButton(groupchatAdmin)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,1,2,1,1)

        self.pushButton_2 = QtGui.QPushButton(groupchatAdmin)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(201,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.retranslateUi(groupchatAdmin)
        self.groupchatAdminTab.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),groupchatAdmin.reject)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),groupchatAdmin.accept)
        QtCore.QMetaObject.connectSlotsByName(groupchatAdmin)

    def retranslateUi(self, groupchatAdmin):
        groupchatAdmin.setWindowTitle(QtGui.QApplication.translate("groupchatAdmin", "MUC Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchatAdminTab.setTabText(self.groupchatAdminTab.indexOf(self.config), QtGui.QApplication.translate("groupchatAdmin", "MUC Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchatAdminTab.setTabText(self.groupchatAdminTab.indexOf(self.affiliation), QtGui.QApplication.translate("groupchatAdmin", "Affiliations", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("groupchatAdmin", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("groupchatAdmin", "Save", None, QtGui.QApplication.UnicodeUTF8))

