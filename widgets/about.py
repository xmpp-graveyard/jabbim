# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgets/about.ui'
#
# Created: Sat Jul 28 12:08:28 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_about_window(object):
    def setupUi(self, about_window):
        about_window.setObjectName("about_window")
        about_window.resize(QtCore.QSize(QtCore.QRect(0,0,261,679).size()).expandedTo(about_window.minimumSizeHint()))
        about_window.setWindowIcon(QtGui.QIcon("images/16x16/apps/jabbim.png"))

        self.gridlayout = QtGui.QGridLayout(about_window)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        spacerItem = QtGui.QSpacerItem(243,186,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,14,0,1,1)

        self.label_jabbimLogo = QtGui.QLabel(about_window)
        self.label_jabbimLogo.setPixmap(QtGui.QPixmap("../../test/jabbim-ng/images/logo.png"))
        self.label_jabbimLogo.setObjectName("label_jabbimLogo")
        self.gridlayout.addWidget(self.label_jabbimLogo,0,0,1,1)

        self.label = QtGui.QLabel(about_window)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,1,0,1,1)

        self.label_7 = QtGui.QLabel(about_window)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridlayout.addWidget(self.label_7,2,0,1,1)

        self.label_2 = QtGui.QLabel(about_window)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,3,0,1,1)

        self.label_8 = QtGui.QLabel(about_window)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.gridlayout.addWidget(self.label_8,4,0,1,1)

        self.label_3 = QtGui.QLabel(about_window)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,5,0,1,1)

        self.label_4 = QtGui.QLabel(about_window)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,6,0,1,1)

        self.label_5 = QtGui.QLabel(about_window)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,7,0,1,1)

        self.label_6 = QtGui.QLabel(about_window)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,8,0,1,1)

        self.label_9 = QtGui.QLabel(about_window)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridlayout.addWidget(self.label_9,9,0,1,1)

        self.label_11 = QtGui.QLabel(about_window)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.gridlayout.addWidget(self.label_11,10,0,1,1)

        self.label_12 = QtGui.QLabel(about_window)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.gridlayout.addWidget(self.label_12,11,0,1,1)

        self.label_10 = QtGui.QLabel(about_window)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.gridlayout.addWidget(self.label_10,12,0,1,1)

        self.label_13 = QtGui.QLabel(about_window)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.gridlayout.addWidget(self.label_13,13,0,1,1)

        self.pushButton = QtGui.QPushButton(about_window)
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(True)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.gridlayout.addWidget(self.pushButton,15,0,1,1)

        self.retranslateUi(about_window)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),about_window.accept)
        QtCore.QMetaObject.connectSlotsByName(about_window)

    def retranslateUi(self, about_window):
        about_window.setWindowTitle(QtGui.QApplication.translate("about_window", "About Jabbim", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Version:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("about_window", "SVN version", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">License:</span> </p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("about_window", "GNU GPL version 2\n"
        "", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Main developers:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("about_window", "Jan \'HanzZ\' Kaluža\n"
        "Jiří \'Sef\' Gabryš", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Other developers:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("about_window", "Josef \'Cornelius\' Vybíral\n"
        "Josef \'Pepeq\' Halíček\n"
        "Peter \'Chio\' Habčák\n"
	"Jáchym \'kamahl\' Barvínek", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Where you find us:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("about_window", "Conference: jabbim@conf.netlab.cz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("about_window", "Web <a href=\"http://dev.jabbim.cz/jabbim\">http://dev.jabbim.cz/jabbim</a>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("about_window", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Thanks to:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("about_window", "We thank all testers and bug reporters!", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("about_window", "OK", None, QtGui.QApplication.UnicodeUTF8))

