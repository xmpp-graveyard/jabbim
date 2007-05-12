# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/preferences.ui'
#
# Created: Sat May 12 08:44:11 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_preferences(object):
    def setupUi(self, preferences):
        preferences.setObjectName("preferences")
        preferences.resize(QtCore.QSize(QtCore.QRect(0,0,591,406).size()).expandedTo(preferences.minimumSizeHint()))
        preferences.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.gridlayout = QtGui.QGridLayout(preferences)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.stackedWidget = QtGui.QStackedWidget(preferences)
        self.stackedWidget.setObjectName("stackedWidget")

        self.userPreferences = QtGui.QWidget()
        self.userPreferences.setObjectName("userPreferences")

        self.gridlayout1 = QtGui.QGridLayout(self.userPreferences)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,4,0,1,1)

        self.groupBox_4 = QtGui.QGroupBox(self.userPreferences)
        self.groupBox_4.setObjectName("groupBox_4")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox_4)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)
        self.hboxlayout1.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.connection_jid = QtGui.QLineEdit(self.groupBox_4)
        self.connection_jid.setMinimumSize(QtCore.QSize(150,0))
        self.connection_jid.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.connection_jid.setObjectName("connection_jid")
        self.vboxlayout1.addWidget(self.connection_jid)

        self.connection_password = QtGui.QLineEdit(self.groupBox_4)
        self.connection_password.setEchoMode(QtGui.QLineEdit.Password)
        self.connection_password.setObjectName("connection_password")
        self.vboxlayout1.addWidget(self.connection_password)
        self.hboxlayout1.addLayout(self.vboxlayout1)
        self.hboxlayout.addLayout(self.hboxlayout1)
        self.gridlayout1.addWidget(self.groupBox_4,2,0,1,1)

        self.line = QtGui.QFrame(self.userPreferences)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,2)

        self.label = QtGui.QLabel(self.userPreferences)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)
        self.stackedWidget.addWidget(self.userPreferences)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout2 = QtGui.QGridLayout(self.page_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.chatSkin_list = QtGui.QComboBox(self.page_2)
        self.chatSkin_list.setMinimumSize(QtCore.QSize(130,0))
        self.chatSkin_list.setObjectName("chatSkin_list")
        self.gridlayout2.addWidget(self.chatSkin_list,2,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1,2,1,1,1)

        self.line_4 = QtGui.QFrame(self.page_2)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridlayout2.addWidget(self.line_4,1,0,1,2)

        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout2.addWidget(self.label_5,0,0,1,2)

        self.chatSkin_preview = QtGui.QTextBrowser(self.page_2)
        self.chatSkin_preview.setObjectName("chatSkin_preview")
        self.gridlayout2.addWidget(self.chatSkin_preview,3,0,1,2)
        self.stackedWidget.addWidget(self.page_2)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout3 = QtGui.QGridLayout(self.page)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        spacerItem2 = QtGui.QSpacerItem(181,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem2,2,1,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem3,3,0,1,1)

        self.groupBox_5 = QtGui.QGroupBox(self.page)
        self.groupBox_5.setObjectName("groupBox_5")

        self.gridlayout4 = QtGui.QGridLayout(self.groupBox_5)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_4 = QtGui.QLabel(self.groupBox_5)
        self.label_4.setObjectName("label_4")
        self.hboxlayout2.addWidget(self.label_4)

        self.roster_iconSize = QtGui.QComboBox(self.groupBox_5)
        self.roster_iconSize.setObjectName("roster_iconSize")
        self.hboxlayout2.addWidget(self.roster_iconSize)
        self.gridlayout4.addLayout(self.hboxlayout2,0,0,1,1)
        self.gridlayout3.addWidget(self.groupBox_5,2,0,1,1)

        self.line_5 = QtGui.QFrame(self.page)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridlayout3.addWidget(self.line_5,1,0,1,2)

        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setObjectName("label_6")
        self.gridlayout3.addWidget(self.label_6,0,0,1,2)
        self.stackedWidget.addWidget(self.page)
        self.gridlayout.addWidget(self.stackedWidget,0,1,1,2)

        self.listWidget = QtGui.QListWidget(preferences)
        self.listWidget.setMaximumSize(QtCore.QSize(150,16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,2,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.saveButton = QtGui.QPushButton(preferences)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout3.addWidget(self.saveButton)

        self.cancelButton = QtGui.QPushButton(preferences)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout3.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout3,1,2,1,1)

        spacerItem4 = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,1,1,1,1)

        self.retranslateUi(preferences)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),preferences.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),preferences.accept)
        QtCore.QObject.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        preferences.setWindowTitle(QtGui.QApplication.translate("preferences", "Jabbim - Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("preferences", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("preferences", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Connection</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Chat skins</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("preferences", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("preferences", "Icon size:", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_iconSize.addItem(QtGui.QApplication.translate("preferences", "16x16", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_iconSize.addItem(QtGui.QApplication.translate("preferences", "32x32", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Roster</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QListWidgetItem(self.listWidget)
        item1.setText(QtGui.QApplication.translate("preferences", "Chat skins", None, QtGui.QApplication.UnicodeUTF8))

        item2 = QtGui.QListWidgetItem(self.listWidget)
        item2.setText(QtGui.QApplication.translate("preferences", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("preferences", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("preferences", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

