# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/mucbrowser.ui'
#
# Created: Sun Jan 27 09:56:41 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MUCBrowser(object):
    def setupUi(self, MUCBrowser):
        MUCBrowser.setObjectName("MUCBrowser")
        MUCBrowser.resize(QtCore.QSize(QtCore.QRect(0,0,712,389).size()).expandedTo(MUCBrowser.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(MUCBrowser)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(MUCBrowser)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.vboxlayout = QtGui.QVBoxLayout(self.widget)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.groupchats = QtGui.QTreeWidget(self.widget)
        self.groupchats.setAllColumnsShowFocus(True)
        self.groupchats.setObjectName("groupchats")
        self.groupchats.headerItem().setText(0,"")
        self.vboxlayout.addWidget(self.groupchats)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(100,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.label_5 = QtGui.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.hboxlayout.addWidget(self.label_5)

        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.hboxlayout.addWidget(self.lineEdit)

        self.serverChangeButton = QtGui.QPushButton(self.widget)
        self.serverChangeButton.setObjectName("serverChangeButton")
        self.hboxlayout.addWidget(self.serverChangeButton)

        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.showJid = QtGui.QCheckBox(self.widget)
        self.showJid.setObjectName("showJid")
        self.hboxlayout.addWidget(self.showJid)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.layoutWidget)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.groupBox = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout1 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.roomLabel = QtGui.QLabel(self.groupBox)
        self.roomLabel.setObjectName("roomLabel")
        self.gridlayout1.addWidget(self.roomLabel,0,0,1,2)

        self.serverLabel = QtGui.QLabel(self.groupBox)
        self.serverLabel.setObjectName("serverLabel")
        self.gridlayout1.addWidget(self.serverLabel,1,0,1,2)
        self.vboxlayout1.addWidget(self.groupBox)

        self.groupBox_2 = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.password = QtGui.QLineEdit(self.groupBox_2)
        self.password.setObjectName("password")
        self.gridlayout2.addWidget(self.password,1,1,1,1)

        self.nickname = QtGui.QLineEdit(self.groupBox_2)
        self.nickname.setObjectName("nickname")
        self.gridlayout2.addWidget(self.nickname,0,1,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridlayout2.addWidget(self.label_3,1,0,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridlayout2.addWidget(self.label_4,0,0,1,1)
        self.vboxlayout1.addWidget(self.groupBox_2)

        self.groupBox_3 = QtGui.QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.bookmark = QtGui.QCheckBox(self.groupBox_3)
        self.bookmark.setChecked(True)
        self.bookmark.setObjectName("bookmark")
        self.gridlayout3.addWidget(self.bookmark,1,0,1,2)

        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout3.addWidget(self.label_6,0,0,1,1)

        self.name = QtGui.QLineEdit(self.groupBox_3)
        self.name.setObjectName("name")
        self.gridlayout3.addWidget(self.name,0,1,1,1)
        self.vboxlayout1.addWidget(self.groupBox_3)

        spacerItem1 = QtGui.QSpacerItem(20,20,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem2)

        self.pushButton_2 = QtGui.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout1.addWidget(self.pushButton_2)

        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout1.addWidget(self.pushButton)
        self.vboxlayout1.addLayout(self.hboxlayout1)
        self.gridlayout.addWidget(self.splitter,0,0,1,1)

        self.retranslateUi(MUCBrowser)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),MUCBrowser.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),MUCBrowser.reject)
        QtCore.QObject.connect(self.bookmark,QtCore.SIGNAL("toggled(bool)"),self.name.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MUCBrowser)
        MUCBrowser.setTabOrder(self.nickname,self.password)
        MUCBrowser.setTabOrder(self.password,self.name)
        MUCBrowser.setTabOrder(self.name,self.bookmark)
        MUCBrowser.setTabOrder(self.bookmark,self.showJid)
        MUCBrowser.setTabOrder(self.showJid,self.pushButton_2)
        MUCBrowser.setTabOrder(self.pushButton_2,self.pushButton)
        MUCBrowser.setTabOrder(self.pushButton,self.groupchats)
        MUCBrowser.setTabOrder(self.groupchats,self.lineEdit)

    def retranslateUi(self, MUCBrowser):
        MUCBrowser.setWindowTitle(QtGui.QApplication.translate("MUCBrowser", "MUC Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchats.headerItem().setText(1,QtGui.QApplication.translate("MUCBrowser", "JID", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchats.headerItem().setText(2,QtGui.QApplication.translate("MUCBrowser", "Room name", None, QtGui.QApplication.UnicodeUTF8))
        self.groupchats.headerItem().setText(3,QtGui.QApplication.translate("MUCBrowser", "#", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MUCBrowser", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.serverChangeButton.setText(QtGui.QApplication.translate("MUCBrowser", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.showJid.setText(QtGui.QApplication.translate("MUCBrowser", "show JID", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MUCBrowser", "Room Informations", None, QtGui.QApplication.UnicodeUTF8))
        self.roomLabel.setText(QtGui.QApplication.translate("MUCBrowser", "Room:", None, QtGui.QApplication.UnicodeUTF8))
        self.serverLabel.setText(QtGui.QApplication.translate("MUCBrowser", "Server:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MUCBrowser", "User Informations", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MUCBrowser", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MUCBrowser", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MUCBrowser", "Bookmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark.setText(QtGui.QApplication.translate("MUCBrowser", "Bookmark this room", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MUCBrowser", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MUCBrowser", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MUCBrowser", "Join", None, QtGui.QApplication.UnicodeUTF8))

