try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

from paint_ui import *

class paintArea(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.pen=QtGui.QPen(QtGui.QColor(0,0,0),5,QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,QtCore.Qt.RoundJoin)
		self.pen.setWidth(5)
##		gradient=QtGui.QLinearGradient(10,10,20,20)
##		gradient.setColorAt(0.0, QtGui.QColor(128,128,128,63))
##		gradient.setColorAt(1.0, QtGui.QColor(255,255,0, 191))
##		self.pen.setBrush(gradient)
		self.brush=QtGui.QBrush(QtGui.QColor(0,0,0))
		self.newImage(400,400)
		self.penSize=5
		self.tool="pen"
		self.mousePress=[-1,-1]
		self.mouseActual=[-1,-1]

	def penSizeChanged(self,value):
		self.penSize=int(value)
		self.pen.setWidth(self.penSize)

	def toolChanged(self,tool):
		self.tool=unicode(tool)

	def newImage(self,w,h):
		self.image=QtGui.QImage(w,h,QtGui.QImage.Format_RGB32)
		self.image.fill(QtGui.QColor(255,255,255).rgb())
		self.setMaximumSize(QtCore.QSize(w,h))
		self.setMinimumSize(QtCore.QSize(w,h))

	def getImage(self):
		return self.image
	
	def paintEvent(self,event):
		QtGui.QWidget.paintEvent(self,event)
		p=QtGui.QPainter(self)
		p.drawImage(0,0,self.image)
		if self.mousePress[0]!=-1:
			p.drawRect(self.mousePress[0],self.mousePress[1],self.mouseActual[0]-self.mousePress[0],self.mouseActual[1]-self.mousePress[1])

	def mousePressEvent(self,event):
		if self.tool!="pen":
			self.mousePress=[int(event.x()),int(event.y())]
		elif self.tool == 'pen':
			p=QtGui.QPainter(self.image)
			self.setupPainter(p)
			p.drawLine(event.x(),event.y(),event.x(),event.y())
			self.repaint()

	def mouseReleaseEvent(self,event):
		if self.tool=="square":
			p=QtGui.QPainter(self.image)
			self.setupPainter(p)
			r=QtCore.QRect(self.mousePress[0],self.mousePress[1],event.x()-self.mousePress[0],event.y()-self.mousePress[1])
			p.drawRect(r)
			self.repaint()
		self.mousePress=[-1,-1]
		self.mouseActual=[-1,-1]

	def mouseMoveEvent(self,event):
		if self.mouseActual[0]!=-1:
			if self.tool=="pen":
				p=QtGui.QPainter(self.image)
				self.setupPainter(p)
				p.drawLine(self.mouseActual[0],self.mouseActual[1],event.x(),event.y())
		self.repaint()
		self.mouseActual=[int(event.x()),int(event.y())]

	def setupPainter(self,p):
		p.setRenderHint(QtGui.QPainter.Antialiasing, True)
		p.setPen(self.pen)
		p.setBrush(self.brush)

class paintWindow(QtGui.QMainWindow):
	def __init__(self,parent=None,  chatwidget = None):
		QtGui.QMainWindow.__init__(self,parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		l=QtGui.QHBoxLayout(self.ui.container)
		self.paintArea=paintArea(self.ui.container)
		l.addWidget(self.paintArea)
		self.chat = chatwidget
		
		QtCore.QObject.connect(self.ui.penSize,QtCore.SIGNAL("valueChanged ( int  )"),self.paintArea.penSizeChanged)
		QtCore.QObject.connect(self.ui.pen,QtCore.SIGNAL("clicked()"),self.pen)
		QtCore.QObject.connect(self.ui.square,QtCore.SIGNAL("clicked()"),self.square)
		QtCore.QObject.connect(self.ui.sendButton,QtCore.SIGNAL("clicked()"),self.send)
		QtCore.QObject.connect(self.ui.clearButton,QtCore.SIGNAL("clicked()"),self.clear)
		
	def pen(self):
		self.paintArea.toolChanged("pen")

	def square(self):
		self.paintArea.toolChanged("square")
	
	def send(self):
		self.chat.sendPaint(self.paintArea.image)
	
	def clear(self):
		self.paintArea.newImage(400,400)
		self.paintArea.repaint()
	
	def open(self,  path = None,  image = None):
		if image == None:
			img = QtGui.QImage(path)
			if not img.isNull():
				self.paintArea.image = img
			else:
				self.paintArea.newImage(400,400)
		else:
			self.paintArea.image = image
		self.paintArea.repaint()

if __name__ == "__main__":
	app=QtGui.QApplication([])

	w=paintWindow()
	w.show()

	app.exec_()
