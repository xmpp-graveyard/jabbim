# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addcontactng.ui'
#
# Created: Tue Aug 26 09:10:13 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_addContact(object):
    def setupUi(self, addContact):
        addContact.setObjectName("addContact")
        addContact.resize(439, 385)
        self.gridLayout = QtGui.QGridLayout(addContact)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(addContact)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self._tabBar = QtGui.QWidget(addContact)
        self._tabBar.setObjectName("_tabBar")
        self.gridLayout.addWidget(self._tabBar, 1, 0, 1, 3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(addContact)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.search = QtGui.QPushButton(addContact)
        self.search.setObjectName("search")
        self.horizontalLayout.addWidget(self.search)
        self.add = QtGui.QPushButton(addContact)
        self.add.setObjectName("add")
        self.horizontalLayout.addWidget(self.add)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 3)
        self.empty = QtGui.QLabel(addContact)
        self.empty.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.empty.setObjectName("empty")
        self.gridLayout.addWidget(self.empty, 3, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(388, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 3)
        self.treeWidget = QtGui.QTreeWidget(addContact)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setObjectName("treeWidget")
        self.gridLayout.addWidget(self.treeWidget, 5, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(218, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 6, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(addContact)
        self.pushButton_2.setAutoDefault(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 6, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(addContact)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 6, 2, 1, 1)

        self.retranslateUi(addContact)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("returnPressed()"), self.search.click)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), addContact.accept)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), addContact.reject)
        QtCore.QMetaObject.connectSlotsByName(addContact)

    def retranslateUi(self, addContact):
        addContact.setWindowTitle(QtGui.QApplication.translate("addContact", "Find user", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("addContact", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><h2>Find user</h2></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.search.setText(QtGui.QApplication.translate("addContact", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.add.setText(QtGui.QApplication.translate("addContact", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.empty.setText(QtGui.QApplication.translate("addContact", "No contact matching your criteria was found", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("addContact", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("addContact", "Add to roster", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("addContact", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

