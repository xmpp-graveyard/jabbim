# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'grouped_events.ui'
#
# Created: Mon Feb 26 18:17:35 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_groupedevents(object):
    def setupUi(self, groupedevents):
        groupedevents.setObjectName("groupedevents")
        groupedevents.resize(QtCore.QSize(QtCore.QRect(0,0,611,408).size()).expandedTo(groupedevents.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(groupedevents)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")

        self.page = QtGui.QWidget()
        self.page.setObjectName("page")

        self.gridlayout1 = QtGui.QGridLayout(self.page)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.line = QtGui.QFrame(self.page)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout1.addWidget(self.line,1,0,1,4)

        self.label = QtGui.QLabel(self.page)
        self.label.setObjectName("label")
        self.gridlayout1.addWidget(self.label,0,0,1,4)

        self.groupBox_2 = QtGui.QGroupBox(self.page)
        self.groupBox_2.setObjectName("groupBox_2")

        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.selectedUsers = QtGui.QListWidget(self.groupBox_2)
        self.selectedUsers.setObjectName("selectedUsers")
        self.vboxlayout.addWidget(self.selectedUsers)
        self.gridlayout1.addWidget(self.groupBox_2,4,0,1,1)

        self.line_2 = QtGui.QFrame(self.page)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridlayout1.addWidget(self.line_2,5,0,1,4)

        spacerItem = QtGui.QSpacerItem(201,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,6,0,1,1)

        self.addContact = QtGui.QPushButton(self.page)
        self.addContact.setObjectName("addContact")
        self.gridlayout1.addWidget(self.addContact,6,1,1,1)

        self.pushButton_2 = QtGui.QPushButton(self.page)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout1.addWidget(self.pushButton_2,6,2,1,2)

        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setObjectName("label_2")
        self.gridlayout1.addWidget(self.label_2,2,0,1,4)

        self.groupBox = QtGui.QGroupBox(self.page)
        self.groupBox.setObjectName("groupBox")

        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.vboxlayout1.addWidget(self.label_6)

        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.vboxlayout1.addWidget(self.label_7)
        self.hboxlayout1.addLayout(self.vboxlayout1)

        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.nickname = QtGui.QComboBox(self.groupBox)
        self.nickname.setMinimumSize(QtCore.QSize(200,0))
        self.nickname.setEditable(True)
        self.nickname.setObjectName("nickname")
        self.vboxlayout2.addWidget(self.nickname)

        self.group = QtGui.QComboBox(self.groupBox)
        self.group.setEditable(True)
        self.group.setObjectName("group")
        self.vboxlayout2.addWidget(self.group)
        self.hboxlayout1.addLayout(self.vboxlayout2)
        self.hboxlayout.addLayout(self.hboxlayout1)
        self.gridlayout1.addWidget(self.groupBox,3,0,1,3)

        spacerItem1 = QtGui.QSpacerItem(41,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem1,3,3,1,1)

        spacerItem2 = QtGui.QSpacerItem(201,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2,4,1,1,3)
        self.stackedWidget.addWidget(self.page)

        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")

        self.gridlayout2 = QtGui.QGridLayout(self.page_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        spacerItem3 = QtGui.QSpacerItem(20,261,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout2.addItem(spacerItem3,2,1,1,1)

        spacerItem4 = QtGui.QSpacerItem(161,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem4,4,0,1,1)

        self.ok = QtGui.QPushButton(self.page_2)
        self.ok.setObjectName("ok")
        self.gridlayout2.addWidget(self.ok,4,2,1,1)

        self.line_4 = QtGui.QFrame(self.page_2)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridlayout2.addWidget(self.line_4,3,0,1,3)

        self.line_3 = QtGui.QFrame(self.page_2)
        self.line_3.setFrameShape(QtGui.QFrame.HLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridlayout2.addWidget(self.line_3,1,0,1,3)

        self.label_8 = QtGui.QLabel(self.page_2)
        self.label_8.setObjectName("label_8")
        self.gridlayout2.addWidget(self.label_8,0,0,1,3)
        self.stackedWidget.addWidget(self.page_2)
        self.gridlayout.addWidget(self.stackedWidget,0,0,1,1)
        groupedevents.setCentralWidget(self.centralwidget)

        self.dockWidget = QtGui.QDockWidget(groupedevents)
        self.dockWidget.setBaseSize(QtCore.QSize(120,0))
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidget.setObjectName("dockWidget")

        self.dockWidgetContents = QtGui.QWidget(self.dockWidget)
        self.dockWidgetContents.setObjectName("dockWidgetContents")

        self.vboxlayout3 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName("vboxlayout3")

        self.events = QtGui.QTreeWidget(self.dockWidgetContents)
        self.events.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.events.setRootIsDecorated(False)
        self.events.setObjectName("events")
        self.vboxlayout3.addWidget(self.events)
        self.dockWidget.setWidget(self.dockWidgetContents)
        groupedevents.addDockWidget(QtCore.Qt.DockWidgetArea(1),self.dockWidget)

        self.retranslateUi(groupedevents)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),groupedevents.close)
        QtCore.QMetaObject.connectSlotsByName(groupedevents)

    def retranslateUi(self, groupedevents):
        groupedevents.setWindowTitle(QtGui.QApplication.translate("groupedevents", "Events", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("groupedevents", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Subscriptions</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("groupedevents", "Selected users", None, QtGui.QApplication.UnicodeUTF8))
        self.addContact.setText(QtGui.QApplication.translate("groupedevents", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("groupedevents", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("groupedevents", "Authorize all selected users and add them to the roster.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("groupedevents", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("groupedevents", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("groupedevents", "Group:", None, QtGui.QApplication.UnicodeUTF8))
        self.ok.setText(QtGui.QApplication.translate("groupedevents", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("groupedevents", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Subscribed</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.events.headerItem().setText(0,QtGui.QApplication.translate("groupedevents", "Jabber ID", None, QtGui.QApplication.UnicodeUTF8))

