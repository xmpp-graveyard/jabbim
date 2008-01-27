# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/albumfiletransfer.ui'
#
# Created: Sun Jan 27 10:21:15 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_albumFiletransferDialog(object):
    def setupUi(self, albumFiletransferDialog):
        albumFiletransferDialog.setObjectName("albumFiletransferDialog")
        albumFiletransferDialog.resize(QtCore.QSize(QtCore.QRect(0,0,498,451).size()).expandedTo(albumFiletransferDialog.minimumSizeHint()))
        albumFiletransferDialog.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.gridlayout = QtGui.QGridLayout(albumFiletransferDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.gridlayout1 = QtGui.QGridLayout()
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.files = QtGui.QListWidget(albumFiletransferDialog)
        self.files.setMaximumSize(QtCore.QSize(160,16777215))
        self.files.setObjectName("files")
        self.gridlayout1.addWidget(self.files,0,0,2,1)

        self.photo = QtGui.QLabel(albumFiletransferDialog)
        self.photo.setFrameShape(QtGui.QFrame.StyledPanel)
        self.photo.setObjectName("photo")
        self.gridlayout1.addWidget(self.photo,0,1,1,1)

        self.description = QtGui.QTextEdit(albumFiletransferDialog)
        self.description.setObjectName("description")
        self.gridlayout1.addWidget(self.description,1,1,1,1)
        self.gridlayout.addLayout(self.gridlayout1,0,0,1,2)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.pushButton_2 = QtGui.QPushButton(albumFiletransferDialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout.addWidget(self.pushButton_2)

        self.pushButton = QtGui.QPushButton(albumFiletransferDialog)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)
        self.gridlayout.addLayout(self.hboxlayout,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(211,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,1,0,1,1)

        self.retranslateUi(albumFiletransferDialog)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),albumFiletransferDialog.reject)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),albumFiletransferDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(albumFiletransferDialog)

    def retranslateUi(self, albumFiletransferDialog):
        albumFiletransferDialog.setWindowTitle(QtGui.QApplication.translate("albumFiletransferDialog", "Filetransfer", None, QtGui.QApplication.UnicodeUTF8))
        self.photo.setText(QtGui.QApplication.translate("albumFiletransferDialog", "photo", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("albumFiletransferDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("albumFiletransferDialog", "Send", None, QtGui.QApplication.UnicodeUTF8))

