# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/preferences.ui'
#
# Created: Sun Jul 29 17:01:51 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_preferences(object):
    def setupUi(self, preferences):
        preferences.setObjectName("preferences")
        preferences.resize(QtCore.QSize(QtCore.QRect(0,0,591,420).size()).expandedTo(preferences.minimumSizeHint()))
        preferences.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.gridlayout = QtGui.QGridLayout(preferences)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.stackedWidget = QtGui.QStackedWidget(preferences)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")

        self.gridlayout1 = QtGui.QGridLayout(self.page_4)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.line_2 = QtGui.QFrame(self.page_4)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout1.addWidget(self.line_2,1,0,1,1)

        self.label_4 = QtGui.QLabel(self.page_4)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(20,261,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,3,0,1,1)

        self.savePosition = QtGui.QCheckBox(self.page_4)
        self.savePosition.setChecked(True)
        self.savePosition.setObjectName("savePosition")
        self.gridlayout1.addWidget(self.savePosition,2,0,1,1)
        self.stackedWidget.addWidget(self.page_4)

        self.userPreferences = QtGui.QWidget()
        self.userPreferences.setObjectName("userPreferences")

        self.vboxlayout = QtGui.QVBoxLayout(self.userPreferences)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.userPreferences)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.line = QtGui.QFrame(self.userPreferences)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)

        self.groupBox_4 = QtGui.QGroupBox(self.userPreferences)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem1 = QtGui.QSpacerItem(51,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1,1,0,1,1)

        self.connection_autojoin = QtGui.QCheckBox(self.groupBox_4)
        self.connection_autojoin.setObjectName("connection_autojoin")
        self.gridlayout2.addWidget(self.connection_autojoin,1,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.vboxlayout1.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.vboxlayout1.addWidget(self.label_3)
        self.hboxlayout.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.connection_jid = QtGui.QLineEdit(self.groupBox_4)
        self.connection_jid.setMinimumSize(QtCore.QSize(150,0))
        self.connection_jid.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.connection_jid.setObjectName("connection_jid")
        self.vboxlayout2.addWidget(self.connection_jid)

        self.connection_password = QtGui.QLineEdit(self.groupBox_4)
        self.connection_password.setEchoMode(QtGui.QLineEdit.Password)
        self.connection_password.setObjectName("connection_password")
        self.vboxlayout2.addWidget(self.connection_password)
        self.hboxlayout.addLayout(self.vboxlayout2)
        self.gridlayout2.addLayout(self.hboxlayout,0,0,1,2)
        self.vboxlayout.addWidget(self.groupBox_4)

        spacerItem2 = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem2)
        self.stackedWidget.addWidget(self.userPreferences)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout3 = QtGui.QGridLayout(self.page_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.chatSkin_list = QtGui.QComboBox(self.page_2)
        self.chatSkin_list.setMinimumSize(QtCore.QSize(130,0))
        self.chatSkin_list.setObjectName("chatSkin_list")
        self.gridlayout3.addWidget(self.chatSkin_list,2,0,1,1)

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

        self.chatSkin_preview = QtGui.QTextBrowser(self.page_2)
        self.chatSkin_preview.setObjectName("chatSkin_preview")
        self.gridlayout3.addWidget(self.chatSkin_preview,3,0,1,2)
        self.stackedWidget.addWidget(self.page_2)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout4 = QtGui.QGridLayout(self.page)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        spacerItem4 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem4,4,0,1,1)

        self.label_10 = QtGui.QLabel(self.page)
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.gridlayout4.addWidget(self.label_10,3,0,1,1)

        self.groupBox = QtGui.QGroupBox(self.page)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.roster_normal = QtGui.QRadioButton(self.groupBox)
        self.roster_normal.setChecked(True)
        self.roster_normal.setObjectName("roster_normal")
        self.vboxlayout3.addWidget(self.roster_normal)

        self.roster_compact = QtGui.QRadioButton(self.groupBox)
        self.roster_compact.setObjectName("roster_compact")
        self.vboxlayout3.addWidget(self.roster_compact)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.hboxlayout1.addWidget(self.label_9)

        self.roster_iconSize = QtGui.QComboBox(self.groupBox)
        self.roster_iconSize.setObjectName("roster_iconSize")
        self.hboxlayout1.addWidget(self.roster_iconSize)
        self.vboxlayout3.addLayout(self.hboxlayout1)
        self.gridlayout4.addWidget(self.groupBox,2,0,1,1)

        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setObjectName("label_6")
        self.gridlayout4.addWidget(self.label_6,0,0,1,2)

        self.line_5 = QtGui.QFrame(self.page)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridlayout4.addWidget(self.line_5,1,0,1,2)

        spacerItem5 = QtGui.QSpacerItem(81,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem5,2,1,1,1)
        self.stackedWidget.addWidget(self.page)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout5 = QtGui.QGridLayout(self.page_3)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.themes = QtGui.QListWidget(self.page_3)
        self.themes.setIconSize(QtCore.QSize(128,128))
        self.themes.setViewMode(QtGui.QListView.IconMode)
        self.themes.setObjectName("themes")
        self.gridlayout5.addWidget(self.themes,2,0,1,1)

        self.label_7 = QtGui.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.gridlayout5.addWidget(self.label_7,0,0,1,1)

        self.line_6 = QtGui.QFrame(self.page_3)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridlayout5.addWidget(self.line_6,1,0,1,1)
        self.stackedWidget.addWidget(self.page_3)

        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")

        self.gridlayout6 = QtGui.QGridLayout(self.page_5)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.line_7 = QtGui.QFrame(self.page_5)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridlayout6.addWidget(self.line_7,1,0,1,1)

        self.label_8 = QtGui.QLabel(self.page_5)
        self.label_8.setObjectName("label_8")
        self.gridlayout6.addWidget(self.label_8,0,0,1,1)

        self.plugins = QtGui.QTreeWidget(self.page_5)
        self.plugins.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plugins.setAlternatingRowColors(True)
        self.plugins.setRootIsDecorated(False)
        self.plugins.setObjectName("plugins")
        self.plugins.headerItem().setText(0,"")
        self.gridlayout6.addWidget(self.plugins,2,0,1,1)
        self.stackedWidget.addWidget(self.page_5)
        self.gridlayout.addWidget(self.stackedWidget,0,1,1,2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.saveButton = QtGui.QPushButton(preferences)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout2.addWidget(self.saveButton)

        self.cancelButton = QtGui.QPushButton(preferences)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout2.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout2,1,2,1,1)

        spacerItem6 = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem6,1,1,1,1)

        self.listWidget = QtGui.QListWidget(preferences)
        self.listWidget.setMaximumSize(QtCore.QSize(150,16777215))
        self.listWidget.setIconSize(QtCore.QSize(32,32))
        self.listWidget.setViewMode(QtGui.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,2,1)

        self.retranslateUi(preferences)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),preferences.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),preferences.accept)
        QtCore.QObject.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.roster_compact,QtCore.SIGNAL("toggled(bool)"),self.roster_iconSize.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        preferences.setWindowTitle(QtGui.QApplication.translate("preferences", "Jabbim - Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Jabbim</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.savePosition.setText(QtGui.QApplication.translate("preferences", "Save Jabbim position on close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Connection</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_autojoin.setText(QtGui.QApplication.translate("preferences", "Automatically join at startup.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("preferences", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("preferences", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Chat skins</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("preferences", "Remember: you have to restart Jabbim to change roster style!", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("preferences", "Roster Style", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_normal.setText(QtGui.QApplication.translate("preferences", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_compact.setText(QtGui.QApplication.translate("preferences", "Compact", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("preferences", "Roster icons size:", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_iconSize.addItem(QtGui.QApplication.translate("preferences", "16x16", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_iconSize.addItem(QtGui.QApplication.translate("preferences", "22x22", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_iconSize.addItem(QtGui.QApplication.translate("preferences", "32x32", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Roster</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Themes</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><span style=\" font-size:12pt; font-weight:600;\">Plugins</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.plugins.headerItem().setText(1,QtGui.QApplication.translate("preferences", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.plugins.headerItem().setText(2,QtGui.QApplication.translate("preferences", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("preferences", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("preferences", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("preferences", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(QtGui.QIcon("images/32x32/apps/jabbim.png"))

        item1 = QtGui.QListWidgetItem(self.listWidget)
        item1.setText(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(QtGui.QIcon("images/32x32/categories/applications-internet.png"))

        item2 = QtGui.QListWidgetItem(self.listWidget)
        item2.setText(QtGui.QApplication.translate("preferences", "Chat skins", None, QtGui.QApplication.UnicodeUTF8))
        item2.setIcon(QtGui.QIcon("images/32x32/categories/applications-graphics.png"))

        item3 = QtGui.QListWidgetItem(self.listWidget)
        item3.setText(QtGui.QApplication.translate("preferences", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        item3.setIcon(QtGui.QIcon("images/32x32/categories/system-users.png"))

        item4 = QtGui.QListWidgetItem(self.listWidget)
        item4.setText(QtGui.QApplication.translate("preferences", "Themes", None, QtGui.QApplication.UnicodeUTF8))
        item4.setIcon(QtGui.QIcon("images/32x32/categories/preferences-desktop-theme.png"))

        item5 = QtGui.QListWidgetItem(self.listWidget)
        item5.setText(QtGui.QApplication.translate("preferences", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        item5.setIcon(QtGui.QIcon("images/32x32/categories/applications-accessories.png"))

