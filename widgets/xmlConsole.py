# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xmlConsole.ui'
#
# Created: Sun Oct 28 14:17:40 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_xmlConsole(object):
    def setupUi(self, xmlConsole):
        xmlConsole.setObjectName("xmlConsole")
        xmlConsole.resize(QtCore.QSize(QtCore.QRect(0,0,562,477).size()).expandedTo(xmlConsole.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(xmlConsole)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.xml = QtGui.QTextBrowser(self.centralwidget)
        self.xml.setObjectName("xml")
        self.gridlayout.addWidget(self.xml,0,0,1,1)

        self.enable = QtGui.QCheckBox(self.centralwidget)
        self.enable.setChecked(False)
        self.enable.setObjectName("enable")
        self.gridlayout.addWidget(self.enable,1,0,1,1)
        xmlConsole.setCentralWidget(self.centralwidget)

        self.retranslateUi(xmlConsole)
        QtCore.QMetaObject.connectSlotsByName(xmlConsole)

    def retranslateUi(self, xmlConsole):
        xmlConsole.setWindowTitle(QtGui.QApplication.translate("xmlConsole", "XML Console", None, QtGui.QApplication.UnicodeUTF8))
        self.enable.setText(QtGui.QApplication.translate("xmlConsole", "Enable console", None, QtGui.QApplication.UnicodeUTF8))

