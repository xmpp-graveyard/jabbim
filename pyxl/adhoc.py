#-*-coding:UTF-8-*-

from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish.domish import Element
#from xdata import *

def x2dict(x):
	if x["type"] != "submit":
		return
	data = {}
	for field in x.elements():
		if field.name != "field":
			continue
		values = []
		for value in field.elemens():
			if value.name != "value":
				continue
			values.append(unicode(value))
		data[filed["var"]] = [values, filed["type"]]
	return data

class Stage:
	def __init__(self, main, session, data = None, xmllang=None):
		self.main = main
		self.session = session
		self.data = data
		self.xmllang=xmllang

		self.xform = None
		self.status = None
		self.actions = {"cancel":CancelStage} # "action":StageClass
		self.execute = None

	def exec_(self):
		pass # Definovat v subclass

	def send(self):
		iq = IQ(self.main.client.xmlstream, "result")
		iq["to"] = self.session.jid
		command = iq.addElement("command")
		command.attributes = {
				"xmlns":"http://jabber.org/protocol/commands",
				"sessionid":self.session.sessionid,
				"node":self.session.node,
				"status":self.status
				}
		actions = command.addElement("actions")
		if self.execute:
			actions["execute"] = self.execute
		for action in self.actions.keys():
			if action != "cancel":
				actions.addElement(action)
		if self.xform:
			command.addChild(self.xform)
		
		self.session.addCallbackStages(self.actions)
		iq.send()
		self.main.client.disp(iq["id"])

class CancelStage(Stage):
	def exec_(self):
		self.status = "cancelled"
		self.session.sessionEnded()

class Session:
	def __init__(self, main, node, firststage, jid, sessionid):
		self.main	= main
		#self.client	= main.client
		self.node	= unicode(node)
		#self.name	= unicode(name)
		self.stages	= stages	# list of classes (not instances)
		self.jid 	= unicode(jid)
		#self.firststage	= firstage

		self.sessionid	= sessionid
		self.nextstages = {}

		self.execStage(firststage)

	def execStage(self, stageC, data = None, xmllang=None):
		stage = stageC(self, data, xmllang)
		stage.exec_()
		stage.send()

	def addCallbackStages(self, stages):
		self.nextages = stages

	def _recieved(self, el):
		command = el.firstChildElement()
		try:
			action = command.attributes["action"]
		except KeyError:
			action = "execute"
		try:
			xmllang = command.attributes["xml:lang"]
		except KeyError:
			xmllang = None
		x = command.firstChildElement()
		data = x2dict(x)
		self.execStage(self.nextstages[action], data, xmllang)

	def sessionEnded(self):
		del self.main.client.commands.sessions[self.sessionid]

class Commands:
	def __init__(self, main):
		self.sessions = []
		self.nodes = {}
		self.sessionids = 0
		self.main = main

	def registerNode(self, name, desc, firststage, jid = None):
		if jid == None:
			jid = unicode(self.main.client.jid.full())
		self.nodes["name"] = [desc, firststage, jid]

	def startSession(self, node, jid):
		self.sessionids += 1
		self.sessions[self.sessionids] = Session(self.main, node, self.nodes[node][1], jid, unicode(self.sessionids))

	def commandsList(self, el):
		self.main.client.disp(el["id"])
		iq = IQ(self.main.client.xmlstream, "result")
		iq["id"] = el["id"]
		iq["to"] = el["from"]
		query = iq.addElement("query", "http://jabber.org/protocol/disco#items")
		query["node"] = "http://jabber.org/protocol/commands"
		for node in self.nodes.keys():
			item = query.addElement("item")
			item["node"] = node
			item["jid"] = self.nodes[node][2]
		iq.send()
		self.main.client.disp(iq["id"])
