try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
	
def loadPalette(data):
	palette=QtGui.QPalette()
	if data.has_key("base"):
		if len(data["base"])!=0:
			palette.setColor(QtGui.QPalette.Base,QtGui.QColor(data["base"]))
	elif data.has_key("alternateBase"):
		if len(data["alternateBase"])!=0:
			palette.setColor(QtGui.QPalette.AlternateBase,QtGui.QColor(data["alternateBase"]))
	elif data.has_key("text"):
		if len(data["text"])!=0:
			palette.setColor(QtGui.QPalette.Text,QtGui.QColor(data["text"]))
	elif data.has_key("highlight"):
		if len(data["highlight"])!=0:
			palette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(data["highlight"]))
	elif data.has_key("highlightedText"):
		if len(data["highlightedText"])!=0:
			palette.setColor(QtGui.QPalette.HighlightedText,QtGui.QColor(data["highlightedText"]))
	return palette
