from PyQt4 import QtCore, QtGui
class tabWidget(QtGui.QTabBar):
	def __init__(self,main,parent):
		QtGui.QTabBar.__init__(self,parent)
		self.main=main

	def mousePressEvent(self,event):
		if event.button()==QtCore.Qt.LeftButton:
			i=self.tabAt(event.pos())
			if i==0:
				self.main.ui.roster.favouriteMode=False
				self.main.ui.roster.setSize()
				self.main.ui.roster.repaint()
				return QtGui.QTabBar.mousePressEvent(self,event)
			elif i==1:
				self.setCurrentIndex(0)
				self.blockSignals(True)
				r=QtGui.QTabBar.mousePressEvent(self,event)
				self.blockSignals(False)
				self.main.ui.roster.favouriteMode=True
				self.main.ui.roster.setSize()
				self.main.ui.roster.repaint()
				return r
			else:
				return QtGui.QTabBar.mousePressEvent(self,event)
