# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/miniroster.ui'
#
# Created: Thu May 22 14:10:59 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_miniRoster(object):
    def setupUi(self, miniRoster):
        miniRoster.setObjectName("miniRoster")
        miniRoster.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(miniRoster.minimumSizeHint()))
        miniRoster.setModal(True)

        self.gridlayout = QtGui.QGridLayout(miniRoster)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.buttonBox = QtGui.QDialogButtonBox(miniRoster)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,1,0,1,1)

        self.users = QtGui.QTreeWidget(miniRoster)
        self.users.setIconSize(QtCore.QSize(22,22))
        self.users.setRootIsDecorated(False)
        self.users.setAllColumnsShowFocus(True)
        self.users.setObjectName("users")
        self.gridlayout.addWidget(self.users,0,0,1,1)

        self.retranslateUi(miniRoster)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),miniRoster.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),miniRoster.reject)
        QtCore.QMetaObject.connectSlotsByName(miniRoster)

    def retranslateUi(self, miniRoster):
        miniRoster.setWindowTitle(QtGui.QApplication.translate("miniRoster", "Mini roster", None, QtGui.QApplication.UnicodeUTF8))

