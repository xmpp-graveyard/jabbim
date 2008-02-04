# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/chatwidget.ui'
#
# Created: Mon Feb  4 05:22:42 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_chatwidget(object):
    def setupUi(self, chatwidget):
        chatwidget.setObjectName("chatwidget")
        chatwidget.resize(QtCore.QSize(QtCore.QRect(0,0,515,414).size()).expandedTo(chatwidget.minimumSizeHint()))
        chatwidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.gridlayout = QtGui.QGridLayout(chatwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter_2 = QtGui.QSplitter(chatwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.viewWidget = QtGui.QWidget(self.splitter)
        self.viewWidget.setMinimumSize(QtCore.QSize(0,10))
        self.viewWidget.setObjectName("viewWidget")

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.selfAvatar = QtGui.QLabel(self.layoutWidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selfAvatar.sizePolicy().hasHeightForWidth())
        self.selfAvatar.setSizePolicy(sizePolicy)
        self.selfAvatar.setObjectName("selfAvatar")
        self.hboxlayout.addWidget(self.selfAvatar)

        self.lineWidget = QtGui.QWidget(self.layoutWidget)
        self.lineWidget.setMinimumSize(QtCore.QSize(0,10))
        self.lineWidget.setObjectName("lineWidget")
        self.hboxlayout.addWidget(self.lineWidget)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem = QtGui.QSpacerItem(111,29,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)

        self.boldButton = QtGui.QToolButton(self.layoutWidget)
        self.boldButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boldButton.setIcon(QtGui.QIcon("images/16x16/actions/format-text-bold.png"))
        self.boldButton.setCheckable(True)
        self.boldButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.boldButton.setObjectName("boldButton")
        self.hboxlayout1.addWidget(self.boldButton)

        self.italicButton = QtGui.QToolButton(self.layoutWidget)
        self.italicButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.italicButton.setIcon(QtGui.QIcon("images/16x16/actions/format-text-italic.png"))
        self.italicButton.setCheckable(True)
        self.italicButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.italicButton.setObjectName("italicButton")
        self.hboxlayout1.addWidget(self.italicButton)

        self.underlineButton = QtGui.QToolButton(self.layoutWidget)
        self.underlineButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.underlineButton.setIcon(QtGui.QIcon("images/16x16/actions/format-text-underline.png"))
        self.underlineButton.setCheckable(True)
        self.underlineButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.underlineButton.setObjectName("underlineButton")
        self.hboxlayout1.addWidget(self.underlineButton)

        self.colorButton = QtGui.QToolButton(self.layoutWidget)
        self.colorButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.colorButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.colorButton.setObjectName("colorButton")
        self.hboxlayout1.addWidget(self.colorButton)

        self.backgroundButton = QtGui.QToolButton(self.layoutWidget)
        self.backgroundButton.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.backgroundButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.backgroundButton.setObjectName("backgroundButton")
        self.hboxlayout1.addWidget(self.backgroundButton)

        self.fontSize = QtGui.QComboBox(self.layoutWidget)
        self.fontSize.setObjectName("fontSize")
        self.hboxlayout1.addWidget(self.fontSize)

        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout1.addWidget(self.line)

        self.smileys = QtGui.QToolButton(self.layoutWidget)
        self.smileys.setIcon(QtGui.QIcon("images/16x16/emotes/biggrin.png"))
        self.smileys.setCheckable(True)
        self.smileys.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.smileys.setObjectName("smileys")
        self.hboxlayout1.addWidget(self.smileys)

        self.sendButton = QtGui.QPushButton(self.layoutWidget)
        self.sendButton.setIcon(QtGui.QIcon("images/16x16/actions/send.png"))
        self.sendButton.setObjectName("sendButton")
        self.hboxlayout1.addWidget(self.sendButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.layoutWidget1 = QtGui.QWidget(self.splitter_2)
        self.layoutWidget1.setObjectName("layoutWidget1")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.avatar = QtGui.QLabel(self.layoutWidget1)
        self.avatar.setAlignment(QtCore.Qt.AlignCenter)
        self.avatar.setObjectName("avatar")
        self.vboxlayout1.addWidget(self.avatar)

        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.vboxlayout1.addWidget(self.label)

        self.chatstate = QtGui.QLabel(self.layoutWidget1)
        self.chatstate.setAlignment(QtCore.Qt.AlignCenter)
        self.chatstate.setObjectName("chatstate")
        self.vboxlayout1.addWidget(self.chatstate)

        self.pluginWidget = QtGui.QWidget(self.layoutWidget1)
        self.pluginWidget.setObjectName("pluginWidget")
        self.vboxlayout1.addWidget(self.pluginWidget)

        self.ftwidget = QtGui.QWidget(self.layoutWidget1)
        self.ftwidget.setObjectName("ftwidget")
        self.vboxlayout1.addWidget(self.ftwidget)

        spacerItem1 = QtGui.QSpacerItem(20,281,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)
        self.gridlayout.addWidget(self.splitter_2,0,0,1,1)

        self.retranslateUi(chatwidget)
        QtCore.QMetaObject.connectSlotsByName(chatwidget)

    def retranslateUi(self, chatwidget):
        chatwidget.setWindowTitle(QtGui.QApplication.translate("chatwidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.boldButton.setText(QtGui.QApplication.translate("chatwidget", "Bold", None, QtGui.QApplication.UnicodeUTF8))
        self.italicButton.setText(QtGui.QApplication.translate("chatwidget", "Italic", None, QtGui.QApplication.UnicodeUTF8))
        self.underlineButton.setText(QtGui.QApplication.translate("chatwidget", "Underline", None, QtGui.QApplication.UnicodeUTF8))
        self.smileys.setText(QtGui.QApplication.translate("chatwidget", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("chatwidget", "&Send", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("chatwidget", "name", None, QtGui.QApplication.UnicodeUTF8))

