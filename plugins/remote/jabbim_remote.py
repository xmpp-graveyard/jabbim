#!/usr/bin/env python
import sys, xmlrpclib, traceback
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-u","--uri", dest="uri", metavar="XMPP-URI", help="Execute xmpp uri (see RFC 4622)", type="str")
options, args = parser.parse_args()

def handleuri(argv):
	print 'handle uri!'
	print argv
	if not argv[0].startswith('xmpp:'):
		return 'wrong uri'
	uri = ' '.join(argv)[5:]
	parts = uri.split('?', 1)
	if len (parts) == 1:
		return server.startChat(parts[0])
	elif parts[1] == 'join':
		return server.joinMUC(parts[0])
		
functions = {'uri': handleuri}#, 'setStatus':setStatus}
server = xmlrpclib.Server('http://localhost:7080/')

if functions.has_key(sys.argv[1]):
	try:	
		print functions[sys.argv[1]](sys.argv[2:])
	except:
		print 'error in command: ', sys.argv[1]
		print traceback.format_exc()
else:
	print	handleuri(sys.argv[1:])
