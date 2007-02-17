try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from joingroupchat_ui import *

class joinGroupChatWindow(QtGui.QDialog):
	def __init__(self,main,jab,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_joingroupchat()
		self.ui.setupUi(self)
		self.main=main
		self.jab=jab

	def accept(self):
		room=unicode(self.ui.room.text())
		nickname=unicode(self.ui.nickname.text())
		if self.ui.bookmark.isChecked() and not self.main.bookmarks.has_key(room):
			self.main.bookmarks[room]=nickname
			self.main.bookmarks.write()
		print "joining",room,nickname
		self.jab.getIntoRoom(room,nickname)
		self.main.chat.addGroupChatTab(room,nickname)
		self.main.groupchat[room]=[]
		self.done(1)

	def reject(self):
		self.close()