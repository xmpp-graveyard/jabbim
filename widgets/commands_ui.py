# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'commands.ui'
#
# Created: Fri Nov  9 18:23:32 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,447,148).size()).expandedTo(Dialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(Dialog)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setObjectName("gridlayout1")

        self.cancel = QtGui.QPushButton(Dialog)
        self.cancel.setObjectName("cancel")
        self.gridlayout1.addWidget(self.cancel,0,4,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.next = QtGui.QPushButton(Dialog)
        self.next.setObjectName("next")
        self.gridlayout1.addWidget(self.next,0,3,1,1)

        self.complete = QtGui.QPushButton(Dialog)
        self.complete.setObjectName("complete")
        self.gridlayout1.addWidget(self.complete,0,2,1,1)

        self.previous = QtGui.QPushButton(Dialog)
        self.previous.setObjectName("previous")
        self.gridlayout1.addWidget(self.previous,0,1,1,1)

        self.close = QtGui.QPushButton(Dialog)
        self.close.setObjectName("close")
        self.gridlayout1.addWidget(self.close,0,5,1,1)
        self.gridlayout.addLayout(self.gridlayout1,5,0,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)
        self.gridlayout.addLayout(self.vboxlayout,0,0,3,1)

        self.gridlayout2 = QtGui.QGridLayout()
        self.gridlayout2.setObjectName("gridlayout2")
        self.gridlayout.addLayout(self.gridlayout2,3,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1,4,0,1,1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.close,QtCore.SIGNAL("clicked()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Extra action", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setText(QtGui.QApplication.translate("Dialog", "Next →", None, QtGui.QApplication.UnicodeUTF8))
        self.complete.setText(QtGui.QApplication.translate("Dialog", "Finish", None, QtGui.QApplication.UnicodeUTF8))
        self.previous.setText(QtGui.QApplication.translate("Dialog", "← Back", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

