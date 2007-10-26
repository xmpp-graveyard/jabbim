#-*-coding:UTF-8-*-

from twisted.words.protocols.jabber.xmlstream import IQ
from twisted.python import log
# iq
# | querry
# | attr: xmlns == "jabber:iq:privacy"
# |
# `--| list
#    | attr: name == string
#    |
#    `--| item
#       | attr: action == string("allow"|"deny")
#       | attr: order == unsigned unique int
#       | [attr: type == string("jid"|"group"|"subscription")]
#       | [attr: value == string]
#       |
#       `--| [message]
#       `--| [iq]
#       `--| [presence-in]
#       `--| [presence-out]

class PrivacyListItem:
	def __init__(self, action, order, typ = None, value = None, stanzas = []):
		self.action	= action
		self.order	= int(order)
		if self.order < 0:
			raise ValueError("Order must be unsigned int")
		self.typ	= typ
		self.value	= value
		self.stanzas	= stanzas # stanzas = [] denies|allows all communication

class PrivacyList:
	def __init__(self, name, items, main):
		self.name	= name
		self.items	= items
		self.main	= main
		self._reviseOrders()

		self.invisible	= None
		lastitem = self.getItem(self._getOrders()[-1])
		if lastitem.action == "deny" and (lastitem.stanzas == [] or "presence-out" in lastitem.stanzas) and lastitem.typ == None:
			self.invisible = lastitem

		for item in self.items:
			if item.value and item.typ == "jid":
				for useritem in self.main.ui.roster.getUserItems(item.value):
					useritem.block = self.isBlockedJID(item.value) and True
				

	def _getOrders(self):
		orders = [int(item.order) for item in self.items]
		orders.sort()
		return orders

	def _reviseOrders(self): # ejabberd je pyca, jednodussi prace s itemama
		orders = self._getOrders()
		while orders:
			i = orders.pop()
			if i in orders:
				self._advance(self.getItem(i), False)
				self._reviseOrders()
		self.update()

	def update(self):
		iq	= IQ(self.main.client.xmlstream, "set")
		query	= iq.addElement("query", "jabber:iq:privacy")
		list_	= query.addElement("list")
		list_.attributes = {"name": self.name}
		for rule in self.items:
			item = list_.addElement("item")
			item.attributes = {"action":rule.action, "order":unicode(rule.order)}
			if rule.typ and rule.value:
				item.attributes["type"] = rule.typ
				item.attributes["value"] = rule.value
			for stanza in rule.stanzas:
				item.addElement(stanza)

		self.main.client.on_xml(iq.toXml())
		iq.send()
		self.main.client.disp(iq["id"])

	def addItem(self, item):
		self.items.append(item)
		self.update()

	def delItem(self, item):
		if item in self.items:
			self.items.remove(item)
			self.update()

	def mkItem(self, action, typ = None, value = None, stanzas = [],
			to_zero = True):	# True - lowest possible (more important), False - current highest + 1 (less important)
		orders = self._getOrders()
		if to_zero:
			zitem = self.getItem(0)
			if zitem:
				self._advance(zitem, False)
			order = 0
		else:
			order = orders[-1] + 1
		item = PrivacyListItem(action, order, typ, value, stanzas)
		self.addItem(item)
		return item

	def getItem(self, order):
		for item in self.items:
			if item.order == order:
				return item

	def _advance(self, item, update=True):
		orders = self._getOrders()
		to_advance = None
		if item.order + 1 in orders:
			to_advance = self.getItem(item.order + 1)
		item.order += 1
		if to_advance:
			self._advance(to_advance)
		if update:
			self.update()
			
	def changeOrder(self, old, new):
		orders = self._getOrders()
		item = getItem(old)
		if new in orders:
			self._advance(self.getItem(new))
		item.order = new
	
	######## ^   BASE   ^ #######
	######## v ADVANCED v #######
	
	#def _getScheme(self):
	#	for item in self.items:
	#		r += "Action: %s;" % item.action
	#		r += "Order: %s;" % item.order
	#		if item.typ:
	#			r += "Type: %s;" % item.typ
	#			r += "Value: %s;" % item.value
	#		r += "Stanzas: "+", ".join(item.stanzas) or "Stanzas: All"
	#		r += "\n"
	#		return r
	# TODO
	def isBlockedJID(self, jid):
		r = False
		order = None
		for item in self.items:
			item.stanzas.sort()
			if item.typ == "jid" and item.value == jid and item.action == "deny" and  (item.stanzas == [] or item.stanzas == ["iq","message","presence-out"]):
				r = item
				order = item.order

			if	(item.typ == "jid" and item.value == jid) and (item.action == "allow" and item.order < order) and (item.stanzas == [] or item.stanzas == ["iq","message","presence-out"]):
				r = False
		return r

	def blockJID(self, jid): # Block all communication
		self.mkItem("deny", "jid", jid)#, ["message", "iq", "presence-out"])
		for x in self.main.ui.roster.getUserItems(jid.split("/", 1)[0]):
			x.privacy["block"] = True

	def unBlockJID(self, jid):
		item = self.isBlockedJID(jid)
		if item:
			self.delItem(item)
		for x in self.main.ui.roster.getUserItems(jid.split("/", 1)[0]):
			x.privacy["block"] = False
	

	def isAllowedJID(self, jid):
		r = False
		order = None
		for item in self.items:
			if item.typ == "jid" and item.value == jid and item.action == "allow" and (item.stanzas == [] or "presence-out" in item.stanzas):
				r = item
				order = item.order
			if	(item.typ == "jid" and item.value == jid) and (item.action == "deny" and item.order < order) and (item.stanzas == [] or "presence-out" in item.stanzas):
				r = False
		return r

	def allowJID(self, jid): 
		self.mkItem("allow", "jid", jid, ["presence-out"])
		for x in self.main.ui.roster.getUserItems(jid.split("/", 1)[0]):
			x.privacy["allow"] = True

	def disAllowJID(self, jid):
		item = self.isAllowedJID(jid)
		log.msg("isAllowedJID(%s): %s" % (jid,str(item)))
		if item:
			self.delItem(item)
		for x in self.main.ui.roster.getUserItems(jid.split("/", 1)[0]):
			x.privacy["allow"] = False

	def setInvisible(self):
		self.invisible = self.mkItem("deny", stanzas = ["presence-out"], to_zero = False)
	def unsetInvisible(self):
		self.delItem(self.invisible)
		self.invisible = None

	
class Privacy:
	def __init__(self, main):
		self.main	= main
		self.lists	= {}
		self.active	= None
		self.default	= None
	
	def setActive(self, name):
		if name not in self.lists.keys() and name != None:
			self.lists[name] = None
		iq = IQ(self.main.client.xmlstream, "set")
		query = iq.addElement("query", "jabber:iq:privacy")
		active = query.addElement("active")
		if name != None:
			active.attributes = {"name":name}
		iq.send()
		self.main.client.on_xml(iq.toXml())
		self.main.client.disp(iq["id"])
		if name != None:
			self.active = self.lists[name]	
		else:
			self.active = None

	def setDefault(self, name):
		if name not in self.lists.keys() and name != None:
			self.lists[name] = None
		iq = IQ(self.main.client.xmlstream, "set")
		query = iq.addElement("query", "jabber:iq:privacy")
		default = query.addElement("default")
		if name != None:
			default.attributes = {"name":name}
		iq.send()
		self.main.client.on_xml(iq.toXml())
		self.main.client.disp(iq["id"])
		if name != None:
			self.default = self.lists[name]
		else:
			self.default = None
