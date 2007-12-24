# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/statuseditor.ui'
#
# Created: Mon Dec 24 06:10:24 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_statusEditor(object):
    def setupUi(self, statusEditor):
        statusEditor.setObjectName("statusEditor")
        statusEditor.resize(QtCore.QSize(QtCore.QRect(0,0,291,300).size()).expandedTo(statusEditor.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(statusEditor)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.removeStatus = QtGui.QPushButton(statusEditor)
        self.removeStatus.setObjectName("removeStatus")
        self.gridlayout.addWidget(self.removeStatus,2,1,1,2)

        self.statusList = QtGui.QListWidget(statusEditor)
        self.statusList.setIconSize(QtCore.QSize(22,22))
        self.statusList.setObjectName("statusList")
        self.gridlayout.addWidget(self.statusList,2,0,3,1)

        self.label = QtGui.QLabel(statusEditor)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,3)

        self.pushButton = QtGui.QPushButton(statusEditor)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,4,1,1,2)

        self.line = QtGui.QFrame(statusEditor)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridlayout.addWidget(self.line,1,0,1,3)

        spacerItem = QtGui.QSpacerItem(20,141,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,3,1,1,1)

        self.retranslateUi(statusEditor)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),statusEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(statusEditor)

    def retranslateUi(self, statusEditor):
        statusEditor.setWindowTitle(QtGui.QApplication.translate("statusEditor", "Remove message", None, QtGui.QApplication.UnicodeUTF8))
        self.removeStatus.setText(QtGui.QApplication.translate("statusEditor", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("statusEditor", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:16px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:x-large; font-weight:600;\"><span style=\" font-size:x-large;\">Remove status message</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("statusEditor", "Close", None, QtGui.QApplication.UnicodeUTF8))

