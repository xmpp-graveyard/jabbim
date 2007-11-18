#-*-coding:UTF-8-*-

from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.words.xish.domish import Element
from twisted.python import log
#from xdata import *

def x2dict(x):
	if not x:
		log.msg("Not x")
		return
	if x["type"] != "submit":
		log.msg('Not type="submit"')
		return
	data = {}
	log.msg(x.toXml())
	for field in x.elements():
		values = []
		if field.name != "field":
			continue
		for value in field.elements():
			if value.name != "value":
				continue
			values.append(unicode(value))
		data[field["var"]] = values 
	return data

class Stage:
	def __init__(self, main, id, session, data = None, xmllang=None):
		self.main = main
		self.session = session
		self.data = data
		self.xmllang=xmllang

		self.xform = None
		self.status = None
		self.actions = {"cancel":CancelStage} # "action":StageClass
		self.execute = None
		self.id = id

		log.msg("__init__ stage %s; data %s" % (id, data))

	def exec_(self):
		pass # Definovat v subclass

	def send(self):
		iq = IQ(self.main.client.xmlstream, "result")
		iq["to"] = self.session.jid
		iq["id"] = self.id
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
		log.msg("Sent stage %s" % self.id)
#		self.main.client.disp(iq["id"])

class CancelStage(Stage):
	def exec_(self):
		self.status = "cancelled"
		self.session.sessionEnded()
		log.msg("Stage cancelled")

class Session:
	def __init__(self, main, node, firststage, jid, sessionid, fid):
		self.main	= main
		self.node	= unicode(node)
		self.jid 	= unicode(jid)

		self.sessionid	= sessionid
		self.nextstages = {}

		self.execStage(firststage, fid)
		log.msg("Starting session %s" % self.sessionid)

	def execStage(self, stageC, id, data = None, xmllang=None):
		stage = stageC(self.main, id, self, data, xmllang)
		stage.exec_()
		log.msg("Executing stage")
		stage.send()
		log.msg("Stage executed")

	def addCallbackStages(self, stages):
		self.nextstages = stages

#	def _recieved(self, el):
#		command = el.firstChildElement()
#		try:
#			action = command.attributes["action"]
#		except KeyError:
#			action = "execute"
#		try:
#			xmllang = command.attributes["xml:lang"]
#		except KeyError:
#			xmllang = None
#		x = command.firstChildElement()
#		data = x2dict(x)
#		self.execStage(self.nextstages[action], data, xmllang)

	def sessionEnded(self):
		del self.main.client.commands.sessions[self.sessionid]

class Commands:
	def __init__(self, main):
		self.sessions = {}
		self.nodes = {}
		self.sessionids = 0
		self.main = main

	def registerNode(self, name, desc, firststage, jid = None, public=False):
		if jid == None:
			jid = unicode(self.main.client.jid.full())
		self.main.client.registerFeature("http://jabber.org/protocol/commands", name, identity={"category":"automation","type":"command-node","name":desc})
		self.main.client.registerFeature("jabber:x:data", name)
		self.main.client.discoitems["http://jabber.org/protocol/commands"].append({"jid":jid,"name":desc,"node":name})
		self.main.client.discoitems[name] = []
		self.nodes[name] = [desc, firststage, jid, public]

	def startSession(self, node, jid, fid):
		self.sessionids += 1
		self.sessions[unicode(self.sessionids)] = Session(self.main, node, self.nodes[node][1], jid, unicode(self.sessionids), fid)

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
			item["name"] = self.nodes[node][0]
			item["jid"] = self.nodes[node][2]
		iq.send()
		self.main.client.disp(iq["id"])
