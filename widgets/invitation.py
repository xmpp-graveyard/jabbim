# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'invitation.ui'
#
# Created: Sat Oct 13 14:11:10 2007
#      by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_invitation(object):
    def setupUi(self, invitation):
        invitation.setObjectName("invitation")
        invitation.resize(QtCore.QSize(QtCore.QRect(0,0,245,171).size()).expandedTo(invitation.minimumSizeHint()))
        invitation.setWindowIcon(QtGui.QIcon("../../jabbim-ng/widgets/images/16x16/jgames.png"))

        self.gridlayout = QtGui.QGridLayout(invitation)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.acceptButton = QtGui.QPushButton(invitation)
        self.acceptButton.setObjectName("acceptButton")
        self.gridlayout.addWidget(self.acceptButton,5,2,1,3)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem,5,0,1,1)

        self.label = QtGui.QLabel(invitation)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,4,5)

        self.declineButton = QtGui.QPushButton(invitation)
        self.declineButton.setObjectName("declineButton")
        self.gridlayout.addWidget(self.declineButton,5,1,1,1)

        self.nickLabel = QtGui.QLabel(invitation)
        self.nickLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nickLabel.setObjectName("nickLabel")
        self.gridlayout.addWidget(self.nickLabel,4,0,1,1)

        self.nickname = QtGui.QLineEdit(invitation)
        self.nickname.setObjectName("nickname")
        self.gridlayout.addWidget(self.nickname,4,1,1,4)

        self.retranslateUi(invitation)
        QtCore.QObject.connect(self.acceptButton,QtCore.SIGNAL("clicked()"),invitation.accept)
        QtCore.QObject.connect(self.declineButton,QtCore.SIGNAL("clicked()"),invitation.reject)
        QtCore.QMetaObject.connectSlotsByName(invitation)

    def retranslateUi(self, invitation):
        invitation.setWindowTitle(QtGui.QApplication.translate("invitation", "MUC invitation", None, QtGui.QApplication.UnicodeUTF8))
        self.acceptButton.setText(QtGui.QApplication.translate("invitation", "Accept", None, QtGui.QApplication.UnicodeUTF8))
        self.declineButton.setText(QtGui.QApplication.translate("invitation", "Decline", None, QtGui.QApplication.UnicodeUTF8))
        self.nickLabel.setText(QtGui.QApplication.translate("invitation", "Nickname:", None, QtGui.QApplication.UnicodeUTF8))
        self.nickname.setToolTip(QtGui.QApplication.translate("invitation", "Your nickname in the room.", None, QtGui.QApplication.UnicodeUTF8))

