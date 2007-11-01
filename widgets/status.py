# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/status.ui'
#
# Created: Thu Nov  1 04:51:47 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_status(object):
    def setupUi(self, status):
        status.setObjectName("status")
        status.resize(QtCore.QSize(QtCore.QRect(0,0,289,227).size()).expandedTo(status.minimumSizeHint()))
        status.setWindowIcon(QtGui.QIcon("images/16x16/jgames.png"))

        self.gridlayout = QtGui.QGridLayout(status)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.statusBox = QtGui.QComboBox(status)
        self.statusBox.setObjectName("statusBox")
        self.gridlayout.addWidget(self.statusBox,0,0,1,3)

        self.status = QtGui.QTextBrowser(status)
        self.status.setTabChangesFocus(True)
        self.status.setReadOnly(False)
        self.status.setObjectName("status")
        self.gridlayout.addWidget(self.status,1,0,1,3)

        self.time = QtGui.QLabel(status)
        self.time.setObjectName("time")
        self.gridlayout.addWidget(self.time,2,0,1,3)

        self.set = QtGui.QPushButton(status)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set.sizePolicy().hasHeightForWidth())
        self.set.setSizePolicy(sizePolicy)
        self.set.setIcon(QtGui.QIcon("images/16x16/actions/ok.png"))
        self.set.setObjectName("set")
        self.gridlayout.addWidget(self.set,3,2,1,1)

        self.pushButton = QtGui.QPushButton(status)
        self.pushButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,3,0,1,1)

        spacerItem = QtGui.QSpacerItem(91,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,3,1,1,1)

        self.retranslateUi(status)
        QtCore.QObject.connect(self.set,QtCore.SIGNAL("clicked()"),status.accept)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),status.reject)
        QtCore.QMetaObject.connectSlotsByName(status)

    def retranslateUi(self, status):
        status.setWindowTitle(QtGui.QApplication.translate("status", "Set status message", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setToolTip(QtGui.QApplication.translate("status", "Enter a short message describing your status (e.g. at lunch)", None, QtGui.QApplication.UnicodeUTF8))
        self.set.setText(QtGui.QApplication.translate("status", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("status", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

