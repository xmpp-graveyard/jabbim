try: from PyQt4 import QtCore, QtGui
except: print "PyQt4 is not installed."
locale=unicode(QtCore.QLocale.system().name())[:2]
help={}
if locale=="cs":
	help['resource']='(<a href="http://www.jabber.cz/wiki/Resource">?</a>)'
	