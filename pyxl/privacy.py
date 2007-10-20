#-*-coding:UTF-8-*-

from twisted.words.protocols.jabber.xmlstream import IQ

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
			items.attributes = {"action":rule.action, "order":unicode(rule.order)}
			if rule.typ and rule.value:
				item.attributes["type"] = rule.typ
				item.attributes["value"] = rule.value
			for stanza in rule.stanzas:
				item.addElement(stanza)

		self.main.on_xml(iq.toXml())
		self.main.xmlstream.send(iq)

	def addItem(self, item):
		self.items.append(item)
		self.update()
	
	def mkItem(self, action, typ = None, value = None, stanzas = [],
			order_direction = True):	# True - lowest possible (more important), False - current highest + 1 (less important)
		orders = self._getOrders()
		if order_direction:
			order = filter(lambda a: a not in orders, range(len(orders)+1))[0]
		else:
			order = orders[-1] + 1
		item = PrivacyListItem(action, order, typ, value, stanzas)
		self.addItem(item)

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

	# TODO

class Privacy:
	def __init__(self):
		self.lists = {}
