# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/extra.ui'
#
# Created: Sat Jan 26 14:12:21 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Extra(object):
    def setupUi(self, Extra):
        Extra.setObjectName("Extra")
        Extra.resize(QtCore.QSize(QtCore.QRect(0,0,497,300).size()).expandedTo(Extra.minimumSizeHint()))
        Extra.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.gridlayout = QtGui.QGridLayout(Extra)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.preview = QtGui.QLabel(Extra)
        self.preview.setObjectName("preview")
        self.gridlayout.addWidget(self.preview,2,1,1,3)

        self.textBrowser = QtGui.QTextBrowser(Extra)
        self.textBrowser.setObjectName("textBrowser")
        self.gridlayout.addWidget(self.textBrowser,1,1,1,3)

        self.label = QtGui.QLabel(Extra)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.pushButton = QtGui.QPushButton(Extra)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,3,2,1,1)

        self.pushButton_2 = QtGui.QPushButton(Extra)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,3,3,1,1)

        self.listWidget = QtGui.QListWidget(Extra)
        self.listWidget.setMaximumSize(QtCore.QSize(165,16777215))
        self.listWidget.setObjectName("listWidget")
        self.gridlayout.addWidget(self.listWidget,1,0,2,1)

        spacerItem = QtGui.QSpacerItem(241,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,3,0,1,2)

        self.retranslateUi(Extra)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),Extra.accept)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),Extra.reject)
        QtCore.QMetaObject.connectSlotsByName(Extra)

    def retranslateUi(self, Extra):
        Extra.setWindowTitle(QtGui.QApplication.translate("Extra", "Jabbim Extra", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Extra", "<h2>Emoticons</h2>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Extra", "Install", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Extra", "Close", None, QtGui.QApplication.UnicodeUTF8))

