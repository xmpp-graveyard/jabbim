try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."

class TitleBar(QtGui.QWidget):
	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.setAutoFillBackground(True)
		self.setBackgroundRole(QtGui.QPalette.Highlight)
		self.parent=parent
		self.close = QtGui.QToolButton(self)

		self.pix = self.style().standardPixmap(QtGui.QStyle.SP_TitleBarCloseButton)
		self.close.setIcon(QtGui.QIcon(self.pix))
		self.close.setMinimumHeight(20)


		self.label = QtGui.QLabel(self)
		self.label.setText("Window Title")
		self.parent.setWindowTitle("Window Title")

		hbox = QtGui.QHBoxLayout(self)

		hbox.addWidget(self.label)
		hbox.addWidget(self.close)

		hbox.insertStretch(1, 500)
		hbox.setSpacing(0)
		self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)

		self.maxNormal = False

		self.connect(self.close, QtCore.SIGNAL(" clicked() "), parent.close)

	def showSmall(self):
		self.parentWidget().showMinimized()

	def showMaxRestore(self):
	    if self.maxNormal:
	        self.parentWidget().showNormal()
	        self.maxNormal = not self.maxNormal
	        self.maximize.setIcon(self.maxPix)
	    else:
	        self.parentWidget().showMaximized()
	        self.maxNormal = not self.maxNormal
	        self.maximize.setIcon(self.restorePix)

	def mousePressEvent(self,me):
		self.startPos = me.globalPos()
		self.clickPos = self.mapToParent(me.pos())

	def mouseMoveEvent(self,me):
		if self.maxNormal:
			return
		self.parentWidget().move(me.globalPos() - self.clickPos)


class Frame(QtGui.QFrame):
	def __init__(self):
		QtGui.QFrame.__init__(self,None)
		self.m_mouse_down = False
		self.setFrameShape(self.NoFrame)

		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setMouseTracking(True)

		self.m_titleBar = TitleBar(self)

		self.m_content = QtGui.QWidget(self)

		vbox = QtGui.QVBoxLayout(self)
		vbox.addWidget(self.m_titleBar)
		vbox.setMargin(0)
		vbox.setSpacing(0)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.m_content)
		layout.setMargin(5)
		layout.setSpacing(0)
		vbox.addLayout(layout)
		self.m_mouse_down=False
		self.left=self.right=self.bottom=False
		self.g=None

	def resizeEvent(self,event):
		r=QtGui.QRegion(10,0,event.size().width()-20,event.size().height())
		r2=QtGui.QRegion(0,10,event.size().width(),event.size().height()-20)
		r=r.united(r2)
		r=r.united(QtGui.QRegion(0,0,20,20,QtGui.QRegion.Ellipse))
		r=r.united(QtGui.QRegion(event.size().width()-20,0,20,20,QtGui.QRegion.Ellipse))
		r=r.united(QtGui.QRegion(event.size().width()-20,event.size().height()-20,20,20,QtGui.QRegion.Ellipse))
		r=r.united(QtGui.QRegion(0,event.size().height()-20,20,20,QtGui.QRegion.Ellipse))
		self.setMask(r)

		return QtGui.QFrame.resizeEvent(self,event)


	def contentWidget(self):
		return self.m_content

	def titleBar(self):
		return self.m_titleBar

	def mousePressEvent(self,e):
	    self.m_old_pos = e.pos()
	    self.m_mouse_down = e.button() == QtCore.Qt.LeftButton

	def mouseMoveEvent(self,e):
		x = e.x()
		y = e.y()
		if self.m_mouse_down:
			dx = x - self.m_old_pos.x()
			dy = y - self.m_old_pos.y()

			g = self.geometry()

#			if self.left:
#			    g.setLeft(g.left() + dx)
#			if self.right:
#			    g.setRight(g.right() + dx)
			if self.bottom or self.right:
			    g.setBottom(g.bottom() + dy)
			    g.setRight(g.right() + dx)

			self.setGeometry(g)
			self.layout().update()
			self.resizeEvent(QtGui.QResizeEvent(QtCore.QSize(self.width(),self.height()),QtCore.QSize(self.width(),self.height())))
##			self.m_old_pos = QPoint(!left ? e.x() : m_old_pos.x(), e.y())
			self.m_old_pos = QtCore.QPoint(e.x(), e.y())
		else:
		    r = self.rect()
#		    self.left = abs(x - r.left()) <= 5.
		    self.right = abs(x - r.right()) <= 5.
		    self.bottom = abs(y - r.bottom()) <= 5.
		    hor = self.left or self.right

		    if hor and self.bottom:
		        if self.left:
		            self.setCursor(QtCore.Qt.SizeBDiagCursor)
		        else:
		            self.setCursor(QtCore.Qt.SizeFDiagCursor)
#		    elif hor:
#		        self.setCursor(QtCore.Qt.SizeHorCursor)
#		    elif self.bottom:
#		        self.setCursor(QtCore.Qt.SizeVerCursor)
		    else:
		        self.setCursor(QtCore.Qt.ArrowCursor)

	def mouseReleaseEvent(self,e):
	    self.m_mouse_down = False
            if self.g:
		self.setGeometry(self.g)
		self.layout().update()
		self.resizeEvent(QtGui.QResizeEvent(QtCore.QSize(self.width(),self.height()),QtCore.QSize(self.width(),self.height())))
##
##private:
##    TitleBar *m_titleBar.
##    QWidget *m_content.
##    QPoint m_old_pos.
##    bool m_mouse_down.
##    bool left, right, bottom.
##}.


app=QtGui.QApplication([])

box=Frame()
box.move(0,0)

l = QtGui.QVBoxLayout(box.contentWidget())
l.setMargin(0)
edit = QtGui.QTextEdit(box.contentWidget())
l.addWidget(edit)

box.show()
app.exec_()
