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
from chatwidget_ui import *
from configobj import ConfigObj
#from palette import *
import urllib,re,os
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes
import filetransfer
from twisted.words.protocols.jabber import jid as jidT
import time
from include import utils
from abstractchatwidget import abstractChatWidget,abstractTextView

class flowLayout(QtGui.QLayout):
	"""
	Flow layout from Qt4 examples. Used for plugins buttons.
	"""
	def __init__(self, parent=None, margin=0, spacing=-1):
		QtGui.QLayout.__init__(self, parent)

		if parent is not None:
			self.setMargin(2)
		self.setSpacing(spacing)

		self.itemList = []

	def addItem(self, item):
		self.itemList.append(item)

	def count(self):
		return len(self.itemList)

	def itemAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList[index]

	def takeAt(self, index):
		if index >= 0 and index < len(self.itemList):
			return self.itemList.pop(index)

	def expandingDirections(self):
		return QtCore.Qt.Orientations(QtCore.Qt.Orientation(0))

	def hasHeightForWidth(self):
		return True

	def heightForWidth(self, width):
		height = self.doLayout(QtCore.QRect(0, 0, width, 0), True)
		return height

	def setGeometry(self, rect):
		QtGui.QLayout.setGeometry(self, rect)
		self.doLayout(rect, False)

	def sizeHint(self):
		return self.minimumSize()

	def minimumSize(self):
		size = QtCore.QSize()

		for item in self.itemList:
			size = size.expandedTo(item.minimumSize())

		size += QtCore.QSize(2 * self.margin(), 2 * self.margin())
		return size

	def doLayout(self, rect, testOnly):
		x = rect.x()
		y = rect.y()
		lineHeight = 0

		for item in self.itemList:
			nextX = x + item.sizeHint().width() + self.spacing()
			if nextX - self.spacing() > rect.right() and lineHeight > 0:
				x = rect.x()
				y = y + lineHeight + self.spacing()
				nextX = x + item.sizeHint().width() + self.spacing()
				lineHeight = 0

			if not testOnly:
				item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

			x = nextX
			lineHeight = max(lineHeight, item.sizeHint().height())

		return y + lineHeight - rect.y()

