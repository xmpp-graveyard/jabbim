# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jdm.ui'
#
# Created: Fri Sep 28 10:18:13 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,624,569).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setMinimumSize(QtCore.QSize(624,569))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.listWidget_content = QtGui.QListWidget(self.centralwidget)
        self.listWidget_content.setAlternatingRowColors(False)
        self.listWidget_content.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidget_content.setMovement(QtGui.QListView.Static)
        self.listWidget_content.setWrapping(True)
        self.listWidget_content.setLayoutMode(QtGui.QListView.SinglePass)
        self.listWidget_content.setSpacing(10)
        self.listWidget_content.setViewMode(QtGui.QListView.IconMode)
        self.listWidget_content.setUniformItemSizes(True)
        self.listWidget_content.setObjectName("listWidget_content")
        self.gridlayout.addWidget(self.listWidget_content,1,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_url = QtGui.QLabel(self.centralwidget)
        self.label_url.setObjectName("label_url")
        self.hboxlayout.addWidget(self.label_url)

        self.lineEdit_urlValue = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_urlValue.setObjectName("lineEdit_urlValue")
        self.hboxlayout.addWidget(self.lineEdit_urlValue)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,1)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_fileDescription = QtGui.QLabel(self.centralwidget)
        self.label_fileDescription.setObjectName("label_fileDescription")
        self.vboxlayout.addWidget(self.label_fileDescription)

        self.label_name = QtGui.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.vboxlayout.addWidget(self.label_name)

        self.label_nameText = QtGui.QLabel(self.centralwidget)
        self.label_nameText.setObjectName("label_nameText")
        self.vboxlayout.addWidget(self.label_nameText)

        self.label_size = QtGui.QLabel(self.centralwidget)
        self.label_size.setObjectName("label_size")
        self.vboxlayout.addWidget(self.label_size)

        self.label_sizeText = QtGui.QLabel(self.centralwidget)
        self.label_sizeText.setObjectName("label_sizeText")
        self.vboxlayout.addWidget(self.label_sizeText)

        self.label_description = QtGui.QLabel(self.centralwidget)
        self.label_description.setObjectName("label_description")
        self.vboxlayout.addWidget(self.label_description)

        self.label_descriptionText = QtGui.QLabel(self.centralwidget)
        self.label_descriptionText.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_descriptionText.setWordWrap(True)
        self.label_descriptionText.setObjectName("label_descriptionText")
        self.vboxlayout.addWidget(self.label_descriptionText)

        self.label_preview = QtGui.QLabel(self.centralwidget)
        self.label_preview.setObjectName("label_preview")
        self.vboxlayout.addWidget(self.label_preview)

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(120,120))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.gridlayout1 = QtGui.QGridLayout(self.frame)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.label_foto = QtGui.QLabel(self.frame)
        self.label_foto.setPixmap(QtGui.QPixmap("phpThumb.jpeg"))
        self.label_foto.setAlignment(QtCore.Qt.AlignCenter)
        self.label_foto.setObjectName("label_foto")
        self.gridlayout1.addWidget(self.label_foto,0,0,1,1)
        self.vboxlayout.addWidget(self.frame)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.gridlayout.addLayout(self.vboxlayout,0,1,2,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setIconSize(QtCore.QSize(32,32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(self.toolBar)

        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.toolBar_2 = QtGui.QToolBar(MainWindow)
        self.toolBar_2.setMovable(False)
        self.toolBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar_2.setIconSize(QtCore.QSize(32,32))
        self.toolBar_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolBar_2.setObjectName("toolBar_2")
        MainWindow.addToolBar(self.toolBar_2)

        self.actionUpdate_views = QtGui.QAction(MainWindow)
        self.actionUpdate_views.setIcon(QtGui.QIcon("icons/view-refresh.png"))
        self.actionUpdate_views.setObjectName("actionUpdate_views")

        self.actionUpload_file = QtGui.QAction(MainWindow)
        self.actionUpload_file.setIcon(QtGui.QIcon("icons/upload.png"))
        self.actionUpload_file.setObjectName("actionUpload_file")

        self.actionDownload_file = QtGui.QAction(MainWindow)
        self.actionDownload_file.setIcon(QtGui.QIcon("icons/document-save.png"))
        self.actionDownload_file.setObjectName("actionDownload_file")

        self.actionDelete_file = QtGui.QAction(MainWindow)
        self.actionDelete_file.setIcon(QtGui.QIcon("icons/edit-delete.png"))
        self.actionDelete_file.setObjectName("actionDelete_file")

        self.actionQuit_manager = QtGui.QAction(MainWindow)
        self.actionQuit_manager.setIcon(QtGui.QIcon("icons/window-close.png"))
        self.actionQuit_manager.setObjectName("actionQuit_manager")

        self.actionPublic = QtGui.QAction(MainWindow)
        self.actionPublic.setIcon(QtGui.QIcon("icons/jdisk-public.png"))
        self.actionPublic.setObjectName("actionPublic")

        self.actionJabbim_album = QtGui.QAction(MainWindow)
        self.actionJabbim_album.setIcon(QtGui.QIcon("icons/jalbum-32.png"))
        self.actionJabbim_album.setObjectName("actionJabbim_album")

        self.actionPrivate = QtGui.QAction(MainWindow)
        self.actionPrivate.setIcon(QtGui.QIcon("icons/jdisk-private.png"))
        self.actionPrivate.setObjectName("actionPrivate")

        self.actionBrowser = QtGui.QAction(MainWindow)
        self.actionBrowser.setIcon(QtGui.QIcon("icons/browser.png"))
        self.actionBrowser.setObjectName("actionBrowser")
        self.toolBar.addAction(self.actionUpdate_views)
        self.toolBar.addAction(self.actionUpload_file)
        self.toolBar.addAction(self.actionDownload_file)
        self.toolBar.addAction(self.actionDelete_file)
        self.toolBar.addAction(self.actionQuit_manager)
        self.toolBar_2.addAction(self.actionPublic)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.actionPrivate)
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.actionJabbim_album)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.listWidget_content.clear()

        item = QtGui.QListWidgetItem(self.listWidget_content)
        item.setText(QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(QtGui.QIcon("icons/upload.png"))

        item1 = QtGui.QListWidgetItem(self.listWidget_content)
        item1.setText(QtGui.QApplication.translate("MainWindow", "New Item", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(QtGui.QIcon("icons/upload.png"))
        self.label_url.setText(QtGui.QApplication.translate("MainWindow", "URL:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_fileDescription.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">File description</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Name:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_nameText.setText(QtGui.QApplication.translate("MainWindow", "Adina_46.jpg", None, QtGui.QApplication.UnicodeUTF8))
        self.label_size.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Size:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_sizeText.setText(QtGui.QApplication.translate("MainWindow", "1,5 MB", None, QtGui.QApplication.UnicodeUTF8))
        self.label_description.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Description:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_descriptionText.setText(QtGui.QApplication.translate("MainWindow", "Some simple example of file description.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_preview.setText(QtGui.QApplication.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Preview:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpdate_views.setText(QtGui.QApplication.translate("MainWindow", "Update views", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpload_file.setText(QtGui.QApplication.translate("MainWindow", "Upload file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDownload_file.setText(QtGui.QApplication.translate("MainWindow", "download file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_file.setText(QtGui.QApplication.translate("MainWindow", "Delete file", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit_manager.setText(QtGui.QApplication.translate("MainWindow", "Quit manager", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPublic.setText(QtGui.QApplication.translate("MainWindow", "Public", None, QtGui.QApplication.UnicodeUTF8))
        self.actionJabbim_album.setText(QtGui.QApplication.translate("MainWindow", "Jabbim album", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrivate.setText(QtGui.QApplication.translate("MainWindow", "Private", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBrowser.setText(QtGui.QApplication.translate("MainWindow", "View other disks", None, QtGui.QApplication.UnicodeUTF8))

