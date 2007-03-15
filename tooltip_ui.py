# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tooltip.ui'
#
# Created: Thu Mar 15 07:35:50 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_tooltipwidget(object):
    def setupUi(self, tooltipwidget):
        tooltipwidget.setObjectName("tooltipwidget")
        tooltipwidget.resize(QtCore.QSize(QtCore.QRect(0,0,227,95).size()).expandedTo(tooltipwidget.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(tooltipwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.frame = QtGui.QFrame(tooltipwidget)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")

        self.gridlayout1 = QtGui.QGridLayout(self.frame)
        self.gridlayout1.setMargin(2)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.status = QtGui.QLabel(self.frame)
        self.status.setMaximumSize(QtCore.QSize(16777215,20))
        self.status.setObjectName("status")
        self.gridlayout1.addWidget(self.status,1,1,1,1)

        self.icon = QtGui.QLabel(self.frame)
        self.icon.setMaximumSize(QtCore.QSize(66,66))
        self.icon.setObjectName("icon")
        self.gridlayout1.addWidget(self.icon,0,0,3,1)

        self.message = QtGui.QLabel(self.frame)
        self.message.setTextFormat(QtCore.Qt.RichText)
        self.message.setWordWrap(True)
        self.message.setObjectName("message")
        self.gridlayout1.addWidget(self.message,3,0,1,2)

        self.jid = QtGui.QLabel(self.frame)
        self.jid.setMaximumSize(QtCore.QSize(16777215,20))
        self.jid.setScaledContents(True)
        self.jid.setWordWrap(True)
        self.jid.setObjectName("jid")
        self.gridlayout1.addWidget(self.jid,0,1,1,1)
        self.gridlayout.addWidget(self.frame,0,0,1,1)

        self.retranslateUi(tooltipwidget)
        QtCore.QMetaObject.connectSlotsByName(tooltipwidget)

    def retranslateUi(self, tooltipwidget):
        tooltipwidget.setWindowTitle(QtGui.QApplication.translate("tooltipwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setText(QtGui.QApplication.translate("tooltipwidget", "Presence", None, QtGui.QApplication.UnicodeUTF8))
        self.message.setText(QtGui.QApplication.translate("tooltipwidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.jid.setText(QtGui.QApplication.translate("tooltipwidget", "Jabber ID", None, QtGui.QApplication.UnicodeUTF8))

