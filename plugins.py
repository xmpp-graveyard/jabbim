try:
	from PyQt4 import QtCore, QtGui
except:
	print "PyQt4 is not installed."

def addChatWindowMenu(main,title,function):
	menu=main.chat.ui.menubar.addMenu(title)
	menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),function)
	return menu

def addChatWindowMenuAction(menu,title,identification):
	action=menu.addAction(title)
	action.setData(QtCore.QVariant(unicode(identification)))
	return action

def getActionID(action):
	data=action.data()
	return unicode(data.toString())