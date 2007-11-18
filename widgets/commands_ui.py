# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/commands.ui'
#
# Created: Sun Nov 18 15:28:58 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,436,358).size()).expandedTo(Dialog.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.cancel = QtGui.QPushButton(self.centralwidget)
        self.cancel.setObjectName("cancel")
        self.gridlayout1.addWidget(self.cancel,0,4,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,0,1,1)

        self.next = QtGui.QPushButton(self.centralwidget)
        self.next.setObjectName("next")
        self.gridlayout1.addWidget(self.next,0,3,1,1)

        self.complete = QtGui.QPushButton(self.centralwidget)
        self.complete.setObjectName("complete")
        self.gridlayout1.addWidget(self.complete,0,2,1,1)

        self.previous = QtGui.QPushButton(self.centralwidget)
        self.previous.setObjectName("previous")
        self.gridlayout1.addWidget(self.previous,0,1,1,1)

        self.close = QtGui.QPushButton(self.centralwidget)
        self.close.setObjectName("close")
        self.gridlayout1.addWidget(self.close,0,5,1,1)
        self.gridlayout.addLayout(self.gridlayout1,1,0,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.vboxlayout.addWidget(self.line)
        self.gridlayout.addLayout(self.vboxlayout,0,0,1,1)
        Dialog.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(Dialog)
        self.statusbar.setObjectName("statusbar")
        Dialog.setStatusBar(self.statusbar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Extra action", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.next.setText(QtGui.QApplication.translate("Dialog", "Next →", None, QtGui.QApplication.UnicodeUTF8))
        self.complete.setText(QtGui.QApplication.translate("Dialog", "Finish", None, QtGui.QApplication.UnicodeUTF8))
        self.previous.setText(QtGui.QApplication.translate("Dialog", "← Back", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

