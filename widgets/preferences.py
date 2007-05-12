try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
import sys; sys.path.append('..')
from preferences_ui import *
from configobj import ConfigObj
import os

class preferencesWindow(QtGui.QDialog):
	def __init__(self,main,parent=None,page=0):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.setModal(False)
		self.ui=Ui_preferences()
		self.ui.setupUi(self)
		self.ui.stackedWidget.setCurrentIndex(page)
		
		# connection
		self.ui.connection_password.setText(self.main.config['passwd'])
		self.ui.connection_jid.setText(self.main.config['jid'])

		# chat skins
		skins=os.listdir("skins/")
		for skin in skins:
			if skin.endswith(".conf"):
				if skin==self.main.config["chat_skin"]:
					self.ui.chatSkin_list.insertItem(0,unicode(skin))
					self.chatSkin_listChanged(skin)
				else:
					self.ui.chatSkin_list.addItem(unicode(skin))
		self.ui.chatSkin_list.setCurrentIndex(0)
		QtCore.QObject.connect(self.ui.chatSkin_list, QtCore.SIGNAL("activated ( const QString & )"),self.chatSkin_listChanged)

		# roster
		index=self.ui.roster_iconSize.findText(self.main.config['rosterIconSize'])
		self.ui.roster_iconSize.setCurrentIndex(int(index))

	def chatSkinPreviewtextEditWrite(self,text):
		cur=self.ui.chatSkin_preview.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.chatSkin_preview.setTextCursor(cur)
		self.ui.chatSkin_preview.insertHtml(text)
		cur=self.ui.chatSkin_preview.textCursor()
		cur.movePosition(QtGui.QTextCursor.End)
		self.ui.chatSkin_preview.setTextCursor(cur)

	def chatSkin_listChanged(self,file):
		file=unicode(file)
		testConfig=ConfigObj("skins/"+file,encoding='UTF8')
		self.ui.chatSkin_preview.clear()
		self.chatSkinPreviewtextEditWrite(testConfig["message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message_for_me_history"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name send in past."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("This is test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("Me"))).replace("[message]",unicode(self.tr("This is my test message."))))
		self.chatSkinPreviewtextEditWrite(testConfig["message_for_me"].replace("[time]",self.main.now()).replace("[user]",unicode(self.tr("User"))).replace("[message]",unicode(self.tr("Me"))+", "+unicode(self.tr("this is message contains my name."))))
		self.chatSkinPreviewtextEditWrite(testConfig["status_message"].replace("[time]",self.main.now()).replace("[message]",unicode(self.tr("User has set the subject to: Subject"))))

	def accept(self):
		jid=unicode(self.ui.connection_jid.text())
		password=unicode(self.ui.connection_password.text())
		self.main.skin=ConfigObj("skins/"+unicode(self.ui.chatSkin_list.currentText()),encoding='UTF8')
		self.main.config['passwd']=password
		self.main.config['chat_skin']=unicode(self.ui.chatSkin_list.currentText())
		self.main.config['jid']=jid
		self.main.config['rosterIconSize']=unicode(self.ui.roster_iconSize.currentText())
		self.main.config.write()
		#size=unicode(self.main.config['rosterIconSize']).rsplit("x")
		#self.main.ui.roster.setIconSize(QtCore.QSize(int(size[0]),int(size[1])))
		self.done(1)
