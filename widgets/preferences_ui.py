# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/preferences.ui'
#
# Created: Sun Nov 11 11:51:57 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_preferences(object):
    def setupUi(self, preferences):
        preferences.setObjectName("preferences")
        preferences.resize(QtCore.QSize(QtCore.QRect(0,0,676,420).size()).expandedTo(preferences.minimumSizeHint()))
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

        self.gridlayout2 = QtGui.QGridLayout(self.userPreferences)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem1 = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem1,4,0,1,1)

        self.groupBox_2 = QtGui.QGroupBox(self.userPreferences)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.gridlayout4 = QtGui.QGridLayout()
        self.gridlayout4.setMargin(0)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_15 = QtGui.QLabel(self.groupBox_2)
        self.label_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.vboxlayout.addWidget(self.label_15)

        self.label_16 = QtGui.QLabel(self.groupBox_2)
        self.label_16.setObjectName("label_16")
        self.vboxlayout.addWidget(self.label_16)
        self.gridlayout4.addLayout(self.vboxlayout,0,0,1,1)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.connection_source = QtGui.QLineEdit(self.groupBox_2)
        self.connection_source.setObjectName("connection_source")
        self.vboxlayout1.addWidget(self.connection_source)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem2 = QtGui.QSpacerItem(41,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem2)

        self.connection_priority = QtGui.QSpinBox(self.groupBox_2)
        self.connection_priority.setMinimum(-128)
        self.connection_priority.setMaximum(127)
        self.connection_priority.setObjectName("connection_priority")
        self.hboxlayout.addWidget(self.connection_priority)

        self.connection_autoPriority = QtGui.QCheckBox(self.groupBox_2)
        self.connection_autoPriority.setObjectName("connection_autoPriority")
        self.hboxlayout.addWidget(self.connection_autoPriority)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.gridlayout4.addLayout(self.vboxlayout1,0,1,1,1)
        self.gridlayout3.addLayout(self.gridlayout4,0,0,1,1)
        self.gridlayout2.addWidget(self.groupBox_2,3,0,1,2)

        self.groupBox_4 = QtGui.QGroupBox(self.userPreferences)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.label_2 = QtGui.QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.vboxlayout2.addWidget(self.label_2)

        self.label_3 = QtGui.QLabel(self.groupBox_4)
        self.label_3.setObjectName("label_3")
        self.vboxlayout2.addWidget(self.label_3)

        self.label_41 = QtGui.QLabel(self.groupBox_4)
        self.label_41.setObjectName("label_41")
        self.vboxlayout2.addWidget(self.label_41)
        self.hboxlayout1.addLayout(self.vboxlayout2)

        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setMargin(0)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.connection_jid = QtGui.QLineEdit(self.groupBox_4)
        self.connection_jid.setMinimumSize(QtCore.QSize(150,0))
        self.connection_jid.setMaximumSize(QtCore.QSize(16777215,16777215))
        self.connection_jid.setObjectName("connection_jid")
        self.vboxlayout3.addWidget(self.connection_jid)

        self.connection_password = QtGui.QLineEdit(self.groupBox_4)
        self.connection_password.setEchoMode(QtGui.QLineEdit.Password)
        self.connection_password.setObjectName("connection_password")
        self.vboxlayout3.addWidget(self.connection_password)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.connection_autojoin = QtGui.QCheckBox(self.groupBox_4)
        self.connection_autojoin.setObjectName("connection_autojoin")
        self.hboxlayout2.addWidget(self.connection_autojoin)
        self.vboxlayout3.addLayout(self.hboxlayout2)
        self.hboxlayout1.addLayout(self.vboxlayout3)
        self.gridlayout5.addLayout(self.hboxlayout1,0,0,1,1)
        self.gridlayout2.addWidget(self.groupBox_4,2,0,1,2)

        self.line = QtGui.QFrame(self.userPreferences)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout2.addWidget(self.line,1,0,1,1)

        self.label = QtGui.QLabel(self.userPreferences)
        self.label.setObjectName("label")
        self.gridlayout2.addWidget(self.label,0,0,1,1)
        self.stackedWidget.addWidget(self.userPreferences)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout6 = QtGui.QGridLayout(self.page_2)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.line_3 = QtGui.QFrame(self.page_2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout6.addWidget(self.line_3,1,0,1,1)

        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout6.addWidget(self.label_5,0,0,1,1)

        self.groupBox_5 = QtGui.QGroupBox(self.page_2)
        self.groupBox_5.setObjectName("groupBox_5")

        self.vboxlayout4 = QtGui.QVBoxLayout(self.groupBox_5)
        self.vboxlayout4.setSpacing(6)
        self.vboxlayout4.setMargin(9)
        self.vboxlayout4.setObjectName("vboxlayout4")

        self.useMUCNames = QtGui.QCheckBox(self.groupBox_5)
        self.useMUCNames.setObjectName("useMUCNames")
        self.vboxlayout4.addWidget(self.useMUCNames)
        self.gridlayout6.addWidget(self.groupBox_5,4,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,171,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout6.addItem(spacerItem3,5,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.page_2)
        self.groupBox_3.setObjectName("groupBox_3")

        self.vboxlayout5 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout5.setSpacing(6)
        self.vboxlayout5.setMargin(9)
        self.vboxlayout5.setObjectName("vboxlayout5")

        self.showChatStatusChanges = QtGui.QCheckBox(self.groupBox_3)
        self.showChatStatusChanges.setObjectName("showChatStatusChanges")
        self.vboxlayout5.addWidget(self.showChatStatusChanges)
        self.gridlayout6.addWidget(self.groupBox_3,3,0,1,1)

        self.sendByCtrl = QtGui.QCheckBox(self.page_2)
        self.sendByCtrl.setObjectName("sendByCtrl")
        self.gridlayout6.addWidget(self.sendByCtrl,2,0,1,1)
        self.stackedWidget.addWidget(self.page_2)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout7 = QtGui.QGridLayout(self.page)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        spacerItem4 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout7.addItem(spacerItem4,5,0,1,1)

        self.showTransports = QtGui.QCheckBox(self.page)
        self.showTransports.setObjectName("showTransports")
        self.gridlayout7.addWidget(self.showTransports,4,0,1,2)

        spacerItem5 = QtGui.QSpacerItem(81,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout7.addItem(spacerItem5,3,1,1,1)

        self.line_5 = QtGui.QFrame(self.page)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridlayout7.addWidget(self.line_5,1,0,1,2)

        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setObjectName("label_6")
        self.gridlayout7.addWidget(self.label_6,0,0,1,2)

        self.groupBox = QtGui.QGroupBox(self.page)
        self.groupBox.setObjectName("groupBox")

        self.vboxlayout6 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout6.setSpacing(6)
        self.vboxlayout6.setMargin(9)
        self.vboxlayout6.setObjectName("vboxlayout6")

        self.roster_normal = QtGui.QRadioButton(self.groupBox)
        self.roster_normal.setChecked(True)
        self.roster_normal.setObjectName("roster_normal")
        self.vboxlayout6.addWidget(self.roster_normal)

        self.roster_compact = QtGui.QRadioButton(self.groupBox)
        self.roster_compact.setObjectName("roster_compact")
        self.vboxlayout6.addWidget(self.roster_compact)
        self.gridlayout7.addWidget(self.groupBox,2,0,2,1)
        self.stackedWidget.addWidget(self.page)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout8 = QtGui.QGridLayout(self.page_3)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.tabWidget = QtGui.QTabWidget(self.page_3)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout9 = QtGui.QGridLayout(self.tab)
        self.gridlayout9.setMargin(9)
        self.gridlayout9.setSpacing(6)
        self.gridlayout9.setObjectName("gridlayout9")

        self.useThemes = QtGui.QCheckBox(self.tab)
        self.useThemes.setChecked(True)
        self.useThemes.setObjectName("useThemes")
        self.gridlayout9.addWidget(self.useThemes,0,0,1,1)

        self.themes = QtGui.QListWidget(self.tab)
        self.themes.setIconSize(QtCore.QSize(128,128))
        self.themes.setObjectName("themes")
        self.gridlayout9.addWidget(self.themes,1,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout10 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout10.setMargin(9)
        self.gridlayout10.setSpacing(6)
        self.gridlayout10.setObjectName("gridlayout10")

        self.chatSkin_preview = QtGui.QTextBrowser(self.tab_2)
        self.chatSkin_preview.setObjectName("chatSkin_preview")
        self.gridlayout10.addWidget(self.chatSkin_preview,1,0,1,2)

        self.chatSkin_list = QtGui.QComboBox(self.tab_2)
        self.chatSkin_list.setMinimumSize(QtCore.QSize(130,0))
        self.chatSkin_list.setObjectName("chatSkin_list")
        self.gridlayout10.addWidget(self.chatSkin_list,0,0,1,1)

        spacerItem6 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout10.addItem(spacerItem6,0,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout8.addWidget(self.tabWidget,2,0,1,1)

        self.label_7 = QtGui.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.gridlayout8.addWidget(self.label_7,0,0,1,1)

        self.line_6 = QtGui.QFrame(self.page_3)
        self.line_6.setFrameShape(QtGui.QFrame.HLine)
        self.line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.gridlayout8.addWidget(self.line_6,1,0,1,1)
        self.stackedWidget.addWidget(self.page_3)

        self.page_5 = QtGui.QWidget()
        self.page_5.setObjectName("page_5")

        self.gridlayout11 = QtGui.QGridLayout(self.page_5)
        self.gridlayout11.setMargin(9)
        self.gridlayout11.setSpacing(6)
        self.gridlayout11.setObjectName("gridlayout11")

        self.pluginConfiguration = QtGui.QPushButton(self.page_5)
        self.pluginConfiguration.setObjectName("pluginConfiguration")
        self.gridlayout11.addWidget(self.pluginConfiguration,3,1,1,1)

        self.plugins = QtGui.QTreeWidget(self.page_5)
        self.plugins.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plugins.setAlternatingRowColors(True)
        self.plugins.setRootIsDecorated(False)
        self.plugins.setObjectName("plugins")
        self.plugins.headerItem().setText(0,"")
        self.gridlayout11.addWidget(self.plugins,2,0,1,2)

        spacerItem7 = QtGui.QSpacerItem(261,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout11.addItem(spacerItem7,3,0,1,1)

        self.label_8 = QtGui.QLabel(self.page_5)
        self.label_8.setObjectName("label_8")
        self.gridlayout11.addWidget(self.label_8,0,0,1,2)

        self.line_7 = QtGui.QFrame(self.page_5)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridlayout11.addWidget(self.line_7,1,0,1,2)
        self.stackedWidget.addWidget(self.page_5)
        self.gridlayout.addWidget(self.stackedWidget,0,1,1,2)

        self.listWidget = QtGui.QListWidget(preferences)
        self.listWidget.setMinimumSize(QtCore.QSize(190,0))
        self.listWidget.setIconSize(QtCore.QSize(32,32))
        self.listWidget.setViewMode(QtGui.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,2,1)

        spacerItem8 = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem8,1,1,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setObjectName("hboxlayout3")

        self.saveButton = QtGui.QPushButton(preferences)
        self.saveButton.setObjectName("saveButton")
        self.hboxlayout3.addWidget(self.saveButton)

        self.cancelButton = QtGui.QPushButton(preferences)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout3.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout3,1,2,1,1)

        self.retranslateUi(preferences)
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),preferences.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),preferences.accept)
        QtCore.QObject.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.useThemes,QtCore.SIGNAL("toggled(bool)"),self.themes.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        preferences.setWindowTitle(QtGui.QApplication.translate("preferences", "Jabbim - Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Jabbim</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.savePosition.setToolTip(QtGui.QApplication.translate("preferences", "Jabbim will remember its position and geometry.", None, QtGui.QApplication.UnicodeUTF8))
        self.savePosition.setText(QtGui.QApplication.translate("preferences", "Save Jabbim position on close", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("preferences", "Advanced", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("preferences", "Resource:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("preferences", "Priority:", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_autoPriority.setToolTip(QtGui.QApplication.translate("preferences", "Priority steps are per 5 numbers: 25 for chatty, 20 for available, etc", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_autoPriority.setText(QtGui.QApplication.translate("preferences", "Change priority automatically due to status", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("preferences", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("preferences", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_41.setText(QtGui.QApplication.translate("preferences", "Autojoin:", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_jid.setToolTip(QtGui.QApplication.translate("preferences", "It has the form: nickname@jabber_server.org", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_password.setToolTip(QtGui.QApplication.translate("preferences", "Fill in your secret password :)", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_autojoin.setToolTip(QtGui.QApplication.translate("preferences", "Jabbim will join automatically if password and <br> Jabber ID are saved.", None, QtGui.QApplication.UnicodeUTF8))
        self.connection_autojoin.setText(QtGui.QApplication.translate("preferences", "Automatically join at startup.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Connection</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><span style=\" font-size:12pt; font-weight:600;\">Chat</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("preferences", "Groupchat", None, QtGui.QApplication.UnicodeUTF8))
        self.useMUCNames.setText(QtGui.QApplication.translate("preferences", "Use names for tabs", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("preferences", "Normal chat", None, QtGui.QApplication.UnicodeUTF8))
        self.showChatStatusChanges.setText(QtGui.QApplication.translate("preferences", "Show status message", None, QtGui.QApplication.UnicodeUTF8))
        self.sendByCtrl.setText(QtGui.QApplication.translate("preferences", "Sends messages with ctrl+enter", None, QtGui.QApplication.UnicodeUTF8))
        self.showTransports.setText(QtGui.QApplication.translate("preferences", "Show transports", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Roster</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("preferences", "Roster Style", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_normal.setToolTip(QtGui.QApplication.translate("preferences", "Big status icons, big avatars and you will see status messages, ", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_normal.setText(QtGui.QApplication.translate("preferences", "Normal", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_compact.setToolTip(QtGui.QApplication.translate("preferences", "Smaller  status icons and avatars, no status messages.", None, QtGui.QApplication.UnicodeUTF8))
        self.roster_compact.setText(QtGui.QApplication.translate("preferences", "Compact", None, QtGui.QApplication.UnicodeUTF8))
        self.useThemes.setText(QtGui.QApplication.translate("preferences", "Use themes", None, QtGui.QApplication.UnicodeUTF8))
        self.themes.setToolTip(QtGui.QApplication.translate("preferences", "Choose whe theme of Jabbim, then restart the client", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("preferences", "Themes", None, QtGui.QApplication.UnicodeUTF8))
        self.chatSkin_preview.setToolTip(QtGui.QApplication.translate("preferences", "Here you see preview of the selected chat look.", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("preferences", "Chat Themes", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><span style=\" font-size:12pt; font-weight:600;\">View</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pluginConfiguration.setText(QtGui.QApplication.translate("preferences", "Plugin configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.plugins.setToolTip(QtGui.QApplication.translate("preferences", "Tick plugins you want to use, right click to change settings.", None, QtGui.QApplication.UnicodeUTF8))
        self.plugins.headerItem().setText(1,QtGui.QApplication.translate("preferences", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.plugins.headerItem().setText(2,QtGui.QApplication.translate("preferences", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><span style=\" font-size:12pt; font-weight:600;\">Plugins</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget.clear()

        item = QtGui.QListWidgetItem(self.listWidget)
        item.setText(QtGui.QApplication.translate("preferences", "Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(QtGui.QIcon("images/32x32/apps/jabbim.png"))

        item1 = QtGui.QListWidgetItem(self.listWidget)
        item1.setText(QtGui.QApplication.translate("preferences", "Connection", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(QtGui.QIcon("images/32x32/categories/applications-internet.png"))

        item2 = QtGui.QListWidgetItem(self.listWidget)
        item2.setText(QtGui.QApplication.translate("preferences", "Chat", None, QtGui.QApplication.UnicodeUTF8))
        item2.setIcon(QtGui.QIcon("images/32x32/apps/jabbim.png"))

        item3 = QtGui.QListWidgetItem(self.listWidget)
        item3.setText(QtGui.QApplication.translate("preferences", "Roster", None, QtGui.QApplication.UnicodeUTF8))
        item3.setIcon(QtGui.QIcon("images/32x32/categories/system-users.png"))

        item4 = QtGui.QListWidgetItem(self.listWidget)
        item4.setText(QtGui.QApplication.translate("preferences", "View", None, QtGui.QApplication.UnicodeUTF8))
        item4.setIcon(QtGui.QIcon("images/32x32/categories/preferences-desktop-theme.png"))

        item5 = QtGui.QListWidgetItem(self.listWidget)
        item5.setText(QtGui.QApplication.translate("preferences", "Plugins", None, QtGui.QApplication.UnicodeUTF8))
        item5.setIcon(QtGui.QIcon("images/32x32/categories/applications-accessories.png"))
        self.saveButton.setText(QtGui.QApplication.translate("preferences", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("preferences", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

