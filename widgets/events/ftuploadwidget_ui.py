# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ftuploadwidget.ui'
#
# Created: Mon Aug 11 07:47:49 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FTUploadWidget(object):
    def setupUi(self, FTUploadWidget):
        FTUploadWidget.setObjectName("FTUploadWidget")
        FTUploadWidget.resize(274, 146)
        self.gridLayout = QtGui.QGridLayout(FTUploadWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName("gridLayout")
        self.transferInfo = QtGui.QLabel(FTUploadWidget)
        self.transferInfo.setObjectName("transferInfo")
        self.gridLayout.addWidget(self.transferInfo, 2, 0, 1, 3)
        self.progressBar = QtGui.QProgressBar(FTUploadWidget)
        self.progressBar.setProperty("value", QtCore.QVariant(0))
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 3, 0, 1, 3)
        self.reject = QtGui.QPushButton(FTUploadWidget)
        self.reject.setObjectName("reject")
        self.gridLayout.addWidget(self.reject, 4, 1, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.filename = QtGui.QLabel(FTUploadWidget)
        self.filename.setObjectName("filename")
        self.gridLayout.addWidget(self.filename, 0, 0, 1, 2)
        self.toolButton = QtGui.QToolButton(FTUploadWidget)
        self.toolButton.setCheckable(True)
        self.toolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 2, 1, 1)
        self.more = QtGui.QLabel(FTUploadWidget)
        self.more.setTextFormat(QtCore.Qt.RichText)
        self.more.setObjectName("more")
        self.gridLayout.addWidget(self.more, 1, 0, 1, 3)

        self.retranslateUi(FTUploadWidget)
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL("clicked(bool)"), self.more.setShown)
        QtCore.QMetaObject.connectSlotsByName(FTUploadWidget)

    def retranslateUi(self, FTUploadWidget):
        FTUploadWidget.setWindowTitle(QtGui.QApplication.translate("FTUploadWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.transferInfo.setText(QtGui.QApplication.translate("FTUploadWidget", "Zbyva: 30 s (255 kB/s)", None, QtGui.QApplication.UnicodeUTF8))
        self.reject.setText(QtGui.QApplication.translate("FTUploadWidget", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.filename.setText(QtGui.QApplication.translate("FTUploadWidget", "Smileys_test.zip", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("FTUploadWidget", "More", None, QtGui.QApplication.UnicodeUTF8))
        self.more.setText(QtGui.QApplication.translate("FTUploadWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">File.txt</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">test.zip</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\">music.zip</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

