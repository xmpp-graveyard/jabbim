# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Tue Aug 18 18:59:52 2009
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_about_window(object):
    def setupUi(self, about_window):
        about_window.setObjectName("about_window")
        about_window.resize(519, 326)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/16x16/apps/jabbim.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        about_window.setWindowIcon(icon)
        self.gridlayout = QtGui.QGridLayout(about_window)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.widget = QtGui.QWidget(about_window)
        self.widget.setObjectName("widget")
        self.gridlayout1 = QtGui.QGridLayout(self.widget)
        self.gridlayout1.setMargin(0)
        self.gridlayout1.setSpacing(0)
        self.gridlayout1.setObjectName("gridlayout1")
        self.widget_2 = QtGui.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.label_10 = QtGui.QLabel(self.widget_2)
        self.label_10.setGeometry(QtCore.QRect(340, 190, 80, 32))
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_2 = QtGui.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(90, 80, 80, 32))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label = QtGui.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(90, 0, 80, 32))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.label_6 = QtGui.QLabel(self.widget_2)
        self.label_6.setGeometry(QtCore.QRect(290, 90, 188, 105))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_8 = QtGui.QLabel(self.widget_2)
        self.label_8.setGeometry(QtCore.QRect(70, 110, 107, 30))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtGui.QLabel(self.widget_2)
        self.label_9.setGeometry(QtCore.QRect(70, 140, 129, 31))
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.mucLink = QtGui.QLabel(self.widget_2)
        self.mucLink.setGeometry(QtCore.QRect(40, 160, 194, 41))
        self.mucLink.setAlignment(QtCore.Qt.AlignCenter)
        self.mucLink.setOpenExternalLinks(False)
        self.mucLink.setObjectName("mucLink")
        self.label_12 = QtGui.QLabel(self.widget_2)
        self.label_12.setGeometry(QtCore.QRect(50, 190, 171, 16))
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setOpenExternalLinks(True)
        self.label_12.setObjectName("label_12")
        self.version = QtGui.QLabel(self.widget_2)
        self.version.setGeometry(QtCore.QRect(50, 30, 161, 61))
        self.version.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.version.setObjectName("version")
        self.label_4 = QtGui.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(300, 30, 171, 30))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(320, 60, 131, 32))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_13 = QtGui.QLabel(self.widget_2)
        self.label_13.setGeometry(QtCore.QRect(270, 220, 209, 41))
        self.label_13.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_13.setObjectName("label_13")
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(330, 0, 117, 32))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.pushButton = QtGui.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(190, 270, 101, 27))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(True)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout1.addWidget(self.widget_2, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(about_window)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), about_window.accept)
        QtCore.QMetaObject.connectSlotsByName(about_window)

    def retranslateUi(self, about_window):
        about_window.setWindowTitle(QtGui.QApplication.translate("about_window", "About Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"     p, li { white-space: pre-wrap; }\n"
"     </style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"     <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Thanks to:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"     p, li { white-space: pre-wrap; }\n"
"     </style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"     <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">License:</span> </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"     p, li { white-space: pre-wrap; }\n"
"     </style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"     <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Version:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("about_window", "Josef \'Cornelius\' Vybí­ral\n"
"Josef \'Pepeq\' Halíček\n"
"Jáchym \'Kamahl\' Barvínek\n"
"Michal \'Michich\' Schmidt\n"
"Jan \'Pinky\' Pinkas\n"
"Zenon \'Zenek\' Kuder\n"
"and many translators and patchers", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("about_window", "GNU GPL version 2\n"
"     ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"     p, li { white-space: pre-wrap; }\n"
"     </style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"     <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Where you find us:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.mucLink.setText(QtGui.QApplication.translate("about_window", "Conference: <a href=\'xmpp:jabbim@conf.netlab.cz?join\'>jabbim@conf.netlab.cz</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("about_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Web: <a href=\"http://dev.jabbim.cz/jabbim\"><span style=\" text-decoration: underline; color:#0000ff;\">http://dev.jabbim.cz/jabbim</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.version.setText(QtGui.QApplication.translate("about_window", "$VERSION", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("about_window", "Jan \'HanzZ\' Kaluža\n"
"     Jiří­ \'Sef\' Gabryš", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"     p, li { white-space: pre-wrap; }\n"
"     </style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"     <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Other developers:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("about_window", "We thank all testers and bug reporters!", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"     p, li { white-space: pre-wrap; }\n"
"     </style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
"     <p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Main developers:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("about_window", "OK", None, QtGui.QApplication.UnicodeUTF8))

