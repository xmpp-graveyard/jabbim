# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/hanzz/news.ui'
#
# Created: Wed Dec 24 10:47:39 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(566, 497)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(9, 9, 1008, 602))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.treeWidget = QtGui.QTreeWidget(self.widget)
        self.treeWidget.setMinimumSize(QtCore.QSize(150, 0))
        self.treeWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeWidget.setObjectName("treeWidget")
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.webView = QtWebKit.QWebView(self.widget)
        self.webView.setUrl(QtCore.QUrl("about:blank"))
        self.webView.setObjectName("webView")
        self.horizontalLayout_2.addWidget(self.webView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(MainWindow.translate("MainWindow", "News", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget.headerItem().setText(0, MainWindow.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
