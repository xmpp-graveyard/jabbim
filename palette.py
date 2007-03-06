try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."
	
def loadPalette(palette,data):
	if data.has_key("base"):
		if len(data["base"])!=0:
			palette.setColor(QtGui.QPalette.Base,QtGui.QColor(data["base"]))
	if data.has_key("alternateBase"):
		if len(data["alternateBase"])!=0:
			palette.setColor(QtGui.QPalette.AlternateBase,QtGui.QColor(data["alternateBase"]))
	if data.has_key("text"):
		if len(data["text"])!=0:
			palette.setColor(QtGui.QPalette.Text,QtGui.QColor(data["text"]))
	if data.has_key("highlight"):
		if len(data["highlight"])!=0:
			palette.setColor(QtGui.QPalette.Highlight,QtGui.QColor(data["highlight"]))
	if data.has_key("highlightedText"):
		if len(data["highlightedText"])!=0:
			palette.setColor(QtGui.QPalette.HighlightedText,QtGui.QColor(data["highlightedText"]))
	if data.has_key("baseAlpha"):
		if len(data["baseAlpha"])!=0:
			#color=palette.color(QtGui.QPalette.Base)
			#color.setAlpha(int(data["baseAlpha"]))
			#palette.setColor(QtGui.QPalette.Base,color)
			palette.setColor(QtGui.QPalette.Base,QtCore.Qt.transparent)
	if data.has_key("alternateBaseAlpha"):
		if len(data["alternateBaseAlpha"])!=0:
			#color=palette.color(QtGui.QPalette.AlternateBase)
			#color.setAlpha(int(data["alternateBaseAlpha"]))
			palette.setColor(QtGui.QPalette.AlternateBase,QtCore.Qt.transparent)
	return palette
