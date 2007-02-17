# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
#
# Created: Sat Feb 17 07:06:59 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_preferences(object):
    def setupUi(self, preferences):
        preferences.setObjectName("preferences")
        preferences.resize(QtCore.QSize(QtCore.QRect(0,0,493,305).size()).expandedTo(preferences.minimumSizeHint()))
        preferences.setWindowIcon(QtGui.QIcon("images/16x16/jgames.png"))

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

        spacerItem = QtGui.QSpacerItem(20,91,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,3,0,1,1)

        self.line = QtGui.QFrame(self.userPreferences)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,2)

        self.label = QtGui.QLabel(self.userPreferences)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_2 = QtGui.QLabel(self.userPreferences)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(self.userPreferences)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.jid = QtGui.QLineEdit(self.userPreferences)
        self.jid.setMinimumSize(QtCore.QSize(150,0))
        self.jid.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.jid.setObjectName("jid")
        self.vboxlayout1.addWidget(self.jid)

        self.password = QtGui.QLineEdit(self.userPreferences)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName("password")
        self.vboxlayout1.addWidget(self.password)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout1.addLayout(self.hboxlayout,2,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(111,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem1,2,1,1,1)
        self.stackedWidget.addWidget(self.userPreferences)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout2 = QtGui.QGridLayout(self.page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.line_3 = QtGui.QFrame(self.page)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout2.addWidget(self.line_3,1,0,1,4)

        self.label_4 = QtGui.QLabel(self.page)
        self.label_4.setObjectName("label_4")
        self.gridlayout2.addWidget(self.label_4,0,0,1,4)

        self.bookmarks = QtGui.QTreeWidget(self.page)
        self.bookmarks.setRootIsDecorated(False)
        self.bookmarks.setSortingEnabled(True)
        self.bookmarks.setObjectName("bookmarks")
        self.gridlayout2.addWidget(self.bookmarks,2,0,1,4)

        self.removeBookmark = QtGui.QPushButton(self.page)
        self.removeBookmark.setObjectName("removeBookmark")
        self.gridlayout2.addWidget(self.removeBookmark,3,3,1,1)

        self.editBookmark = QtGui.QPushButton(self.page)
        self.editBookmark.setObjectName("editBookmark")
        self.gridlayout2.addWidget(self.editBookmark,3,2,1,1)

        self.addBookmark = QtGui.QPushButton(self.page)
        self.addBookmark.setObjectName("addBookmark")
        self.gridlayout2.addWidget(self.addBookmark,3,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(71,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem2,3,0,1,1)
        self.stackedWidget.addWidget(self.page)

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

        spacerItem3 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem3,2,1,1,1)

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
        self.gridlayout.addWidget(self.stackedWidget,0,1,1,3)

        spacerItem4 = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,2,1,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.saveButton = QtGui.QPushButton(preferences)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout1.addWidget(self.saveButton)

        self.cancelButton = QtGui.QPushButton(preferences)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout1.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout1,2,3,1,1)

        self.listWidget = QtGui.QListWidget(preferences)
        self.listWidget.setMaximumSize(QtCore.QSize(150,16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,3,1)

        self.line_2 = QtGui.QFrame(preferences)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout.addWidget(self.line_2,1,1,1,3)

        self.retranslateUi(preferences)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),preferences.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),preferences.accept)
        QtCore.QObject.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        preferences.setWindowTitle(QtGui.QApplication.translate("preferences", "jGames - Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Connection</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("preferences", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("preferences", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Bookmarks</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(0,QtGui.QApplication.translate("preferences", "Room", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmarks.headerItem().setText(1,QtGui.QApplication.translate("preferences", "Nickname", None, QtGui.QApplication.UnicodeUTF8))
        self.removeBookmark.setText(QtGui.QApplication.translate("preferences", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.editBookmark.setText(QtGui.QApplication.translate("preferences", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.addBookmark.setText(QtGui.QApplication.translate("preferences", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Chat skins</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("preferences", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("preferences", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))

        item1 = QtGui.QListWidgetItem(self.listWidget)
        item1.setText(QtGui.QApplication.translate("preferences", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))

        item2 = QtGui.QListWidgetItem(self.listWidget)
        item2.setText(QtGui.QApplication.translate("preferences", "Chat skins", None, QtGui.QApplication.UnicodeUTF8))
