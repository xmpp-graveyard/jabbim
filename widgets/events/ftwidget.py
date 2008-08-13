import os,sys
try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

from ftwidget_ui import *
from ftuploadwidget_ui import *
import time
import weakref
from os.path import basename


class FTDownloadWidget(QtGui.QWidget):
	def __init__(self,event):
		QtGui.QWidget.__init__(self,None)
		self.ui=Ui_FTWidget()
		self.ui.setupUi(self)
		self.metrics=QtGui.QFontMetrics(self.ui.filename.font())
		self.size=0
		self.timestamp=time.time()
		self.transfered=0
		self.event=weakref.proxy(event)
		self.ui.reject.hide()
		self.ui.accept.hide()
		QtCore.QObject.connect(self.ui.accept,QtCore.SIGNAL("clicked()"),self.accept)
		QtCore.QObject.connect(self.ui.reject,QtCore.SIGNAL("clicked()"),self.reject)
		self.file=""
		#self.transfered=0

	def resizeEvent(self,event):
		print "WIDTH",self.width()
		self.ui.filename.setText(unicode(self.metrics.elidedText(basename(self.file),QtCore.Qt.ElideMiddle, self.width()-10)))
		return QtGui.QWidget.resizeEvent(self,event)

	def eventAccepted(self):
		pass

	def eventRejected(self):
		pass

	def accept(self):
		filename=unicode(self.file)
		if sys.platform == 'win32':
			filename=filename.replace("/","\\")
			print "open win32",[filename]
			os.startfile(filename)
		else:
			print "open linux",[filename]
			os.system(u"xdg-open \"%s\"" % filename.encode('utf8'))
		#self.event.accept()

	def reject(self):
		self.event.reject()

	def setText(self,text):
		return
		self.ui.filename.setText(text)

	def setFileSize(self,size):
		self.size=int(size)

	def setCurrentFile(self,file):
		self.file=file
		print "WIDTH",self.width()
		self.ui.filename.setText(unicode(self.metrics.elidedText(basename(self.file),QtCore.Qt.ElideMiddle, self.width()-10)))
		

	def transferFinished(self):
		self.ui.progressBar.hide()
		self.ui.accept.show()
		self.ui.reject.show()
		self.ui.transferInfo.setText(self.tr("Finished"))

	def setFileTransfered(self,transfered):
		self.ui.progressBar.setValue(int((float(transfered)/float(self.size))*100))
		newTimestamp=time.time()
		d=newTimestamp-self.timestamp
		if d>1:
			diff=transfered-self.transfered
			self.transfered=transfered
			self.timestamp=newTimestamp
			ratio=1.0/d
			speed=int(diff*ratio)
			remaining=int((self.size-transfered)/speed)
			self.ui.transferInfo.setText(unicode(self.tr("Remaining:"))+" "+unicode(remaining)+" s "+"("+str(speed/1000)+" kB/s)")

class FTUploadWidget(QtGui.QWidget):
	def __init__(self,event):
		QtGui.QWidget.__init__(self,None)
		self.ui=Ui_FTUploadWidget()
		self.ui.setupUi(self)
		self.metrics=QtGui.QFontMetrics(self.ui.filename.font())
		self.text=""
		self.queue={}
		self.size=0
		self.timestamp=time.time()
		self.transfered=0
		self.event=weakref.proxy(event)
		self.ui.reject.hide()
		self.ui.more.hide()
		QtCore.QObject.connect(self.ui.reject,QtCore.SIGNAL("clicked()"),self.reject)
		#self.ui.accept.hide()
		self.setQueue(self.event.queue)

		#self.transfered=0

	def resizeEvent(self,event):
		self.ui.filename.setText(self.metrics.elidedText(self.text,QtCore.Qt.ElideMiddle, self.width()-10-self.ui.toolButton.width()))
		text=""
		for file in self.queue.keys():
			text+=unicode(self.metrics.elidedText(basename(file),QtCore.Qt.ElideMiddle, self.width()-10))+'<br/>'
		self.ui.more.setText(text)
		return QtGui.QWidget.resizeEvent(self,event)

	def eventAccepted(self):
		pass

	def eventRejected(self):
		pass

	def reject(self):
		self.event.reject()

	def setText(self,text):
		self.text=unicode(text)
		self.ui.filename.setText(self.metrics.elidedText(text,QtCore.Qt.ElideMiddle, self.width()-10-self.ui.toolButton.width()))

	def setQueue(self,queue):
		self.queue=queue
		text=""
		for file in self.queue.keys():
			text+=unicode(self.metrics.elidedText(basename(file),QtCore.Qt.ElideMiddle, self.width()-10))+'<br/>'
		self.ui.more.setText(text)

	def setCurrentFile(self,file):
		self.setText(basename(file))

	def setFileSize(self,size):
		self.size=int(size)

	def transferFinished(self):
		self.ui.progressBar.hide()
		self.ui.more.hide()
		self.ui.toolButton.hide()
		#self.ui.accept.show()
		self.ui.reject.show()
		self.ui.transferInfo.setText(self.tr("Finished"))

	def setFileTransfered(self,transfered):
		self.ui.progressBar.setValue(int((float(transfered)/float(self.size))*100))
		newTimestamp=time.time()
		d=newTimestamp-self.timestamp
		if d>1:
			diff=transfered-self.transfered
			self.transfered=transfered
			self.timestamp=newTimestamp
			ratio=1.0/d
			speed=int(diff*ratio)
			if speed!=0:
				remaining=int((self.size-transfered)/speed)
			else:
				remaining="N/A"
			self.ui.transferInfo.setText(unicode(self.tr("Remaining:"))+" "+unicode(remaining)+" s "+"("+str(speed/1000)+" kB/s)")
