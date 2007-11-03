from PyQt4 import QtGui, QtCore
from twisted.python import log
 
class showLabel(QtGui.QLabel):
        def __init__(self, main, defaulttext = ""):
                QtGui.QLabel.__init__(self, None)
		self.defaulttext = unicode(defaulttext)
		self.setText(self.defaulttext)
                self.main=main
		
        def mouseReleaseEvent(self,event):
		text = unicode(self.text())
		if text == self.defaulttext: # Asi neni nechytrejsi
			text = u"" 
		self.main.lineEdit.setText(text)
		self.main.lineEdit.show()
                self.hide()
		
class showLineEdit(QtGui.QLineEdit):
	def __init__(self, label, parent):
                QtGui.QLineEdit.__init__(self, parent)
		self.label = label

	def keyPressEvent(self, event):
		key = event.key()
		if key == QtCore.Qt.Key_Escape:
			self.label.show()
			self.hide()
		else:
			QtGui.QLineEdit.keyPressEvent(self, event)

class showWidget(QtGui.QWidget):
	def __init__(self, main, layout, labeltext = ""):
		QtGui.QWidget.__init__(self, None)
		self.main = main
		self.label = showLabel(self, labeltext)
		layout.addWidget(self.label)
		self.lineEdit = showLineEdit(self.label, self)
		self.lineEdit.hide()
		QtCore.QObject.connect(self.lineEdit,QtCore.SIGNAL("lostFocus ()"),self.lineEditToLabel)
		QtCore.QObject.connect(self.lineEdit,QtCore.SIGNAL("returnPressed ()"),self.lineEditToLabel)
                layout.addWidget(self.lineEdit)
		self.resize(300,50)
		
	def lineEditToLabel(self):
		text = unicode(self.lineEdit.text())
		self.label.setText(text)
		if text == u"":
			self.label.setText(self.label.defaulttext)
		self.label.show()
		self.lineEdit.hide()
		self.main.client.sendPresence(
			status = text,
			show = self.main.client.roster['users'][self.main.client.jid.userhost()].resources[self.main.client.jid.resource].show
		)

