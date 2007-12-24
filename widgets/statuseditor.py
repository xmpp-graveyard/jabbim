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
from statuseditor_ui import *
from configobj import ConfigObj

class statusEditorWindow(QtGui.QDialog):
	def __init__(self,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.main=main
		self.ui=Ui_statusEditor()
		self.ui.setupUi(self)
		self.loadStatuses()
		QtCore.QObject.connect(self.ui.statusList, QtCore.SIGNAL("currentItemChanged ( QListWidgetItem *, QListWidgetItem *)"),self.statusChanged)
		QtCore.QObject.connect(self.ui.removeStatus, QtCore.SIGNAL("clicked()"),self.removeProfile)
		#QtCore.QObject.connect(self.ui.newProfile, QtCore.SIGNAL("clicked()"),self.newProfile)
		self.ui.removeStatus.setEnabled(False)

	def loadStatuses(self):
		self.ui.statusList.clear()
		config=ConfigObj(self.main.homeDir+'/statusmessages',encoding='UTF8')
		for key in config.keys():
			for status in config[key]:
				item=QtGui.QListWidgetItem(self.main.getIcon(status=key,size="16x16"),unicode(status),self.ui.statusList)
				#item.setData(32,QtCore.QVariant(int(config[key].index(status))))
				item.key=key
				item.index=int(config[key].index(status))
				#if len(status)>20:
					#action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),unicode(status)[:20]+"...")
				#else:
					#action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),unicode(status))
				#action.setData(QtCore.QVariant(key+"_"+unicode(config[key].index(status))))
			#self.statusWidgetMenu.addSeparator()
			#separator=False
			
		return []

	#def newProfile(self):
		#if self.main.QT43:
			#fs=firststart.firstStartWizard(self.main,self.main)
			#fs.exec_()
			#self.loadProfiles()

	def removeProfile(self):
		item=self.ui.statusList.currentItem()
		config=ConfigObj(self.main.homeDir+'/statusmessages',encoding='UTF8')
		del config[item.key][item.index]
		config.write()
		self.loadStatuses()
		self.main.buildStatusWidgetMenu()

	def statusChanged(self,item,old):
		print 'item changed'
		self.ui.removeStatus.setEnabled(True)
	

