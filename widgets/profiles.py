"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
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
import sys; sys.path.append('..')
import os
from profiles_ui import *
from include import utils
import shutil
try:
	from wizards import firststart
except:
	pass
class profilesWindow(QtGui.QMainWindow):
	def __init__(self,main,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.main=main
		self.ui=Ui_profilesWindow()
		self.ui.setupUi(self)
		self.loadProfiles()
		QtCore.QObject.connect(self.ui.profilesList, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.profileChanged)
		QtCore.QObject.connect(self.ui.removeProfile, QtCore.SIGNAL("clicked()"),self.removeProfile)
		QtCore.QObject.connect(self.ui.newProfile, QtCore.SIGNAL("clicked()"),self.newProfile)
		self.ui.removeProfile.setEnabled(False)


	def loadProfiles(self):
		self.ui.profilesList.clear()
		profiles=utils.getProfiles(self.main.realHomeDir)
		for profile in profiles:
			jid=profile.replace('-profile','')
	
			if os.path.isfile(self.main.realHomeDir+"/"+profile+"/avatars/"+unicode(jid)):
				avatar=QtGui.QPixmap(self.main.realHomeDir+"/"+profile+"/avatars/"+unicode(jid)).scaled(22,22,QtCore.Qt.KeepAspectRatio)
				result=QtGui.QPixmap(22,22)
				result.fill(QtCore.Qt.transparent)
				painter=QtGui.QPainter(result)
				painter.drawPixmap((22-avatar.width())/2,(22-avatar.height())/2,avatar)
				painter.end()
				result=QtGui.QIcon(result)
			else:
				result=QtGui.QIcon("images/22x22/apps/jabbim.png")
	
			#self.ui.profilesList.addItem(result,jid)
			item=QtGui.QListWidgetItem(result,jid,self.ui.profilesList)
		return profiles

	def newProfile(self):
		if self.main.QT43:
			fs=firststart.firstStartWizard(self.main,self.main)
			fs.exec_()
			self.loadProfiles()

	def removeProfile(self):
		item=self.ui.profilesList.currentItem()
		jid=unicode(item.text())
		shutil.rmtree(self.main.realHomeDir+"/"+jid+"-profile",True)
		profiles=self.loadProfiles()
		print profiles
		if len(profiles)>0:
			print "profilechanged"
			self.main.profileChanged(profiles[0].replace("-profile",''))
		self.main.fillLoginForm()

	def profileChanged(self,item,old):
		self.ui.removeProfile.setEnabled(True)
	

