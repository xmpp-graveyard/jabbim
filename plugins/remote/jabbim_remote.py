#!/usr/bin/env python
import sys, xmlrpclib, traceback

def handleuri(argv):
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
	print 'unknown command'
