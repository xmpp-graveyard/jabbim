# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'piskvorky.ui'
#
# Created: Sat Jan 27 15:50:42 2007
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_piskvorky(object):
    def setupUi(self, piskvorky):
        piskvorky.setObjectName("piskvorky")
        piskvorky.resize(QtCore.QSize(QtCore.QRect(0,0,489,436).size()).expandedTo(piskvorky.minimumSizeHint()))
        piskvorky.setWindowIcon(QtGui.QIcon("../../images/16x16/jgames.png"))

        self.gridlayout = QtGui.QGridLayout(piskvorky)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gameFrame = QtGui.QFrame(piskvorky)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gameFrame.sizePolicy().hasHeightForWidth())
        self.gameFrame.setSizePolicy(sizePolicy)
        self.gameFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.gameFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.gameFrame.setObjectName("gameFrame")
        self.gridlayout.addWidget(self.gameFrame,0,0,1,3)

        self.dismiss = QtGui.QPushButton(piskvorky)
        self.dismiss.setObjectName("dismiss")
        self.gridlayout.addWidget(self.dismiss,1,2,1,1)

        spacerItem = QtGui.QSpacerItem(341,26,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,2)

        self.retranslateUi(piskvorky)
        QtCore.QObject.connect(self.dismiss,QtCore.SIGNAL("clicked()"),piskvorky.reject)
        QtCore.QMetaObject.connectSlotsByName(piskvorky)

    def retranslateUi(self, piskvorky):
        piskvorky.setWindowTitle(QtGui.QApplication.translate("piskvorky", "Piškvorky", None, QtGui.QApplication.UnicodeUTF8))
        self.dismiss.setText(QtGui.QApplication.translate("piskvorky", "Dismiss", None, QtGui.QApplication.UnicodeUTF8))
