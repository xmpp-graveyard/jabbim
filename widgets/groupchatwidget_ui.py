# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/groupchatwidget.ui'
#
# Created: Sun Feb  3 12:13:41 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_groupchatwidget(object):
    def setupUi(self, groupchatwidget):
        groupchatwidget.setObjectName("groupchatwidget")
        groupchatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,536,408).size()).expandedTo(groupchatwidget.minimumSizeHint()))
        groupchatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(groupchatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter_3 = QtGui.QSplitter(groupchatwidget)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")

        self.layoutWidget = QtGui.QWidget(self.splitter_3)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.disco_info = QtGui.QLabel(self.layoutWidget)
        self.disco_info.setObjectName("disco_info")
        self.vboxlayout.addWidget(self.disco_info)

        self.info = QtGui.QTextBrowser(self.layoutWidget)
        self.info.setMinimumSize(QtCore.QSize(0,1))
        self.info.setOpenExternalLinks(True)
        self.info.setObjectName("info")
        self.vboxlayout.addWidget(self.info)

        self.splitter_2 = QtGui.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.viewWidget = QtGui.QWidget(self.splitter)
        self.viewWidget.setObjectName("viewWidget")

        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.boldButton = QtGui.QToolButton(self.widget)
        self.boldButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boldButton.setIcon(QtGui.QIcon("images/16x16/actions/format-text-bold.png"))
        self.boldButton.setCheckable(True)
        self.boldButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.boldButton.setObjectName("boldButton")
        self.gridlayout1.addWidget(self.boldButton,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(16,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,1,0,1,1)

        self.italicButton = QtGui.QToolButton(self.widget)
        self.italicButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.italicButton.setIcon(QtGui.QIcon("images/16x16/actions/format-text-italic.png"))
        self.italicButton.setCheckable(True)
        self.italicButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.italicButton.setObjectName("italicButton")
        self.gridlayout1.addWidget(self.italicButton,1,2,1,1)

        self.smileys = QtGui.QToolButton(self.widget)
        self.smileys.setIcon(QtGui.QIcon("images/16x16/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.gridlayout1.addWidget(self.smileys,1,7,1,1)

        self.sendButton = QtGui.QToolButton(self.widget)
        self.sendButton.setIcon(QtGui.QIcon("images/16x16/actions/send.png"))
        self.sendButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.sendButton.setObjectName("sendButton")
        self.gridlayout1.addWidget(self.sendButton,1,8,1,1)

        self.lineWidget = QtGui.QWidget(self.widget)
        self.lineWidget.setMinimumSize(QtCore.QSize(0,10))
        self.lineWidget.setObjectName("lineWidget")
        self.gridlayout1.addWidget(self.lineWidget,0,0,1,9)

        self.underlineButton = QtGui.QToolButton(self.widget)
        self.underlineButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.underlineButton.setIcon(QtGui.QIcon("images/16x16/actions/format-text-underline.png"))
        self.underlineButton.setCheckable(True)
        self.underlineButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.underlineButton.setObjectName("underlineButton")
        self.gridlayout1.addWidget(self.underlineButton,1,3,1,1)

        self.fontSize = QtGui.QComboBox(self.widget)
        self.fontSize.setObjectName("fontSize")
        self.gridlayout1.addWidget(self.fontSize,1,5,1,1)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,6,1,1)

        self.colorButton = QtGui.QToolButton(self.widget)
        self.colorButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.colorButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.colorButton.setObjectName("colorButton")
        self.gridlayout1.addWidget(self.colorButton,1,4,1,1)

        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.users = QtGui.QTreeWidget(self.layoutWidget1)
        self.users.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.users.setIconSize(QtCore.QSize(32,32))
        self.users.setIndentation(0)
        self.users.setRootIsDecorated(False)
        self.users.setObjectName("users")
        self.vboxlayout1.addWidget(self.users)

        self.pluginWidget = QtGui.QWidget(self.layoutWidget1)
        self.pluginWidget.setObjectName("pluginWidget")
        self.vboxlayout1.addWidget(self.pluginWidget)
        self.gridlayout.addWidget(self.splitter_3,0,0,1,1)

        self.retranslateUi(groupchatwidget)
        QtCore.QMetaObject.connectSlotsByName(groupchatwidget)

    def retranslateUi(self, groupchatwidget):
        groupchatwidget.setWindowTitle(QtGui.QApplication.translate("groupchatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.info.setToolTip(QtGui.QApplication.translate("groupchatwidget", "Every multi-user chat can have topic of its discussion", None, QtGui.QApplication.UnicodeUTF8))
        self.boldButton.setText(QtGui.QApplication.translate("groupchatwidget", "Bold", None, QtGui.QApplication.UnicodeUTF8))
        self.italicButton.setText(QtGui.QApplication.translate("groupchatwidget", "Italic", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setToolTip(QtGui.QApplication.translate("groupchatwidget", "You can add emoticons by clicking here", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("groupchatwidget", "&Send", None, QtGui.QApplication.UnicodeUTF8))
        self.underlineButton.setText(QtGui.QApplication.translate("groupchatwidget", "Underline", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(0,QtGui.QApplication.translate("groupchatwidget", "user", None, QtGui.QApplication.UnicodeUTF8))
        self.users.headerItem().setText(1,QtGui.QApplication.translate("groupchatwidget", "jid", None, QtGui.QApplication.UnicodeUTF8))

