try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

from paint_ui import *

class paintArea(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.pen=QtGui.QPen()
		self.pen.setWidth(5)
		self.brush=QtGui.QBrush(QtGui.QColor(0,0,0))
		self.newImage(400,400)
		self.penSize=5
		self.tool="pen"
		self.mousePress=[-1,-1]
		self.mouseActual=[0,0]

	def penSizeChanged(self,value):
		self.penSize=int(value)

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
		if self.tool=="square" and self.mousePress[0]!=-1:
			p.drawRect(self.mousePress[0],self.mousePress[1],self.mouseActual[0]-self.mousePress[0],self.mouseActual[1]-self.mousePress[1])
	
	def mousePressEvent(self,event):
		if self.tool!="pen":
			self.mousePress=[int(event.x()),int(event.y())]

	def mouseReleaseEvent(self,event):
		if self.tool=="square":
			p=QtGui.QPainter(self.image)
			p.setPen(self.pen)
			p.setBrush(self.brush)
			p.drawRect(self.mousePress[0],self.mousePress[1],event.x()-self.mousePress[0],event.y()-self.mousePress[1])
			self.repaint()
		if self.tool=="floodfill":
			self.floodFill(int(event.x()), int(event.y()))
		self.mousePress=[-1,-1]

	def mouseMoveEvent(self,event):
		if self.tool=="pen":
			p=QtGui.QPainter(self.image)
			p.setPen(self.pen)
			p.setBrush(self.brush)
			p.drawEllipse(event.x(),event.y(),self.penSize,self.penSize)
		else:
			self.mouseActual=[int(event.x()),int(event.y())]
		self.repaint()
	
	def floodFill(self, x, y):
		painter = QtGui.QPainter(self.image)
		queue = []
		queue.append((x, y))
		# local variable access is faster in Python
		get_pixel = self.image.pixel
		target_color = get_pixel(x, y)
		lines_drawn = 0
		img_width = self.image.width()
		img_height = self.image.height()
		while len(queue) != 0:
			(x, y) = queue.pop(0)
			if get_pixel(x, y) == target_color:
				w = e = x
				while w > 0 and get_pixel(w-1, y) == target_color:
					w -= 1
				while e+1 < img_width and get_pixel(e+1, y) == target_color:
					e += 1
				if e != w:
					painter.drawLine(w, y, e, y)
				else:
					painter.drawPoint(w, y)

				# complete floodfill can take a while, so repaint once in a while
				# to have visible progress
				lines_drawn += 1
				if lines_drawn == 100:
					self.repaint()
					lines_drawn = 0

				if y > 0:
					was_target = False
					for x in xrange(w, e+1):
						is_target = (get_pixel(x, y-1) == target_color)
						if is_target and not was_target:
							queue.append((x, y-1))
						was_target = is_target

				if y + 1 < img_height:
					was_target = False
					for x in xrange(w, e+1):
						is_target = (get_pixel(x, y+1) == target_color)
						if is_target and not was_target:
							queue.append((x, y+1))
						was_target = is_target
		self.repaint()


class paintWindow(QtGui.QMainWindow):
	def __init__(self,parent=None):
		QtGui.QMainWindow.__init__(self,parent)
		self.ui=Ui_MainWindow()
		self.ui.setupUi(self)
		l=QtGui.QHBoxLayout(self.ui.container)
		self.paintArea=paintArea(self.ui.container)
		l.addWidget(self.paintArea)
		
		QtCore.QObject.connect(self.ui.penSize,QtCore.SIGNAL("valueChanged ( int  )"),self.paintArea.penSizeChanged)
		QtCore.QObject.connect(self.ui.pen,QtCore.SIGNAL("clicked()"),self.pen)
		QtCore.QObject.connect(self.ui.square,QtCore.SIGNAL("clicked()"),self.square)
		QtCore.QObject.connect(self.ui.floodfill,QtCore.SIGNAL("clicked()"),self.floodfill)
		
	def pen(self):
		self.paintArea.toolChanged("pen")

	def square(self):
		self.paintArea.toolChanged("square")

	def floodfill(self):
		self.paintArea.toolChanged("floodfill")

app=QtGui.QApplication([])

w=paintWindow()
w.show()

app.exec_()
