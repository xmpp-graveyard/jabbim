# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/startchat.ui'
#
# Created: Fri Feb 22 15:56:25 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_StartChatDialog(object):
    def setupUi(self, StartChatDialog):
        StartChatDialog.setObjectName("StartChatDialog")
        StartChatDialog.resize(QtCore.QSize(QtCore.QRect(0,0,390,97).size()).expandedTo(StartChatDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(StartChatDialog)
        self.gridlayout.setObjectName("gridlayout")

        self.buttonBox = QtGui.QDialogButtonBox(StartChatDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,3,0,1,2)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(StartChatDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.comboBox = QtGui.QComboBox(StartChatDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout.addWidget(self.comboBox)
        self.gridlayout.addLayout(self.hboxlayout,0,0,2,2)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,2,0,1,1)

        self.retranslateUi(StartChatDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),StartChatDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),StartChatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StartChatDialog)

    def retranslateUi(self, StartChatDialog):
        StartChatDialog.setWindowTitle(QtGui.QApplication.translate("StartChatDialog", "Start chat", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StartChatDialog", "Jabber ID:", None, QtGui.QApplication.UnicodeUTF8))

