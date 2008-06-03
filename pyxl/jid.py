from twisted.words.protocols.jabber import jid
InvalidFormat = jid.InvalidFormat

def JID(jidstring):
	try:
		j =  jid.internJID(jidstring.strip())
	except:
			raise InvalidFormat
	return j
