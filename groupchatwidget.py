# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupchatwidget.ui'
#
# Created: Fri Feb 16 18:38:26 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_groupchatwidget(object):
    def setupUi(self, groupchatwidget):
        groupchatwidget.setObjectName("groupchatwidget")
        groupchatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,490,360).size()).expandedTo(groupchatwidget.minimumSizeHint()))
        groupchatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(groupchatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.listWidget = QtGui.QListWidget(groupchatwidget)
        self.listWidget.setMaximumSize(QtCore.QSize(130,16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,1,1,1)

        self.textEdit = QtGui.QTextEdit(groupchatwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridlayout.addWidget(self.textEdit,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.line = QtGui.QLineEdit(groupchatwidget)
        self.line.setAcceptDrops(True)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.smileys = QtGui.QToolButton(groupchatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/smileys/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.hboxlayout.addWidget(self.smileys)

        self.sendButton = QtGui.QPushButton(groupchatwidget)
        self.sendButton.setObjectName("sendButton")
        self.hboxlayout.addWidget(self.sendButton)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,2)

        self.retranslateUi(groupchatwidget)
        QtCore.QMetaObject.connectSlotsByName(groupchatwidget)

    def retranslateUi(self, groupchatwidget):
        groupchatwidget.setWindowTitle(QtGui.QApplication.translate("groupchatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("groupchatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("groupchatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))
