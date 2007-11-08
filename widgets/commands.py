#-*-coding:UTF-8-*-

from PyQt4 import QtGui, QtCore
from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.python import log
import dataforms
from commands_ui import Ui_Dialog

class CommandsDialog(QtGui.QDialog):
	def __init__(self, cmds, parent = None):
		QtGui.QDialog.__init__(self, parent)
		self.cmds = cmds
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		
		self.group = QtGui.QButtonGroup(self)
		QtCore.QObject.connect(self.group,QtCore.SIGNAL("buttonClicked ( QAbstractButton * )"),self.buttonClicked) 

	def _resetLayout(self): # Asi neni nejchytrejsi
		for button in self.group.buttons():
			self.ui.gridlayout2.removeWidget(button)

	def buttonClicked(self, button):
		self.cmds.execCommand(button.node, button.jid)

	def reject(self):
		self.close()
		

class Commands:
	def __init__(self, main, jid):
		self.main	= main
		self.jid	= unicode(jid)
		self.dialog	= CommandsDialog(self)
		self.sessionid	= None
		self.dialog.ui.execute.hide()
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
		if commands == []:
			label = QtGui.QLabel(self.main.tr("Sorry. No commands available."))
			self.dialog.ui.gridlayout2.addWidget(label, 0, 0)
			return
		c = 0
		for command in commands:
			button = QtGui.QPushButton(self.dialog)
			button.setText(unicode(command["name"]))
			#button.setObjectName(unicode(command["node"])) # ? + jid
			button.node = unicode(command["node"])
			button.jid = unicode(command["jid"])
			self.dialog.group.addButton(button)
			self.dialog.ui.gridlayout2.addWidget(button, c, 0)
			c += 1

	def execCommand(self, node, jid=None):
		if jid == None:
			jid = self.jid
		iq = IQ(self.main.client.xmlstream, "set")
		iq["to"] = jid
		command = iq.addElement("command")
		command.attributes = {"node":node, "xmlns": "http://jabber.org/protocol/commands", "action":"execute"}
		d=iq.send()
		d.addCallback(self._formRecieved)
		self.main.client.disp(iq["id"])
		log.msg("Executing command %s." % node)

	def _formRecieved(self, el):
		command = el.firstChildElement()
		self.sessionid = command["sessionid"]
		self.dialog._resetLayout()
		if command["status"] == "completed":
			dataforms.makeDataForm(
					self.dialog,
					self.dialog.ui.gridlayout2,
					command.firstChildElement()
					)
			self.dialog.ui.execute.show()
		log.msg("Executed command with sessionid %s." % self.sessionid)
