try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from joingroupchat_ui import *

class joinGroupChatWindow(QtGui.QDialog):
	def __init__(self,main,jab,room="",server="",parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		self.ui=Ui_joingroupchat()
		self.ui.setupUi(self)
		self.main=main
		self.jab=jab
		self.ui.room.setText(room)
		self.ui.server.setText(server)

	def accept(self):
		room=unicode(self.ui.room.text())
		server=unicode(self.ui.server.text())
		name=unicode(self.ui.name.text())
		nickname=unicode(self.ui.nickname.text())
		password=unicode(self.ui.password.text())
		if self.ui.bookmark.isChecked() and not self.main.bookmarks.has_key(room):
			print "setting bookmark for",room+"@"+server
			self.main.bookmarks[room+"@"+server]={"name":name,"nick":nickname,"autojoin":"0","password":password}
			self.jab.setBookmarks(self.main.bookmarks)
			#self.main.buildGroupchatMenu()
		print "joining",room,nickname
		#self.main.chat.addGroupChatTab(room+"@"+server,nickname)
		#self.main.groupchat[room+"@"+server]=[nickname,[]]
		self.jab.getIntoRoom(room+"@"+server,nickname)
		self.done(1)

	def reject(self):
		self.close()