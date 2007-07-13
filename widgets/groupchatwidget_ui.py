# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/groupchatwidget.ui'
#
# Created: Fri Jul 13 05:50:50 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_groupchatwidget(object):
    def setupUi(self, groupchatwidget):
        groupchatwidget.setObjectName("groupchatwidget")
        groupchatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,536,410).size()).expandedTo(groupchatwidget.minimumSizeHint()))
        groupchatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(groupchatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter_2 = QtGui.QSplitter(groupchatwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setOpaqueResize(False)
        self.splitter_2.setObjectName("splitter_2")

        self.info = QtGui.QTextBrowser(self.splitter_2)
        self.info.setMinimumSize(QtCore.QSize(0,1))
        self.info.setObjectName("info")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.textEdit = QtGui.QTextBrowser(self.splitter)
        self.textEdit.setOpenExternalLinks(True)
        self.textEdit.setObjectName("textEdit")

        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.vboxlayout = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.users = QtGui.QTreeWidget(self.widget)
        self.users.setAlternatingRowColors(True)
        self.users.setRootIsDecorated(False)
        self.users.setObjectName("users")
        self.vboxlayout.addWidget(self.users)

        self.admin = QtGui.QWidget(self.widget)
        self.admin.setObjectName("admin")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.admin)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.roomAdmin = QtGui.QPushButton(self.admin)
        self.roomAdmin.setObjectName("roomAdmin")
        self.vboxlayout1.addWidget(self.roomAdmin)

        self.roomConfig = QtGui.QPushButton(self.admin)
        self.roomConfig.setObjectName("roomConfig")
        self.vboxlayout1.addWidget(self.roomConfig)
        self.vboxlayout.addWidget(self.admin)

        self.lineWidget = QtGui.QWidget(self.splitter_2)
        self.lineWidget.setMinimumSize(QtCore.QSize(0,10))
        self.lineWidget.setObjectName("lineWidget")
        self.gridlayout.addWidget(self.splitter_2,0,0,1,3)

        self.sendButton = QtGui.QPushButton(groupchatwidget)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout.addWidget(self.sendButton,1,2,1,1)

        self.smileys = QtGui.QToolButton(groupchatwidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.gridlayout.addWidget(self.smileys,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(331,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.retranslateUi(groupchatwidget)
        QtCore.QMetaObject.connectSlotsByName(groupchatwidget)

    def retranslateUi(self, groupchatwidget):
        groupchatwidget.setWindowTitle(QtGui.QApplication.translate("groupchatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(0,QtGui.QApplication.translate("groupchatwidget", "user", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(1,QtGui.QApplication.translate("groupchatwidget", "jid", None, QtGui.QApplication.UnicodeUTF8))
        self.roomAdmin.setText(QtGui.QApplication.translate("groupchatwidget", "Room administration", None, QtGui.QApplication.UnicodeUTF8))
        self.roomConfig.setText(QtGui.QApplication.translate("groupchatwidget", "Room configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("groupchatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("groupchatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))

