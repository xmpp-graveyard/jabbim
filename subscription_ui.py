# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subscription.ui'
#
# Created: Wed Mar 14 17:57:06 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_subscriptionwidget(object):
    def setupUi(self, subscriptionwidget):
        subscriptionwidget.setObjectName("subscriptionwidget")
        subscriptionwidget.resize(QtCore.QSize(QtCore.QRect(0,0,162,95).size()).expandedTo(subscriptionwidget.minimumSizeHint()))
        subscriptionwidget.setMinimumSize(QtCore.QSize(0,95))

        self.gridlayout = QtGui.QGridLayout(subscriptionwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.text = QtGui.QLabel(subscriptionwidget)
        self.text.setWordWrap(True)
        self.text.setObjectName("text")
        self.gridlayout.addWidget(self.text,0,0,1,1)

        self.retranslateUi(subscriptionwidget)
        QtCore.QMetaObject.connectSlotsByName(subscriptionwidget)

    def retranslateUi(self, subscriptionwidget):
        subscriptionwidget.setWindowTitle(QtGui.QApplication.translate("subscriptionwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.text.setText(QtGui.QApplication.translate("subscriptionwidget", "User hanzz@njs.netlab.cz wants to add you to his/her roster. Add him/her?", None, QtGui.QApplication.UnicodeUTF8))

