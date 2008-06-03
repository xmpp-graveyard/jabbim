from twisted.words.protocols.jabber import jid

def JID(jidstring):
	return jid.internJID(jidstring)
