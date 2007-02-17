# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences_bookmarks.ui'
#
# Created: Sat Feb 17 07:30:02 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_editbookmark(object):
    def setupUi(self, editbookmark):
        editbookmark.setObjectName("editbookmark")
        editbookmark.resize(QtCore.QSize(QtCore.QRect(0,0,295,119).size()).expandedTo(editbookmark.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(editbookmark)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(141,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.line = QtGui.QFrame(editbookmark)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,1,0,1,2)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton = QtGui.QPushButton(editbookmark)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)

        self.pushButton_2 = QtGui.QPushButton(editbookmark)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout.addWidget(self.pushButton_2)
        self.gridlayout.addLayout(self.hboxlayout,2,1,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(editbookmark)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_2 = QtGui.QLabel(editbookmark)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.hboxlayout1.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.room = QtGui.QLineEdit(editbookmark)
        self.room.setObjectName("room")
        self.vboxlayout1.addWidget(self.room)

        self.nickname = QtGui.QLineEdit(editbookmark)
        self.nickname.setObjectName("nickname")
        self.vboxlayout1.addWidget(self.nickname)
        self.hboxlayout1.addLayout(self.vboxlayout1)
        self.gridlayout.addLayout(self.hboxlayout1,0,0,1,2)

        self.retranslateUi(editbookmark)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),editbookmark.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),editbookmark.reject)
        QtCore.QMetaObject.connectSlotsByName(editbookmark)

    def retranslateUi(self, editbookmark):
        editbookmark.setWindowTitle(QtGui.QApplication.translate("editbookmark", "Edit bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("editbookmark", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("editbookmark", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("editbookmark", "Room:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("editbookmark", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
