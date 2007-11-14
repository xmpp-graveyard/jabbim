# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/xmlConsole.ui'
#
# Created: Wed Nov 14 06:54:03 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_xmlConsole(object):
    def setupUi(self, xmlConsole):
        xmlConsole.setObjectName("xmlConsole")
        xmlConsole.resize(QtCore.QSize(QtCore.QRect(0,0,497,569).size()).expandedTo(xmlConsole.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(xmlConsole)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.xml = QtGui.QTextBrowser(self.centralwidget)
        self.xml.setObjectName("xml")
        self.gridlayout.addWidget(self.xml,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.enable = QtGui.QCheckBox(self.centralwidget)
        self.enable.setChecked(False)
        self.enable.setObjectName("enable")
        self.hboxlayout.addWidget(self.enable)

        self.clear = QtGui.QPushButton(self.centralwidget)
        self.clear.setObjectName("clear")
        self.hboxlayout.addWidget(self.clear)

        spacerItem = QtGui.QSpacerItem(81,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.presence = QtGui.QPushButton(self.centralwidget)
        self.presence.setObjectName("presence")
        self.hboxlayout1.addWidget(self.presence)

        self.iq = QtGui.QPushButton(self.centralwidget)
        self.iq.setObjectName("iq")
        self.hboxlayout1.addWidget(self.iq)

        self.message = QtGui.QPushButton(self.centralwidget)
        self.message.setObjectName("message")
        self.hboxlayout1.addWidget(self.message)
        self.hboxlayout.addLayout(self.hboxlayout1)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)

        self.textEdit = QtGui.QTextEdit(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215,100))
        self.textEdit.setObjectName("textEdit")
        self.gridlayout.addWidget(self.textEdit,2,0,1,1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        spacerItem1 = QtGui.QSpacerItem(441,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)

        self.send = QtGui.QPushButton(self.centralwidget)
        self.send.setObjectName("send")
        self.hboxlayout2.addWidget(self.send)
        self.gridlayout.addLayout(self.hboxlayout2,3,0,1,1)
        xmlConsole.setCentralWidget(self.centralwidget)

        self.retranslateUi(xmlConsole)
        QtCore.QObject.connect(self.clear,QtCore.SIGNAL("clicked()"),self.xml.clear)
        QtCore.QMetaObject.connectSlotsByName(xmlConsole)

    def retranslateUi(self, xmlConsole):
        xmlConsole.setWindowTitle(QtGui.QApplication.translate("xmlConsole", "XML Console", None, QtGui.QApplication.UnicodeUTF8))
        self.enable.setText(QtGui.QApplication.translate("xmlConsole", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.clear.setText(QtGui.QApplication.translate("xmlConsole", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.presence.setText(QtGui.QApplication.translate("xmlConsole", "presence", None, QtGui.QApplication.UnicodeUTF8))
        self.iq.setText(QtGui.QApplication.translate("xmlConsole", "iq", None, QtGui.QApplication.UnicodeUTF8))
        self.message.setText(QtGui.QApplication.translate("xmlConsole", "message", None, QtGui.QApplication.UnicodeUTF8))
        self.send.setText(QtGui.QApplication.translate("xmlConsole", "&Send", None, QtGui.QApplication.UnicodeUTF8))