class chatWidget(abstractChatWidget):
	def __init__(self,main,jid,parent=None):
		jidt=jidT.JID(jid)
		try:
			xhtml=main.client.roster['users'][jidt.userhost()].resources[jidt.resource].hasFeature('http://jabber.org/protocol/xhtml-im') #: True if user supports xhtml, otherwise False
		except:
			xhtml=False
		abstractChatWidget.__init__(self,Ui_chatwidget,abstractTextView,main,jid,xhtml,parent)

		# set splitters sizes
		self.ui.splitter.setSizes(list(self.main.config['chatSplitterSizes']))
		self.ui.splitter_2.setSizes(list(self.main.config['chatSplitter2Sizes']))
		widget=self.ui.splitter_2.widget(1)
		widget.setMaximumWidth(128)
		
		# Maximum width of avatar Widget
		self.ui.avatar.setMaximumWidth(128)
		self.noColor=True
		
		# get users avatar
		self.file=self.main.homeDir+'/avatars/'+unicode(jidT.JID(jid).userhost()) #: path to users avatar
		self.avatarHeight=32 #: avatars height
		if not os.path.isfile(self.file):
			# use default avatar if users avatar doesn't exist
			self.file="images/32x32/apps/jabbim.png"
		else:
			# change size of users avatar
			# TODO: size should be changed by skin...
			pixmap=QtGui.QPixmap(self.file).scaledToWidth(32)
			self.avatarHeight=int(pixmap.height())

		# get self avatar
		self.selfHeight=32 #: height of self avatar
		f=self.main.homeDir+'/avatars/'+self.main.client.jid.userhost()
		if not os.path.isfile(f):
			self.file="images/32x32/apps/jabbim.png"
		else:
			pixmap=QtGui.QPixmap(f).scaledToWidth(32)
			self.selfHeight=int(pixmap.height())

		# plugins buttons
		self.flowLayout = flowLayout()
		for key,value in self.main.plugins.iteritems():
			if value['module']:
				self.main.runPluginCommand(value['module'].buildChatWidget,[unicode(jidT.JID(self.jid).userhost()),self.flowLayout,self])
		
		# sendFile buttons
		self.ui.sendFile=QtGui.QToolButton()
		self.ui.sendFile.setIconSize(QtCore.QSize(16,16))
		self.ui.sendFile.setIcon(QtGui.QIcon("images/32x32/actions/upload.png"))
		self.ui.sendFile.setToolTip(self.tr("Send file"))
		self.flowLayout.addWidget(self.ui.sendFile)
		QtCore.QObject.connect(self.ui.sendFile, QtCore.SIGNAL("clicked ()"),self.sendFiles)

		self.ui.pluginWidget.setLayout(self.flowLayout)

		if self.main.selfAvatar:
			result=self.main.getAvatar(self.main.selfAvatar,size="64x64",frame=True)
			self.ui.selfAvatar.setPixmap(result)
			self.ui.selfAvatar.setMaximumWidth(64)
		else:
			self.ui.selfAvatar.hide()

	def sendFiles(self):
		"""
		Shows filetransfer dialog and sends files to user who chats with us.
		"""
		self.main.sendFiles(self.jid)
		#file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file")
		#file=list(file)
		#if len(file)!=0:
			#new=[]
			#for f in file:
				#new.append(unicode(f))
			#file=new
			## show filetransfer dialog and send files
			#self.dialog=filetransfer.filetransferDialog(self.main,file,self.jid)
			#self.dialog.show()
	
	def sendButtonClicked(self):
		"""
		Sends message writed in self.ui.line or call command if message starts with "/".
		"""
		if len(unicode(self.ui.line.toPlainText()))!=0:
			# execute commands if message starts with "/"
			services=unicode(self.ui.line.toPlainText())
			if services.startswith("/google"):
				anchor="http://www.google.com/search?q="+services.replace("/google ","")
				QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.line.composing=False
				return
				
			elif services.startswith("/"):
				try:
					cmd, args = services.split(" ", 1)
					args = args.split(" ")
				except ValueError:
					cmd = services
					args = []
				cmd = cmd[1:]
				# publish onCommnad event for events subscribers (mainly plugins)
				self.main.client.dispatcher.publishEvent("onCommand", cmd, args, self, "chat")
				self.ui.line.clear()
				self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
				self.ui.line.composing=False
				return
			
			# get plain text message
			text=unicode(self.ui.line.toPlainText())
			text=unescape(text)
			ret=[]
			if self.xhtml:
				# get message in Qt html format
				xhtml=self.ui.line.toHtml()
				xhtml=self.qtHtmlToXhtml(xhtml)
				# send message
				if xhtml==text:
					for key,value in self.main.plugins.iteritems():
						if value['module']:
							ret.append(self.main.runPluginCommand(value['module'].on_messageSend,[unicode(self.jid),text,'',"active"]))
					if not False in ret:
						self.main.client.sendMessage(unicode(self.jid),text,composing="active")
				else:
					for key,value in self.main.plugins.iteritems():
						if value['module']:
							ret.append(self.main.runPluginCommand(value['module'].on_messageSend,[unicode(self.jid),text,xhtml,"active"]))
					if not False in ret:
						self.main.client.sendMessage(unicode(self.jid),text,xhtml=xhtml,composing="active")
				
				# prepare message for showing in GUI
				message=xhtml.replace("&quot;",'"')
				file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
				if not os.path.isfile(file):
					file="images/32x32/apps/jabbim.png"
				message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",message).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
			else:
				# send message
				for key,value in self.main.plugins.iteritems():
					if value['module']:
						ret.append(self.main.runPluginCommand(value['module'].on_messageSend,[unicode(self.jid),text,'',"active"]))
				if not False in ret:
					self.main.client.sendMessage(unicode(self.jid),text,composing="active")
				
				# prepare message for showing in GUI
				text=unicode(text).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
				text=utils.replace_url(text)
				text=text.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
				file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
				if not os.path.isfile(file):
					file="images/32x32/apps/jabbim.png"
				if unicode(text).startswith("/me"):
					message=self.main.skin["my_me_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text[3:]).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
				else:
					message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
			# show message
			if not False in ret:
				self.textEditWrite(message)
			# add message to 'sent messages history'
			self.sent.append(text)
			self.hindex = len(self.sent)
			
			#self.ui.line.clear()
			#self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
			self.clearLine()
			self.ui.line.composing=False
			# depracted
			if self.main.chat.active==False:
				self.main.client.dispatcher.publishEvent('onActivity')
				self.main.chat.active=True