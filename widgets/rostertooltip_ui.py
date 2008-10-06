# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/rostertooltip.ui'
#
# Created: Mon Oct  6 14:43:00 2008
#      by: PyQt4 UI code generator 4.4.3-snapshot-20080611
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_RosterToolTip(object):
    def setupUi(self, RosterToolTip):
        RosterToolTip.setObjectName("RosterToolTip")
        RosterToolTip.resize(330, 70)
        self.gridlayout = QtGui.QGridLayout(RosterToolTip)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.nickname = QtGui.QLabel(RosterToolTip)
        self.nickname.setObjectName("nickname")
        self.vboxlayout.addWidget(self.nickname)
        self.jid = QtGui.QLabel(RosterToolTip)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7), QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jid.sizePolicy().hasHeightForWidth())
        self.jid.setSizePolicy(sizePolicy)
        self.jid.setObjectName("jid")
        self.vboxlayout.addWidget(self.jid)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.gridlayout.addLayout(self.vboxlayout, 0, 1, 2, 1)
        self.label = QtGui.QLabel(RosterToolTip)
        self.label.setMaximumSize(QtCore.QSize(16777215, 64))
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 41, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(RosterToolTip)
        QtCore.QMetaObject.connectSlotsByName(RosterToolTip)

    def retranslateUi(self, RosterToolTip):
        RosterToolTip.setWindowTitle(QtGui.QApplication.translate("RosterToolTip", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.nickname.setText(QtGui.QApplication.translate("RosterToolTip", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:12pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">HanzZ</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.jid.setText(QtGui.QApplication.translate("RosterToolTip", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'DejaVu Sans\'; font-size:12pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">JID:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("RosterToolTip", "Avatar", None, QtGui.QApplication.UnicodeUTF8))

