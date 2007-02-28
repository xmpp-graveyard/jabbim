try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from gameslist_ui import *

class gamesListWindow(QtGui.QMainWindow):
	def __init__(self,parent,main,jab):
		apply(QtGui.QMainWindow.__init__,(self,parent))
		self.main=main
		self.jab=jab
		self.ui=Ui_gameslist()
		self.ui.setupUi(self)
		QtCore.QObject.connect(self.ui.refreshButton, QtCore.SIGNAL("clicked()"),self.refreshList)

	def refreshList(self,typ=None):
		if typ==None:
			typ=self.typ
		else:
			self.typ=typ
		self.jab.listGames(int(typ))
