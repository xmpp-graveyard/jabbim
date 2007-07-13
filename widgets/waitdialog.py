# -*- coding: utf-8 -*-
try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

class waitDialog(QtGui.QDialog):
	def __init__(self,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		self.setModal(True)
		
	def accept(self):
		self.done(1)
	def reject(self,send=True):
		if send:
			pass
			#self.main.queue.append("<game><typ>gameAbort</typ><gameid>"+str(self.gameid)+"</gameid><from>"+unicode(self.main.nickname)+"</from></game>")
		self.done(-1)
