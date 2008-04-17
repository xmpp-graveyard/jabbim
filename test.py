import sys
from PyQt4 import QtCore,QtGui

class delegate(QtGui.QItemDelegate):
	def __init__(self,parent=None):
		QtGui.QItemDelegate.__init__(self,parent)
	
	def paint(self,painter,option,index):
		# selected item
		if option.state & QtGui.QStyle.State_Selected and index.column()==0:
			#option.rect.setHeight(50)
			option.displayAlignment=QtCore.Qt.AlignTop
			users=unicode(index.data(32).toString())
			QtGui.QItemDelegate.paint(self,painter,option,index)
			#metrics=QtGui.QFontMetrics(option.font)
			painter.save()
			painter.setPen(option.palette.highlightedText().color())
			#print option.fontMetrics.height(),option.rect.y()
			#painter.drawText(option.rect.x()+QtGui.QApplication.style().pixelMetric(QtGui.QStyle.PM_FocusFrameHMargin) + 1,option.rect.y()+option.fontMetrics.height(),option.rect.width(),option.rect.height(),QtCore.Qt.TextWordWrap,users)
			doc=QtGui.QTextDocument()
			opt=doc.defaultTextOption()
			opt.setWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
			doc.setDefaultTextOption(opt)
			doc.setDefaultFont(option.font)
			doc.setPageSize(QtCore.QSizeF(option.rect.width(),option.rect.height()-option.fontMetrics.height()))
			doc.setHtml("<font color=\"%s\"><b>Users: </b>"%option.palette.highlightedText().color().name()+users+"</font>")
			painter.translate(option.rect.x()+1,option.rect.y()+option.fontMetrics.height())
			print option.rect.height()
			doc.drawContents(painter, QtCore.QRectF(0,0,option.rect.width(),option.rect.height()))
			painter.restore()
			return

		QtGui.QItemDelegate.paint(self,painter,option,index)
	
	def sizeHint(self,option,index):
		# selected item
		if option.state & QtGui.QStyle.State_Selected:
			return QtCore.QSize(100,50)
		return QtGui.QItemDelegate.sizeHint(self,option,index)


def itemChanged(current,old):
	#global window
	if old:
		old.setData(0,QtCore.Qt.SizeHintRole,QtCore.QVariant())
	if current:
		current.setSizeHint(0,QtCore.QSize(100,50))

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = QtGui.QTreeWidget()
	window.setItemDelegate(delegate(window))
	window.setUniformRowHeights(False)
	window.connect(window,QtCore.SIGNAL("currentItemChanged ( QTreeWidgetItem *, QTreeWidgetItem * )"),itemChanged)
	for word in ['a','b','c','d']:
		item=QtGui.QTreeWidgetItem(window)
		item.setText(0,word)
		item.setData(0,32,QtCore.QVariant(" a b s f  sdfd sf sdf sdf w ef wef s f sdf sd vsd v xd vas df sa ef wse es fs  fes "))
	window.show()
	sys.exit(app.exec_())
