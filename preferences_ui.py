# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Thu Mar 15 04:46:46 2007
#      by: PyQt4 UI code generator 4.1.1
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

        spacerItem = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.saveButton = QtGui.QPushButton(preferences)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout.addWidget(self.saveButton)

        self.cancelButton = QtGui.QPushButton(preferences)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout,1,2,1,1)

        self.listWidget = QtGui.QListWidget(preferences)
        self.listWidget.setMaximumSize(QtCore.QSize(150,16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,2,1)

        self.stackedWidget = QtGui.QStackedWidget(preferences)
        self.stackedWidget.setObjectName("stackedWidget")

        self.userPreferences = QtGui.QWidget()
        self.userPreferences.setObjectName("userPreferences")

        self.gridlayout1 = QtGui.QGridLayout(self.userPreferences)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        spacerItem1 = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,4,0,1,1)

        self.groupBox = QtGui.QGroupBox(self.userPreferences)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.vboxlayout.addWidget(self.label_6)

        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.vboxlayout.addWidget(self.label_9)

        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.vboxlayout.addWidget(self.label_10)

        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.vboxlayout.addWidget(self.label_7)

        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.vboxlayout.addWidget(self.label_8)
        self.hboxlayout1.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.proxy_type = QtGui.QComboBox(self.groupBox)
        self.proxy_type.setObjectName("proxy_type")
        self.vboxlayout1.addWidget(self.proxy_type)

        self.proxy_server = QtGui.QLineEdit(self.groupBox)
        self.proxy_server.setObjectName("proxy_server")
        self.vboxlayout1.addWidget(self.proxy_server)

        self.proxy_port = QtGui.QLineEdit(self.groupBox)
        self.proxy_port.setObjectName("proxy_port")
        self.vboxlayout1.addWidget(self.proxy_port)

        self.proxy_username = QtGui.QLineEdit(self.groupBox)
        self.proxy_username.setObjectName("proxy_username")
        self.vboxlayout1.addWidget(self.proxy_username)

        self.proxy_password = QtGui.QLineEdit(self.groupBox)
        self.proxy_password.setEchoMode(QtGui.QLineEdit.Password)
        self.proxy_password.setObjectName("proxy_password")
        self.vboxlayout1.addWidget(self.proxy_password)
        self.hboxlayout1.addLayout(self.vboxlayout1)
        self.gridlayout2.addLayout(self.hboxlayout1,0,0,1,1)
        self.gridlayout1.addWidget(self.groupBox,3,0,1,1)

        self.groupBox_4 = QtGui.QGroupBox(self.userPreferences)
        self.groupBox_4.setObjectName("groupBox_4")

        self.hboxlayout2 = QtGui.QHBoxLayout(self.groupBox_4)
        self.hboxlayout2.setMargin(9)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.vboxlayout2.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.vboxlayout2.addWidget(self.label_3)
        self.hboxlayout3.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.jid = QtGui.QLineEdit(self.groupBox_4)
        self.jid.setMinimumSize(QtCore.QSize(150,0))
        self.jid.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.jid.setObjectName("jid")
        self.vboxlayout3.addWidget(self.jid)

        self.password = QtGui.QLineEdit(self.groupBox_4)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.vboxlayout3.addWidget(self.password)
        self.hboxlayout3.addLayout(self.vboxlayout3)
        self.hboxlayout2.addLayout(self.hboxlayout3)
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

        self.gridlayout3 = QtGui.QGridLayout(self.page_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.chatSkins = QtGui.QComboBox(self.page_2)
        self.chatSkins.setMinimumSize(QtCore.QSize(130,0))
        self.chatSkins.setObjectName("chatSkins")
        self.gridlayout3.addWidget(self.chatSkins,2,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem2,2,1,1,1)

        self.line_4 = QtGui.QFrame(self.page_2)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridlayout3.addWidget(self.line_4,1,0,1,2)

        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout3.addWidget(self.label_5,0,0,1,2)

        self.chatSkinPreview = QtGui.QTextBrowser(self.page_2)
        self.chatSkinPreview.setObjectName("chatSkinPreview")
        self.gridlayout3.addWidget(self.chatSkinPreview,3,0,1,2)
        self.stackedWidget.addWidget(self.page_2)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout4 = QtGui.QGridLayout(self.page_3)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.tabWidget = QtGui.QTabWidget(self.page_3)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout5 = QtGui.QGridLayout(self.tab)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        spacerItem3 = QtGui.QSpacerItem(20,131,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout5.addItem(spacerItem3,1,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout6 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setMargin(0)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.notificationAll = QtGui.QRadioButton(self.groupBox_2)
        self.notificationAll.setObjectName("notificationAll")
        self.vboxlayout4.addWidget(self.notificationAll)

        self.notificationLoggedIn = QtGui.QRadioButton(self.groupBox_2)
        self.notificationLoggedIn.setObjectName("notificationLoggedIn")
        self.vboxlayout4.addWidget(self.notificationLoggedIn)

        self.notificationOnline = QtGui.QRadioButton(self.groupBox_2)
        self.notificationOnline.setObjectName("notificationOnline")
        self.vboxlayout4.addWidget(self.notificationOnline)
        self.gridlayout6.addLayout(self.vboxlayout4,0,0,1,1)
        self.gridlayout5.addWidget(self.groupBox_2,0,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout7 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        spacerItem4 = QtGui.QSpacerItem(20,171,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout7.addItem(spacerItem4,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout8 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.vboxlayout5 = QtGui.QVBoxLayout()
        self.vboxlayout5.setMargin(0)
        self.vboxlayout5.setSpacing(6)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.notification_new_message_all = QtGui.QRadioButton(self.groupBox_3)
        self.notification_new_message_all.setObjectName("notification_new_message_all")
        self.vboxlayout5.addWidget(self.notification_new_message_all)

        self.notification_new_message_chat = QtGui.QRadioButton(self.groupBox_3)
        self.notification_new_message_chat.setObjectName("notification_new_message_chat")
        self.vboxlayout5.addWidget(self.notification_new_message_chat)
        self.gridlayout8.addLayout(self.vboxlayout5,0,0,1,1)
        self.gridlayout7.addWidget(self.groupBox_3,0,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout4.addWidget(self.tabWidget,2,0,1,1)

        self.label_11 = QtGui.QLabel(self.page_3)
        self.label_11.setObjectName("label_11")
        self.gridlayout4.addWidget(self.label_11,0,0,1,1)

        self.line_5 = QtGui.QFrame(self.page_3)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridlayout4.addWidget(self.line_5,1,0,1,1)
        self.stackedWidget.addWidget(self.page_3)
        self.gridlayout.addWidget(self.stackedWidget,0,1,1,2)

        self.retranslateUi(preferences)
        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),preferences.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),preferences.accept)
        QtCore.QObject.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        preferences.setWindowTitle(QtGui.QApplication.translate("preferences", "Jabbim - Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("preferences", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("preferences", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QListWidgetItem(self.listWidget)
        item1.setText(QtGui.QApplication.translate("preferences", "Chat skins", None, QtGui.QApplication.UnicodeUTF8))

        item2 = QtGui.QListWidgetItem(self.listWidget)
        item2.setText(QtGui.QApplication.translate("preferences", "Notification", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("preferences", "Proxy settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("preferences", "Proxy type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("preferences", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("preferences", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("preferences", "User name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("preferences", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_type.addItem(QtGui.QApplication.translate("preferences", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_type.addItem(QtGui.QApplication.translate("preferences", "HTTP Proxy", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_type.addItem(QtGui.QApplication.translate("preferences", "SOCKS4", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_type.addItem(QtGui.QApplication.translate("preferences", "SOCKS5", None, QtGui.QApplication.UnicodeUTF8))
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
        self.groupBox_2.setTitle(QtGui.QApplication.translate("preferences", "Tray messages", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationAll.setText(QtGui.QApplication.translate("preferences", "All - Show all status change.", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationLoggedIn.setText(QtGui.QApplication.translate("preferences", "Logged in - Show message only if user logs in.", None, QtGui.QApplication.UnicodeUTF8))
        self.notificationOnline.setText(QtGui.QApplication.translate("preferences", "Online - Show message only if user gets Online.", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("preferences", "Status change", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("preferences", "Tray messages", None, QtGui.QApplication.UnicodeUTF8))
        self.notification_new_message_all.setText(QtGui.QApplication.translate("preferences", "Show tray message for all new messages", None, QtGui.QApplication.UnicodeUTF8))
        self.notification_new_message_chat.setText(QtGui.QApplication.translate("preferences", "Show tray message only for not opened chat", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("preferences", "New message", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Notification</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

