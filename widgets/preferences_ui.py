# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/preferences.ui'
#
# Created: Sat Dec  1 05:14:56 2007
#      by: PyQt4 UI code generator 4.3
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

        self.listWidget = QtGui.QListWidget(preferences)
        self.listWidget.setMinimumSize(QtCore.QSize(190,0))
        self.listWidget.setIconSize(QtCore.QSize(32,32))
        self.listWidget.setViewMode(QtGui.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,0,0,2,1)

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

        self.stackedWidget = QtGui.QStackedWidget(preferences)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page_4 = QtGui.QWidget()
        self.page_4.setObjectName("page_4")

        self.gridlayout1 = QtGui.QGridLayout(self.page_4)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_4 = QtGui.QLabel(self.page_4)
        self.label_4.setObjectName("label_4")
        self.gridlayout1.addWidget(self.label_4,0,0,1,1)

        self.line_2 = QtGui.QFrame(self.page_4)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout1.addWidget(self.line_2,1,0,1,1)

        self.jabbimWidget = QtGui.QWidget(self.page_4)
        self.jabbimWidget.setObjectName("jabbimWidget")
        self.gridlayout1.addWidget(self.jabbimWidget,3,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,261,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,4,0,1,1)
        self.stackedWidget.addWidget(self.page_4)

        self.userPreferences = QtGui.QWidget()
        self.userPreferences.setObjectName("userPreferences")

        self.gridlayout2 = QtGui.QGridLayout(self.userPreferences)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.connectionWidget = QtGui.QWidget(self.userPreferences)
        self.connectionWidget.setObjectName("connectionWidget")
        self.gridlayout2.addWidget(self.connectionWidget,2,0,1,1)

        self.label = QtGui.QLabel(self.userPreferences)
        self.label.setObjectName("label")
        self.gridlayout2.addWidget(self.label,0,0,1,1)

        self.line = QtGui.QFrame(self.userPreferences)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout2.addWidget(self.line,1,0,1,1)

        spacerItem2 = QtGui.QSpacerItem(20,16,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem2,5,0,1,1)
        self.stackedWidget.addWidget(self.userPreferences)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout3 = QtGui.QGridLayout(self.page_2)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.label_5 = QtGui.QLabel(self.page_2)
        self.label_5.setObjectName("label_5")
        self.gridlayout3.addWidget(self.label_5,0,0,1,1)

        self.line_3 = QtGui.QFrame(self.page_2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout3.addWidget(self.line_3,1,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,171,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout3.addItem(spacerItem3,6,0,1,1)

        self.chatWidget = QtGui.QWidget(self.page_2)
        self.chatWidget.setObjectName("chatWidget")
        self.gridlayout3.addWidget(self.chatWidget,2,0,1,1)
        self.stackedWidget.addWidget(self.page_2)

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout4 = QtGui.QGridLayout(self.page)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setObjectName("label_6")
        self.gridlayout4.addWidget(self.label_6,0,0,1,2)

        self.rosterWidget = QtGui.QWidget(self.page)
        self.rosterWidget.setObjectName("rosterWidget")
        self.gridlayout4.addWidget(self.rosterWidget,2,0,1,3)

        self.line_5 = QtGui.QFrame(self.page)
        self.line_5.setFrameShape(QtGui.QFrame.HLine)
        self.line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.gridlayout4.addWidget(self.line_5,1,0,1,2)

        spacerItem4 = QtGui.QSpacerItem(20,221,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem4,5,0,1,1)
        self.stackedWidget.addWidget(self.page)

        self.page_3 = QtGui.QWidget()
        self.page_3.setObjectName("page_3")

        self.gridlayout5 = QtGui.QGridLayout(self.page_3)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.tabWidget = QtGui.QTabWidget(self.page_3)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout6 = QtGui.QGridLayout(self.tab)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.useThemes = QtGui.QCheckBox(self.tab)
        self.useThemes.setChecked(True)
        self.useThemes.setObjectName("useThemes")
        self.gridlayout6.addWidget(self.useThemes,0,0,1,1)

        self.themes = QtGui.QListWidget(self.tab)
        self.themes.setIconSize(QtCore.QSize(128,128))
        self.themes.setObjectName("themes")
        self.gridlayout6.addWidget(self.themes,1,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout7 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.chatSkin_preview = QtGui.QTextBrowser(self.tab_2)
        self.chatSkin_preview.setObjectName("chatSkin_preview")
        self.gridlayout7.addWidget(self.chatSkin_preview,1,0,1,2)

        self.chatSkin_list = QtGui.QComboBox(self.tab_2)
        self.chatSkin_list.setMinimumSize(QtCore.QSize(130,0))
        self.chatSkin_list.setObjectName("chatSkin_list")
        self.gridlayout7.addWidget(self.chatSkin_list,0,0,1,1)

        spacerItem5 = QtGui.QSpacerItem(31,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout7.addItem(spacerItem5,0,1,1,1)
        self.tabWidget.addTab(self.tab_2,"")
        self.gridlayout5.addWidget(self.tabWidget,2,0,1,1)

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

        self.gridlayout8 = QtGui.QGridLayout(self.page_5)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")

        self.pluginConfiguration = QtGui.QPushButton(self.page_5)
        self.pluginConfiguration.setObjectName("pluginConfiguration")
        self.gridlayout8.addWidget(self.pluginConfiguration,3,1,1,1)

        self.plugins = QtGui.QTreeWidget(self.page_5)
        self.plugins.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plugins.setAlternatingRowColors(True)
        self.plugins.setRootIsDecorated(False)
        self.plugins.setObjectName("plugins")
        self.plugins.headerItem().setText(0,"")
        self.gridlayout8.addWidget(self.plugins,2,0,1,2)

        spacerItem6 = QtGui.QSpacerItem(261,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout8.addItem(spacerItem6,3,0,1,1)

        self.label_8 = QtGui.QLabel(self.page_5)
        self.label_8.setObjectName("label_8")
        self.gridlayout8.addWidget(self.label_8,0,0,1,2)

        self.line_7 = QtGui.QFrame(self.page_5)
        self.line_7.setFrameShape(QtGui.QFrame.HLine)
        self.line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.gridlayout8.addWidget(self.line_7,1,0,1,2)
        self.stackedWidget.addWidget(self.page_5)
        self.gridlayout.addWidget(self.stackedWidget,0,1,1,2)

        self.retranslateUi(preferences)
        self.stackedWidget.setCurrentIndex(3)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),preferences.reject)
        QtCore.QObject.connect(self.saveButton,QtCore.SIGNAL("clicked()"),preferences.accept)
        QtCore.QObject.connect(self.listWidget,QtCore.SIGNAL("currentRowChanged(int)"),self.stackedWidget.setCurrentIndex)
        QtCore.QObject.connect(self.useThemes,QtCore.SIGNAL("toggled(bool)"),self.themes.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(preferences)

    def retranslateUi(self, preferences):
        preferences.setWindowTitle(QtGui.QApplication.translate("preferences", "Jabbim - Preferences", None, QtGui.QApplication.UnicodeUTF8))
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
        self.label_4.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Jabbim</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Connection</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Sans Serif\';\"><span style=\" font-size:12pt; font-weight:600;\">Chat</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("preferences", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Roster</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
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

