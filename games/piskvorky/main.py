 # -*- coding: UTF-8 -*-
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
	
#from Numeric import zeros
from piskvorky import *
from preparegame import *

class config:
	name=u"Piškvorky"
	id=1
	room="piskvorky@games.jabbim.cz"
	about="Piskvorky is game for jGames developed by Jan Kaluza licensed under GPL."
	icon="images/piskvorky/icon.png"
	
class prepareGameWindow(QtGui.QWidget):
	def __init__(self,name,main,jab,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=Ui_prepareGame()
		self.ui.setupUi(parent)
		self.main=main
		self.name=name
		self.jab=jab
		QtCore.QObject.connect(self.ui.play,QtCore.SIGNAL("clicked()"),self.accept)
		#QtCore.QObject.connect(self.ui.cancel,QtCore.SIGNAL("clicked()"),self.reject)
		"""
		Jabber: Zacatek nastavovaci faze hry - nazev hry = promenna name
		"""
	def accept(self):
		"""
		Jabber: Finalni start hry
		"""
		setup=[self.ui.kolecko.isChecked(),self.ui.width.value(),self.ui.heigth.value()]
		self.main.games.append([piskvorkyWindow(setup,self.jab,self.main),config.id])
		self.main.games[-1][0].show()
		print self.main.games[-1]
		for game in self.main.preparedGames:
			if game[0]==self:
				self.main.preparedGames.remove(game)
				print self.main.preparedGames
				break

	#def reject(self):
		#"""
		#Jabber: Zruseni nastavovaci faze hry
		#"""
		#for game in self.main.preparedGames:
			#if game[0]==self:
				#self.main.preparedGames.remove(game)
				#print self.main.preparedGames
				#break

class piskvorkyWindow(QtGui.QDialog):
	def __init__(self,setup,jab,main,parent=None):
		apply(QtGui.QDialog.__init__,(self,parent))
		#self.setModal(False)
		self.ui=Ui_piskvorky()
		self.ui.setupUi(self)
		self.jab=jab
		self.main=main
		layout=QtGui.QHBoxLayout(self.ui.gameFrame)
		self.gameWidget=deskWidget(self.jab,self.ui.gameFrame,20,setup[1],setup[2],setup[0])
		layout.addWidget(self.gameWidget,QtCore.Qt.AlignCenter)

	def reject(self):
		"""
		Jabber: Zruseni hry
		"""
		for game in self.main.games:
			if game[0]==self:
				self.main.games.remove(game)
				print self.main.games
				break
		self.close()



class deskWidget(QtGui.QWidget):
	def __init__(self,jab,parent=None,side=20,countX=26,countY=26,cross=False, *args):
		apply(QtGui.QWidget.__init__,(self,parent) + args)
		self.side=side
		self.countX=countX
		self.countY=countY
		self.setMinimumSize(self.countX*self.side+7,self.countY*self.side+7)
		self.setMaximumSize(self.countX*self.side+8,self.countY*self.side+8)
		self.desk = zeros([self.countY,self.countX])
		self.jab=jab
		self.x=QtGui.QPixmap("images/piskvorky/x.png")
		self.o=QtGui.QPixmap("images/piskvorky/o.png")
		if cross==False:
			self.variable=-1
		else:
			self.variable=1

	def mouseReleaseEvent(self,qe):
		x=qe.x()/self.side
		y=qe.y()/self.side
		if (x+1>self.countX or y+1>self.countY) or (x+1<0 or y+1<0):
			print "You clicked out of desk."
		elif self.desk[y][x]!=0:
			print "Field is not free."
		else:
			self.desk[y][x]=self.variable
			self.repaint()
			# this will put move into queue and jabber class will process it then
			self.jab.inc.put([x,y])
			print self.desk

	def paintEvent(self, qe):
		desk=QtGui.QPainter(self)
		#desk.setBackground(QtGui.QBrush(QtGui.QColor(128,128,128)))
		desk.setRenderHint(desk.Antialiasing)
		desk.setPen(QtGui.QPen(QtGui.QColor(64,64,64), 1))
		for x in range(self.countX+1):
			desk.drawLine(x*self.side,0,x*self.side,self.countY*self.side)
		for y in range(self.countY+1):
			desk.drawLine(0,y*self.side,self.countX*self.side,y*self.side)
		for y in range(len(self.desk)):
			for x in range(len(self.desk[y])):
				if self.desk[y][x]==-1:
					#desk.setPen(QtGui.QPen(QtCore.Qt.blue, 2))
					desk.drawPixmap(x*self.side,y*self.side,self.x)
					#desk.drawLine(x*self.side,y*self.side,x*self.side+self.side,y*self.side+self.side)
					#desk.drawLine(x*self.side+self.side,y*self.side,x*self.side,y*self.side+self.side)
				elif self.desk[y][x]==1:
					#desk.setPen(QtGui.QPen(QtCore.Qt.red, 2))
					desk.drawPixmap(x*self.side,y*self.side,self.o)