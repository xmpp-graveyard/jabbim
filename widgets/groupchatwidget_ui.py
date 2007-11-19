# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/groupchatwidget.ui'
#
# Created: Mon Nov 19 19:22:22 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

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

        self.splitter_3 = QtGui.QSplitter(groupchatwidget)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")

        self.info = QtGui.QTextBrowser(self.splitter_3)
        self.info.setMinimumSize(QtCore.QSize(0,1))
        self.info.setOpenExternalLinks(True)
        self.info.setObjectName("info")

        self.splitter_2 = QtGui.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.viewWidget = QtGui.QWidget(self.splitter)
        self.viewWidget.setObjectName("viewWidget")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.gridlayout1 = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.lineWidget = QtGui.QWidget(self.layoutWidget)
        self.lineWidget.setMinimumSize(QtCore.QSize(0,10))
        self.lineWidget.setObjectName("lineWidget")
        self.gridlayout1.addWidget(self.lineWidget,0,0,1,3)

        spacerItem = QtGui.QSpacerItem(161,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,1,0,1,1)

        self.smileys = QtGui.QToolButton(self.layoutWidget)
        self.smileys.setIcon(QtGui.QIcon("images/22x22/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.gridlayout1.addWidget(self.smileys,1,1,1,1)

        self.sendButton = QtGui.QToolButton(self.layoutWidget)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout1.addWidget(self.sendButton,1,2,1,1)

        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.users = QtGui.QTreeWidget(self.layoutWidget1)
        self.users.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.users.setAlternatingRowColors(True)
        self.users.setIconSize(QtCore.QSize(32,32))
        self.users.setIndentation(0)
        self.users.setRootIsDecorated(False)
        self.users.setObjectName("users")
        self.vboxlayout.addWidget(self.users)

        self.pluginWidget = QtGui.QWidget(self.layoutWidget1)
        self.pluginWidget.setObjectName("pluginWidget")
        self.vboxlayout.addWidget(self.pluginWidget)
        self.gridlayout.addWidget(self.splitter_3,0,0,2,2)

        self.retranslateUi(groupchatwidget)
        QtCore.QMetaObject.connectSlotsByName(groupchatwidget)

    def retranslateUi(self, groupchatwidget):
        groupchatwidget.setWindowTitle(QtGui.QApplication.translate("groupchatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.info.setToolTip(QtGui.QApplication.translate("groupchatwidget", "Every multi user chat can has topic of it\'s discussion", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setToolTip(QtGui.QApplication.translate("groupchatwidget", "You can add emoticons by clicking here", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("groupchatwidget", "Send", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(0,QtGui.QApplication.translate("groupchatwidget", "user", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(1,QtGui.QApplication.translate("groupchatwidget", "jid", None, QtGui.QApplication.UnicodeUTF8))

