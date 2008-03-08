# -*- coding: utf-8 -*- 
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
import gc
import sys,os
sys.path.append('.')
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

class jabbimApplication(QtGui.QApplication):
	def __init__(self,args=[]):
		QtGui.QApplication.__init__(self,args)
		self.shutdown=False
	
	def commitData(self,manager):
		print "data commited"
		self.shutdown=True
		manager.release()

app = jabbimApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)
#qt4reactor.install(app)
#from twisted.internet import reactor, threads
#from twisted.internet.defer import DeferredList
#from twisted.python import log
import time,base64, re
try:
	from hashlib import sha1
except:
	log.msg('Please upgrade to python2.5')
	from sha import new as sha1

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		#self.ui=widgets.mainWindow.Ui_MainWindow()
		#self.ui.setupUi(self)

		# show tray icon
		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon(QtGui.QIcon("images/16x16/apps/jabbim.png").pixmap(16,16,QtGui.QIcon.Disabled)))
		app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.show()
		self.buildTrayMenu()
	def buildTrayMenu(self):
		"""
		Builds system tray menu.
		"""
		menu=QtGui.QMenu(self)
		menu.addAction(self.tr("Quit"),self.trayQuit)
		self.tray.setContextMenu(menu)
	def closeEvent(self,event):
		"""
		Hides window to the tray or quit if tray is not visible. Called by WM when windows is closed.
		"""
		print "TRAY VISIBLE MAIN:"+unicode(self.tray.isVisible())
		if self.tray.isVisible():
			self.hide()
			event.accept()
			return
		self.trayQuit()
		event.accept()

	def trayQuit(self,bool=True):
		"""
		Exits Jabbim.
		"""
		# close windows, hide tray :)
		app.closeAllWindows()
		self.tray.hide()
		app.quit()
		# stop reactor

	def trayActivated(self,reason=QtGui.QSystemTrayIcon.Trigger):
		"""
		Shows or hides mainWindow. Called when is tray activated.
		"""
		if reason==QtGui.QSystemTrayIcon.Trigger:
			if self.isHidden():
				self.show()
				self.raise_()
				self.activateWindow()
				self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
			else:
				if self.windowState() & QtCore.Qt.WindowMinimized:
					self.show()
					self.raise_()
					self.activateWindow()
					self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
				else:
					self.hide()
		elif reason==QtGui.QSystemTrayIcon.MiddleClick:
			if self.isHidden():
				self.show()
				self.raise_()
				self.activateWindow()
				self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
			else:
				if self.windowState() & QtCore.Qt.WindowMinimized:
					self.show()
					self.raise_()
					self.activateWindow()
					self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
				else:
					self.hide()

if __name__ == "__main__":
	translator=QtCore.QTranslator()
	translator.load("locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm")
	print "trying to load locales:","locales/jabbim_"+unicode(QtCore.QLocale.system().name())[:2]+".qm"
	app.installTranslator(translator)
	#app.setStyle(style())
	MainWindow = mainWindow()
	MainWindow.show()
	app.exec_()
