#-*-coding:UTF-8-*-

from PyQt4 import QtGui, QtCore
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.python import log
import dataforms
from commands_ui import Ui_Dialog

class CommandsDialog(QtGui.QDialog):
	def __init__(self, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

	def reject(self):
		self.close()
		

class Commands:
	def __init__(self, main, jid):
		self.main	= main
		self.jid	= unicode(jid)
		self.dialog	= CommandsDialog()
		self.requestCommandsList()

	def requestCommandsList(self):
		iq		= IQ(self.main.client.xmlstream, "get")
		iq["to"]	= self.jid
		query		= iq.addElement("query", "http://jabber.org/protocol/disco#items")
		query.attributes["node"] = "http://jabber.org/protocol/commands"
		d		= iq.send()
		d.addCallback(self._commandsListRecieved).addErrback(self.main.client.chyba)
		self.main.client.disp(iq["id"])
		log.msg("Sending request for Ad-Hoc Commands list")

	def _commandsListRecieved(self, el):
		log.msg("Ad-Hoc commands list recieved")
		query	= el.firstChildElement()
		commands = []
		for item in query.elements():
			if item.name != "item":
				continue
			commands.append(item.attributes)
		
		c = 0
		for command in commands:
			button = QtGui.QPushButton(self.dialog)
			button.setText(unicode(command["name"]))
			button.setObjectName(unicode(command["node"])) # ? + jid
			self.dialog.ui.gridlayout2.addWidget(button, c, 0)
			c += 1

