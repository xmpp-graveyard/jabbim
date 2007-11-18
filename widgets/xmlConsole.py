# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/xmlConsole.ui'
#
# Created: Sun Nov 18 18:43:41 2007
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

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.xml = QtGui.QTextBrowser(self.splitter)
        self.xml.setObjectName("xml")

        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")

        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.textEdit = QtGui.QTextEdit(self.widget)
        self.textEdit.setObjectName("textEdit")
        self.gridlayout1.addWidget(self.textEdit,1,0,1,6)

        self.clear = QtGui.QPushButton(self.widget)
        self.clear.setObjectName("clear")
        self.gridlayout1.addWidget(self.clear,0,1,1,1)

        self.presence = QtGui.QPushButton(self.widget)
        self.presence.setObjectName("presence")
        self.gridlayout1.addWidget(self.presence,0,3,1,1)

        self.iq = QtGui.QPushButton(self.widget)
        self.iq.setObjectName("iq")
        self.gridlayout1.addWidget(self.iq,0,4,1,1)

        self.enable = QtGui.QCheckBox(self.widget)
        self.enable.setChecked(False)
        self.enable.setObjectName("enable")
        self.gridlayout1.addWidget(self.enable,0,0,1,1)

        spacerItem = QtGui.QSpacerItem(81,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,0,2,1,1)

        self.message = QtGui.QPushButton(self.widget)
        self.message.setObjectName("message")
        self.gridlayout1.addWidget(self.message,0,5,1,1)
        self.gridlayout.addWidget(self.splitter,0,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem1 = QtGui.QSpacerItem(441,21,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)

        self.send = QtGui.QPushButton(self.centralwidget)
        self.send.setObjectName("send")
        self.hboxlayout.addWidget(self.send)
        self.gridlayout.addLayout(self.hboxlayout,1,0,1,1)
        xmlConsole.setCentralWidget(self.centralwidget)

        self.retranslateUi(xmlConsole)
        QtCore.QObject.connect(self.clear,QtCore.SIGNAL("clicked()"),self.xml.clear)
        QtCore.QMetaObject.connectSlotsByName(xmlConsole)

    def retranslateUi(self, xmlConsole):
        xmlConsole.setWindowTitle(QtGui.QApplication.translate("xmlConsole", "XML Console", None, QtGui.QApplication.UnicodeUTF8))
        self.clear.setText(QtGui.QApplication.translate("xmlConsole", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.presence.setText(QtGui.QApplication.translate("xmlConsole", "presence", None, QtGui.QApplication.UnicodeUTF8))
        self.iq.setText(QtGui.QApplication.translate("xmlConsole", "iq", None, QtGui.QApplication.UnicodeUTF8))
        self.enable.setText(QtGui.QApplication.translate("xmlConsole", "Enable", None, QtGui.QApplication.UnicodeUTF8))
        self.message.setText(QtGui.QApplication.translate("xmlConsole", "message", None, QtGui.QApplication.UnicodeUTF8))
        self.send.setText(QtGui.QApplication.translate("xmlConsole", "&Send", None, QtGui.QApplication.UnicodeUTF8))

