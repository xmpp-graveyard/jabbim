try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
from headlinewidget_ui import *

class headlineWidget(QtGui.QWidget):
	def __init__(self,main,jab,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.jab=jab
		self.ui=Ui_headlinewidget()
		self.ui.setupUi(self)
		self.main=main
		QtCore.QObject.connect(self.ui.messages, QtCore.SIGNAL("itemClicked ( QTreeWidgetItem * , int )"),self.clicked)
		self.ui.messages.hideColumn(3)

	def clicked(self,item,i):
		urls=item.data(32,0)
		urls=urls.toList()
		descs=item.data(32,1)
		descs=descs.toList()
		html=unicode(item.text(3))+"<br/>--------<br/>"
		for i in range(len(urls)):
			print i,urls[i]
			html+=unicode(urls[i].toString())+" - "+unicode(descs[i].toString())+"</br>"
		self.ui.text.setHtml(html)

	def addMessage(self,jid,subject,text,urls,descs,date):
		item=QtGui.QTreeWidgetItem(self.ui.messages)
		item.setText(0,unicode(subject))
		item.setText(1,unicode(jid))
		item.setText(2,unicode(date))
		item.setText(3,unicode(text))
		item.setData(32,0,QtCore.QVariant(urls))
		item.setData(32,1,QtCore.QVariant(descs))