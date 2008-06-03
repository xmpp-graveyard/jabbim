from twisted.words.protocols.jabber import jid
import copy
InvalidFormat = jid.InvalidFormat

def JID(jidstring):
	try:
		j =  jid.internJID(jidstring.strip())
	except:
			raise InvalidFormat
			return
	return copy.copy(j)
