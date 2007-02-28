# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preparegame.ui'
#
# Created: Sat Feb 10 13:53:53 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_prepareGame(object):
    def setupUi(self, prepareGame):
        prepareGame.setObjectName("prepareGame")
        prepareGame.resize(QtCore.QSize(QtCore.QRect(0,0,322,207).size()).expandedTo(prepareGame.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(prepareGame)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.widget = QtGui.QWidget(prepareGame)
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.kriz = QtGui.QRadioButton(self.widget)
        self.kriz.setChecked(True)
        self.kriz.setObjectName("kriz")
        self.vboxlayout.addWidget(self.kriz)

        self.kolecko = QtGui.QRadioButton(self.widget)
        self.kolecko.setObjectName("kolecko")
        self.vboxlayout.addWidget(self.kolecko)
        self.hboxlayout.addLayout(self.vboxlayout)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.hboxlayout1.addWidget(self.label)

        self.width = QtGui.QSpinBox(self.widget)
        self.width.setMaximum(60)
        self.width.setProperty("value",QtCore.QVariant(15))
        self.width.setObjectName("width")
        self.hboxlayout1.addWidget(self.width)
        self.vboxlayout1.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.hboxlayout2.addWidget(self.label_2)

        self.heigth = QtGui.QSpinBox(self.widget)
        self.heigth.setMaximum(60)
        self.heigth.setProperty("value",QtCore.QVariant(15))
        self.heigth.setObjectName("heigth")
        self.hboxlayout2.addWidget(self.heigth)
        self.vboxlayout1.addLayout(self.hboxlayout2)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.gridlayout1.addLayout(self.hboxlayout,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(20,61,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem,1,0,1,1)

        self.hboxlayout3 = QtGui.QHBoxLayout()
        self.hboxlayout3.setMargin(0)
        self.hboxlayout3.setSpacing(6)
        self.hboxlayout3.setObjectName("hboxlayout3")

        spacerItem1 = QtGui.QSpacerItem(131,26,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout3.addItem(spacerItem1)

        self.play = QtGui.QPushButton(self.widget)
        self.play.setObjectName("play")
        self.hboxlayout3.addWidget(self.play)
        self.gridlayout1.addLayout(self.hboxlayout3,2,0,1,2)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem2,0,1,1,1)
        self.gridlayout.addWidget(self.widget,0,0,1,1)

        self.retranslateUi(prepareGame)
        QtCore.QMetaObject.connectSlotsByName(prepareGame)

    def retranslateUi(self, prepareGame):
        prepareGame.setWindowTitle(QtGui.QApplication.translate("prepareGame", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.kriz.setText(QtGui.QApplication.translate("prepareGame", "Cross", None, QtGui.QApplication.UnicodeUTF8))
        self.kolecko.setText(QtGui.QApplication.translate("prepareGame", "Circle", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("prepareGame", "Board width:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("prepareGame", "Board heigth", None, QtGui.QApplication.UnicodeUTF8))
        self.play.setText(QtGui.QApplication.translate("prepareGame", "Play", None, QtGui.QApplication.UnicodeUTF8))
