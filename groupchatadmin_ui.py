# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupchatadmin.ui'
#
# Created: Sun Mar  4 18:36:55 2007
#      by: PyQt4 UI code generator 4.1.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_groupchatadmin(object):
    def setupUi(self, groupchatadmin):
        groupchatadmin.setObjectName("groupchatadmin")
        groupchatadmin.resize(QtCore.QSize(QtCore.QRect(0,0,449,300).size()).expandedTo(groupchatadmin.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(groupchatadmin)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(groupchatadmin)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.banlist = QtGui.QListWidget(self.tab)
        self.banlist.setObjectName("banlist")
        self.gridlayout1.addWidget(self.banlist,0,0,1,3)

        self.deleteban = QtGui.QPushButton(self.tab)
        self.deleteban.setObjectName("deleteban")
        self.gridlayout1.addWidget(self.deleteban,1,2,1,1)

        self.addban = QtGui.QPushButton(self.tab)
        self.addban.setObjectName("addban")
        self.gridlayout1.addWidget(self.addban,1,1,1,1)

        spacerItem = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout1.addItem(spacerItem,1,0,1,1)
        self.tabWidget.addTab(self.tab,"")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")

        self.gridlayout2 = QtGui.QGridLayout(self.tab_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.deletemember = QtGui.QPushButton(self.tab_2)
        self.deletemember.setObjectName("deletemember")
        self.gridlayout2.addWidget(self.deletemember,1,2,1,1)

        self.memberlist = QtGui.QListWidget(self.tab_2)
        self.memberlist.setObjectName("memberlist")
        self.gridlayout2.addWidget(self.memberlist,0,0,1,3)

        self.addmember = QtGui.QPushButton(self.tab_2)
        self.addmember.setObjectName("addmember")
        self.gridlayout2.addWidget(self.addmember,1,1,1,1)

        spacerItem1 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem1,1,0,1,1)
        self.tabWidget.addTab(self.tab_2,"")

        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName("tab_4")

        self.gridlayout3 = QtGui.QGridLayout(self.tab_4)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        spacerItem2 = QtGui.QSpacerItem(91,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout3.addItem(spacerItem2,1,0,1,1)

        self.deleteowner = QtGui.QPushButton(self.tab_4)
        self.deleteowner.setObjectName("deleteowner")
        self.gridlayout3.addWidget(self.deleteowner,1,2,1,1)

        self.ownerlist = QtGui.QListWidget(self.tab_4)
        self.ownerlist.setObjectName("ownerlist")
        self.gridlayout3.addWidget(self.ownerlist,0,0,1,3)

        self.addowner = QtGui.QPushButton(self.tab_4)
        self.addowner.setObjectName("addowner")
        self.gridlayout3.addWidget(self.addowner,1,1,1,1)
        self.tabWidget.addTab(self.tab_4,"")

        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName("tab_5")

        self.gridlayout4 = QtGui.QGridLayout(self.tab_5)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.adminlist = QtGui.QListWidget(self.tab_5)
        self.adminlist.setObjectName("adminlist")
        self.gridlayout4.addWidget(self.adminlist,0,0,1,3)

        self.addadmin = QtGui.QPushButton(self.tab_5)
        self.addadmin.setObjectName("addadmin")
        self.gridlayout4.addWidget(self.addadmin,1,1,1,1)

        self.deleteadmin = QtGui.QPushButton(self.tab_5)
        self.deleteadmin.setObjectName("deleteadmin")
        self.gridlayout4.addWidget(self.deleteadmin,1,2,1,1)

        spacerItem3 = QtGui.QSpacerItem(241,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout4.addItem(spacerItem3,1,0,1,1)
        self.tabWidget.addTab(self.tab_5,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        spacerItem4 = QtGui.QSpacerItem(321,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem4,1,0,1,1)

        self.addmoderator = QtGui.QPushButton(self.tab_3)
        self.addmoderator.setObjectName("addmoderator")
        self.gridlayout5.addWidget(self.addmoderator,1,1,1,1)

        self.deletemoderator = QtGui.QPushButton(self.tab_3)
        self.deletemoderator.setObjectName("deletemoderator")
        self.gridlayout5.addWidget(self.deletemoderator,1,2,1,1)

        self.moderatorlist = QtGui.QListWidget(self.tab_3)
        self.moderatorlist.setObjectName("moderatorlist")
        self.gridlayout5.addWidget(self.moderatorlist,0,0,1,3)
        self.tabWidget.addTab(self.tab_3,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,2)

        spacerItem5 = QtGui.QSpacerItem(274,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem5,1,0,1,1)

        self.pushButton_2 = QtGui.QPushButton(groupchatadmin)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridlayout.addWidget(self.pushButton_2,1,1,1,1)

        self.retranslateUi(groupchatadmin)
        self.tabWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(groupchatadmin)

    def retranslateUi(self, groupchatadmin):
        groupchatadmin.setWindowTitle(QtGui.QApplication.translate("groupchatadmin", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteban.setText(QtGui.QApplication.translate("groupchatadmin", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.addban.setText(QtGui.QApplication.translate("groupchatadmin", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("groupchatadmin", "Ban list", None, QtGui.QApplication.UnicodeUTF8))
        self.deletemember.setText(QtGui.QApplication.translate("groupchatadmin", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.addmember.setText(QtGui.QApplication.translate("groupchatadmin", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("groupchatadmin", "Member list", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteowner.setText(QtGui.QApplication.translate("groupchatadmin", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.addowner.setText(QtGui.QApplication.translate("groupchatadmin", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QtGui.QApplication.translate("groupchatadmin", "Owner list", None, QtGui.QApplication.UnicodeUTF8))
        self.addadmin.setText(QtGui.QApplication.translate("groupchatadmin", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteadmin.setText(QtGui.QApplication.translate("groupchatadmin", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QtGui.QApplication.translate("groupchatadmin", "Admin list", None, QtGui.QApplication.UnicodeUTF8))
        self.addmoderator.setText(QtGui.QApplication.translate("groupchatadmin", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.deletemoderator.setText(QtGui.QApplication.translate("groupchatadmin", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("groupchatadmin", "Moderator list", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("groupchatadmin", "Close", None, QtGui.QApplication.UnicodeUTF8))

