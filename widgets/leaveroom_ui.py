# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/leaveroom.ui'
#
# Created: Sat Dec  1 12:38:53 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_leaveroom(object):
    def setupUi(self, leaveroom):
        leaveroom.setObjectName("leaveroom")
        leaveroom.resize(QtCore.QSize(QtCore.QRect(0,0,323,128).size()).expandedTo(leaveroom.minimumSizeHint()))
        leaveroom.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.gridlayout = QtGui.QGridLayout(leaveroom)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.checkBox = QtGui.QCheckBox(leaveroom)
        self.checkBox.setObjectName("checkBox")
        self.gridlayout.addWidget(self.checkBox,1,1,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        spacerItem = QtGui.QSpacerItem(16,27,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)

        self.pushButton = QtGui.QPushButton(leaveroom)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)

        self.pushButton_2 = QtGui.QPushButton(leaveroom)
        self.pushButton_2.setObjectName("pushButton_2")
        self.hboxlayout.addWidget(self.pushButton_2)
        self.gridlayout.addLayout(self.hboxlayout,2,0,1,2)

        self.leaveroom = QtGui.QLabel(leaveroom)
        self.leaveroom.setTextFormat(QtCore.Qt.RichText)
        self.leaveroom.setWordWrap(True)
        self.leaveroom.setObjectName("leaveroom")
        self.gridlayout.addWidget(self.leaveroom,0,1,1,1)

        self.label_2 = QtGui.QLabel(leaveroom)
        self.label_2.setMaximumSize(QtCore.QSize(48,48))
        self.label_2.setPixmap(QtGui.QPixmap("images/48x48/categories/conferences.png"))
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,0,0,1,1)

        self.retranslateUi(leaveroom)
        QtCore.QObject.connect(self.pushButton_2,QtCore.SIGNAL("clicked()"),leaveroom.reject)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),leaveroom.accept)
        QtCore.QObject.connect(self.checkBox,QtCore.SIGNAL("toggled(bool)"),self.pushButton_2.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(leaveroom)

    def retranslateUi(self, leaveroom):
        leaveroom.setWindowTitle(QtGui.QApplication.translate("leaveroom", "Leave room", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("leaveroom", "Don\'t ask later", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("leaveroom", "Yes", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("leaveroom", "No", None, QtGui.QApplication.UnicodeUTF8))
        self.leaveroom.setText(QtGui.QApplication.translate("leaveroom", "You are trying to leave room jabbim@conf.netlab.cz\n"
        "Do you realy want to leave this room?", None, QtGui.QApplication.UnicodeUTF8))

