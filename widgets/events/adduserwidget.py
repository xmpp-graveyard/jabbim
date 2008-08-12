import os
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import weakref
from booleanwidget_ui import *
from widgets import vcardeditor

class addUserWidget(QtGui.QWidget):
	def __init__(self,event,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.event=weakref.proxy(event)
		self.ui=Ui_Form()
		self.ui.setupUi(self)
		self.ui.accept.setText(self.tr("Yes"))
		self.ui.reject.setText(self.tr("No"))
		QtCore.QObject.connect(self.ui.accept,QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(self.ui.reject,QtCore.SIGNAL("clicked()"),self.reject)
		QtCore.QObject.connect(self.ui.text,QtCore.SIGNAL("linkActivated ( const QString & )"),self.showUserMenu)
		self.jid=""

	def showUserMenu(self,link):
		menu=QtGui.QMenu(self)
		menu.addAction(self.tr("Show VCard"),self.showVCard)
		menu.addAction(self.tr("Chat"),self.openChat)
		menu.popup(QtCore.QPoint(QtGui.QCursor.pos()))

	def showVCard(self,b=False):
		self.ve=vcardeditor.vcardEditorDialog(self.event.parent.main,self.jid,self.event.parent.main,False)
		self.ve.show()

	def openChat(self,b=False):
		self.event.parent.main.chat.addChatTab(self.jid,self.jid,self.event.parent.main.getIcon(self.jid,'online',size="16x16"))
		self.event.parent.main.chat.activate()

	def setData(self,jid,message=None):
		self.jid=unicode(jid)
		text=unicode(self.tr("Do you want to add user"))
		text+=" <a href=\"http://jid\">"+self.jid+"</a> "
		text+=unicode(self.tr("to you roster?"))
		if message:
			text+="<br/><i>"+unicode(message)+"</i>"
		self.ui.text.setText(text)

	def setAcceptText(self,text):
		self.ui.accept.setText(text)

	def setRejectText(self,text):
		self.ui.reject.setText(text)

	def eventRejected(self):
		pass

	def eventAccepted(self):
		pass

	def accept(self):
		self.event.accept()

	def reject(self):
		self.event.reject()
