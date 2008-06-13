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
import os

class webkitThemeFactory:
	def __init__(self,chatTheme,groupchatTheme):
		self.fullChatTheme=chatTheme
		self.fullGroupchatTheme=groupchatTheme
		self.load()

	def load(self):
		cwd=os.getcwd()
		self.chatTheme,self.chatStyle=self.fullChatTheme.split("/")
		self.groupchatTheme,self.groupchatStyle=self.fullGroupchatTheme.split("/")

		self.incomingContent=None
		if os.path.exists(cwd+"/chatskins/%s/Incoming/Content.html"%self.chatTheme):
			f=open(cwd+"/chatskins/%s/Incoming/Content.html"%self.chatTheme,"r")
			self.incomingContent=f.read()
			f.close()

		self.incomingNextContent=None
		if os.path.exists(cwd+"/chatskins/%s/Incoming/NextContent.html"%self.chatTheme):
			f=open(cwd+"/chatskins/%s/Incoming/NextContent.html"%self.chatTheme,"r")
			self.incomingNextContent=f.read()
			f.close()

		self.outgoingContent=None
		if os.path.exists(cwd+"/chatskins/%s/Outgoing/Content.html"%self.chatTheme):
			f=open(cwd+"/chatskins/%s/Outgoing/Content.html"%self.chatTheme,"r")
			self.outgoingContent=f.read()
			f.close()

		self.outgoingNextContent=None
		if os.path.exists(cwd+"/chatskins/%s/Outgoing/NextContent.html"%self.chatTheme):
			f=open(cwd+"/chatskins/%s/Outgoing/NextContent.html"%self.chatTheme,"r")
			self.outgoingNextContent=f.read()
			f.close()


		self.incomingGroupchatContent=None
		if os.path.exists(cwd+"/chatskins/%s/Incoming/Content.html"%self.groupchatTheme):
			f=open(cwd+"/chatskins/%s/Incoming/Content.html"%self.groupchatTheme,"r")
			self.incomingGroupchatContent=f.read()
			f.close()

		self.incomingGroupchatNextContent=None
		if os.path.exists(cwd+"/chatskins/%s/Incoming/NextContent.html"%self.groupchatTheme):
			f=open(cwd+"/chatskins/%s/Incoming/NextContent.html"%self.groupchatTheme,"r")
			self.incomingGroupchatNextContent=f.read()
			f.close()

		self.outgoingGroupchatContent=None
		if os.path.exists(cwd+"/chatskins/%s/Outgoing/Content.html"%self.groupchatTheme):
			f=open(cwd+"/chatskins/%s/Outgoing/Content.html"%self.groupchatTheme,"r")
			self.outgoingGroupchatContent=f.read()
			f.close()

		self.outgoingGroupchatNextContent=None
		if os.path.exists(cwd+"/chatskins/%s/Outgoing/NextContent.html"%self.groupchatTheme):
			f=open(cwd+"/chatskins/%s/Outgoing/NextContent.html"%self.groupchatTheme,"r")
			self.outgoingGroupchatNextContent=f.read()
			f.close()
		
		self.groupchatStatus=None
		if os.path.exists(cwd+"/chatskins/%s/Status.html"%self.groupchatTheme):
			f=open(cwd+"/chatskins/%s/Status.html"%self.groupchatTheme,"r")
			self.groupchatStatus=f.read()
			f.close()

		self.chatStatus=None
		if os.path.exists(cwd+"/chatskins/%s/Status.html"%self.chatTheme):
			f=open(cwd+"/chatskins/%s/Status.html"%self.chatTheme,"r")
			self.chatStatus=f.read()
			f.close()

	def chatPath(self):
		return os.getcwd()+"/chatskins/%s/" % self.chatTheme

	def groupchatPath(self):
		return os.getcwd()+"/chatskins/%s/" % self.groupchatTheme

	def genChatStatus(self,message,time):
		if not self.chatStatus:
			return ""
		return unicode(self.chatStatus).replace("%status%","online").replace("%time%",time).replace("%message%",message)

	def genGroupchatStatus(self,message,time):
		if not self.groupchatStatus:
			return ""
		return unicode(self.groupchatStatus).replace("%status%","online").replace("%time%",time).replace("%message%",message)

	def genChatStyleSheet(self):
		return '@import url( "Variants/%s" );' % self.chatStyle

	def genGroupchatStyleSheet(self):
		return '@import url( "Variants/%s" );' % self.groupchatStyle

	def genGroupchatIncomingContent(self,user,message,time,avatar=""):
		return unicode(self.incomingGroupchatContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)

	def genGroupchatIncomingNextContent(self,user,message,time,avatar=""):
		return unicode(self.incomingGroupchatNextContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)

	def genGroupchatOutgoingNextContent(self,user,message,time,avatar=""):
		return unicode(self.outgoingGroupchatNextContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)
	
	def genGroupchatOutgoingContent(self,user,message,time,avatar=""):
		return unicode(self.outgoingGroupchatContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)

	def genIncomingContent(self,user,message,time,avatar=""):
		return unicode(self.incomingContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)

	def genIncomingNextContent(self,user,message,time,avatar=""):
		return unicode(self.incomingNextContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)

	def genOutgoingNextContent(self,user,message,time,avatar=""):
		return unicode(self.outgoingNextContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)
	
	def genOutgoingContent(self,user,message,time,avatar=""):
		return unicode(self.outgoingContent).replace("%sender%",user).replace("%time%",time).replace("%message%",message).replace("%userIconPath%",avatar)
