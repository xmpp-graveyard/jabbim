"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from joingroupchat_ui import *
from mucbrowser import MUCBrowserDialog
import pyxl

from twisted.python import log

class joinGroupChatWindow(QtGui.QDialog):
	def __init__(self,main,room="",server="",parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_joingroupchat()
		self.ui.setupUi(self)
		self.main=main
		self.ui.bookmarkName.setEnabled(False)
		self.ui.autojoin.setEnabled(False)
		if not self.main.client.bookmarksEnabled:
			self.ui.bookmarkChat.setEnabled(False)
		
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Cancel).setText(self.tr("Cancel"))
		self.ui.buttonBox.button(QtGui.QDialogButtonBox.Ok).setText(self.tr("Join"))
		self.ui.browser=QtGui.QPushButton(self.tr("Browse chat rooms"))
		self.ui.buttonBox.addButton(self.ui.browser,QtGui.QDialogButtonBox.ActionRole)

		self.ui.nickname.setText(self.main.selfName)
		mucjid = None
		for jid in self.main.client.disco[self.main.client.jid.host][None]['items'].iterkeys():
			if self.main.client.hasIdentity(jid, 'conference', 'text') and jid.startswith('c'):
				mucjid = jid
				break
		if mucjid:
			self.ui.serverName.setText(mucjid)
		
		QtCore.QObject.connect(self.ui.roomName,QtCore.SIGNAL(" textChanged ( const QString &)"),self.ui.bookmarkName.setText)
		QtCore.QObject.connect(self.ui.browser,QtCore.SIGNAL("clicked()"),self.mucBrowser)

		self.ui.roomName.setFocus(QtCore.Qt.MouseFocusReason)

	def mucBrowser(self):
		self.d=MUCBrowserDialog(self.main,unicode(self.ui.serverName.text()),self,self)
		self.d.show()

	def accept(self):
		jid=unicode(self.ui.roomName.text())+"@"+unicode(self.ui.serverName.text())
		if not self.main.getJid(jid):
			return
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		saveRoom=self.ui.bookmarkChat.isChecked()
		autojoin=unicode(self.ui.autojoin.isChecked()).lower()
		bookmarkName=unicode(self.ui.bookmarkName.text())

		if saveRoom and not self.main.client.bookmarks['conference'].has_key(bookmarkName):
			self.main.client.bookmarks['conference'][bookmarkName]=pyxl.client.Bookmark(bookmarkName, 'conference', jid, autojoin, nickname, password)
			self.main.client.setBookmarks()
			self.main.buildBookmarks()

		if len(password)==0:
			password=None
		if self.main.chat.addGroupChatTab(jid,nickname):
			self.main.client.joinGC(jid, nickname, password)
		self.done(1)

	#def roomNameChanged(self,name):
		#old=unicode(self.ui.bookmarkName.text())
		#change=False
		#if len(old)==0:
			#change=True
		#elif len()
		