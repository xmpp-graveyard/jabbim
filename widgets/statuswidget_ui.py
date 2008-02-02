# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/statuswidget.ui'
#
# Created: Sun Dec 23 18:06:45 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_statusWidgetWindow(object):
    def setupUi(self, statusWidgetWindow):
        statusWidgetWindow.setObjectName("statusWidgetWindow")
        statusWidgetWindow.resize(QtCore.QSize(QtCore.QRect(0,0,299,187).size()).expandedTo(statusWidgetWindow.minimumSizeHint()))
        statusWidgetWindow.setWindowIcon(QtGui.QIcon("images/16x16/jgames.png"))

        self.gridlayout = QtGui.QGridLayout(statusWidgetWindow)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.show = QtGui.QComboBox(statusWidgetWindow)
        self.show.setObjectName("show")
        self.gridlayout.addWidget(self.show,0,0,1,3)

        self.status = QtGui.QTextBrowser(statusWidgetWindow)
        self.status.setTabChangesFocus(True)
        self.status.setReadOnly(False)
        self.status.setObjectName("status")
        self.gridlayout.addWidget(self.status,1,0,1,3)

        self.pushButton = QtGui.QPushButton(statusWidgetWindow)
        self.pushButton.setIcon(QtGui.QIcon("images/16x16/actions/process-stop.png"))
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,2,0,1,1)

        spacerItem = QtGui.QSpacerItem(91,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,2,1,1,1)

        self.set = QtGui.QPushButton(statusWidgetWindow)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(1),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set.sizePolicy().hasHeightForWidth())
        self.set.setSizePolicy(sizePolicy)
        self.set.setIcon(QtGui.QIcon("images/16x16/actions/ok.png"))
        self.set.setObjectName("set")
        self.gridlayout.addWidget(self.set,2,2,1,1)

        self.retranslateUi(statusWidgetWindow)
        QtCore.QObject.connect(self.set,QtCore.SIGNAL("clicked()"),statusWidgetWindow.accept)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),statusWidgetWindow.reject)
        QtCore.QMetaObject.connectSlotsByName(statusWidgetWindow)

    def retranslateUi(self, statusWidgetWindow):
        statusWidgetWindow.setWindowTitle(QtGui.QApplication.translate("statusWidgetWindow", "Set status message", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setToolTip(QtGui.QApplication.translate("statusWidgetWindow", "Enter a short message describing your status (e.g. at lunch)", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("statusWidgetWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.set.setText(QtGui.QApplication.translate("statusWidgetWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))

