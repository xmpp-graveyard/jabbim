# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugins/jdm/jdm_ui.ui'
#
# Created: Sat May 24 13:15:04 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,742,405).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.list = QtGui.QListWidget(self.centralwidget)
        self.list.setMinimumSize(QtCore.QSize(480,0))
        self.list.setAcceptDrops(True)
        self.list.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        self.list.setIconSize(QtCore.QSize(32,32))
        self.list.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.list.setMovement(QtGui.QListView.Free)
        self.list.setLayoutMode(QtGui.QListView.Batched)
        self.list.setGridSize(QtCore.QSize(128,96))
        self.list.setViewMode(QtGui.QListView.IconMode)
        self.list.setWordWrap(True)
        self.list.setObjectName("list")
        self.gridlayout.addWidget(self.list,1,0,3,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(3)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label_description = QtGui.QLabel(self.centralwidget)
        self.label_description.setObjectName("label_description")
        self.hboxlayout.addWidget(self.label_description)

        self.line_jid = QtGui.QLineEdit(self.centralwidget)
        self.line_jid.setMinimumSize(QtCore.QSize(0,0))
        self.line_jid.setObjectName("line_jid")
        self.hboxlayout.addWidget(self.line_jid)

        self.showMiniRoster = QtGui.QPushButton(self.centralwidget)
        self.showMiniRoster.setMaximumSize(QtCore.QSize(30,16777215))
        self.showMiniRoster.setIcon(QtGui.QIcon("view-refresh.png"))
        self.showMiniRoster.setObjectName("showMiniRoster")
        self.hboxlayout.addWidget(self.showMiniRoster)

        self.buttonHome = QtGui.QPushButton(self.centralwidget)
        self.buttonHome.setMaximumSize(QtCore.QSize(30,16777215))
        self.buttonHome.setIcon(QtGui.QIcon("home.png"))
        self.buttonHome.setObjectName("buttonHome")
        self.hboxlayout.addWidget(self.buttonHome)

        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.hboxlayout.addWidget(self.line)

        self.publicButton = QtGui.QPushButton(self.centralwidget)
        self.publicButton.setMaximumSize(QtCore.QSize(30,16777215))
        self.publicButton.setIcon(QtGui.QIcon("jdisk-public-24.png"))
        self.publicButton.setObjectName("publicButton")
        self.hboxlayout.addWidget(self.publicButton)

        self.privateButton = QtGui.QPushButton(self.centralwidget)
        self.privateButton.setMaximumSize(QtCore.QSize(30,16777215))
        self.privateButton.setIcon(QtGui.QIcon("jdisk-private-24.png"))
        self.privateButton.setObjectName("privateButton")
        self.hboxlayout.addWidget(self.privateButton)

        self.albumButton = QtGui.QPushButton(self.centralwidget)
        self.albumButton.setMaximumSize(QtCore.QSize(30,16777215))
        self.albumButton.setIcon(QtGui.QIcon("jalbum-32.png"))
        self.albumButton.setObjectName("albumButton")
        self.hboxlayout.addWidget(self.albumButton)

        self.line_3 = QtGui.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.hboxlayout.addWidget(self.line_3)

        self.reload = QtGui.QPushButton(self.centralwidget)
        self.reload.setMinimumSize(QtCore.QSize(123,0))
        self.reload.setObjectName("reload")
        self.hboxlayout.addWidget(self.reload)
        self.gridlayout.addLayout(self.hboxlayout,0,0,1,2)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_3 = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)

        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.vboxlayout.addWidget(self.line_2)

        self.label_4 = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)

        self.label_name = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_name.sizePolicy().hasHeightForWidth())
        self.label_name.setSizePolicy(sizePolicy)
        self.label_name.setMinimumSize(QtCore.QSize(120,0))
        self.label_name.setObjectName("label_name")
        self.vboxlayout.addWidget(self.label_name)

        self.label_6 = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.vboxlayout.addWidget(self.label_6)

        self.label_size = QtGui.QLabel(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_size.sizePolicy().hasHeightForWidth())
        self.label_size.setSizePolicy(sizePolicy)
        self.label_size.setMinimumSize(QtCore.QSize(120,0))
        self.label_size.setObjectName("label_size")
        self.vboxlayout.addWidget(self.label_size)
        self.gridlayout.addLayout(self.vboxlayout,1,1,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(0)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.buttonUpload = QtGui.QToolButton(self.centralwidget)
        self.buttonUpload.setIcon(QtGui.QIcon("upload.png"))
        self.buttonUpload.setIconSize(QtCore.QSize(32,32))
        self.buttonUpload.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.buttonUpload.setAutoRaise(True)
        self.buttonUpload.setObjectName("buttonUpload")
        self.hboxlayout1.addWidget(self.buttonUpload)

        self.buttonDownload = QtGui.QToolButton(self.centralwidget)
        self.buttonDownload.setIcon(QtGui.QIcon("document-save.png"))
        self.buttonDownload.setIconSize(QtCore.QSize(32,32))
        self.buttonDownload.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.buttonDownload.setAutoRaise(True)
        self.buttonDownload.setObjectName("buttonDownload")
        self.hboxlayout1.addWidget(self.buttonDownload)

        self.buttonDelete = QtGui.QToolButton(self.centralwidget)
        self.buttonDelete.setIcon(QtGui.QIcon("edit-delete.png"))
        self.buttonDelete.setIconSize(QtCore.QSize(32,32))
        self.buttonDelete.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.buttonDelete.setAutoRaise(True)
        self.buttonDelete.setObjectName("buttonDelete")
        self.hboxlayout1.addWidget(self.buttonDelete)
        self.gridlayout.addLayout(self.hboxlayout1,2,1,1,1)

        spacerItem = QtGui.QSpacerItem(20,161,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem,3,1,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(MainWindow.translate("MainWindow", "Jabber Disk Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.label_description.setText(MainWindow.translate("MainWindow", "Enter JID of disk owner:", None, QtGui.QApplication.UnicodeUTF8))
        self.reload.setText(MainWindow.translate("MainWindow", "Reload", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(MainWindow.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">File info:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(MainWindow.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">File name:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(MainWindow.translate("MainWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">File size:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonUpload.setText(MainWindow.translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDownload.setText(MainWindow.translate("MainWindow", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDelete.setText(MainWindow.translate("MainWindow", "Delete", None, QtGui.QApplication.UnicodeUTF8))

