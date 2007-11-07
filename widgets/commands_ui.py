# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/commands.ui'
#
# Created: Wed Nov  7 21:07:14 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,318,116).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.close = QtGui.QPushButton(Dialog)
        self.close.setObjectName("close")
        self.gridlayout1.addWidget(self.close,0,2,1,1)

        self.execute = QtGui.QPushButton(Dialog)
        self.execute.setObjectName("execute")
        self.gridlayout1.addWidget(self.execute,0,1,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)
        self.gridlayout.addLayout(self.gridlayout1,2,0,1,1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")
        self.gridlayout.addLayout(self.gridlayout2,0,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,1,0,1,1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.close,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.execute.setText(QtGui.QApplication.translate("Dialog", "Execute", None, QtGui.QApplication.UnicodeUTF8))

