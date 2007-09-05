"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
from twisted.python import log
import traceback

class EventDispatcher:
	def __init__(self, prefix="event_"):
		self.prefix = prefix
		self.callbacks = {}


	def registerHandler(self, name, meth, hname = 'nic', priority = 5):
		self.callbacks.setdefault(name, {})[hname] = {'method':meth, 'prio':priority}
	
	def unregisterHandler(self, name, hname):
		try:
			del self.callbacks[name][hname]
		except:
			pass

	def publishEvent(self, name, *args, **kwargs):
		if self.callbacks.has_key(name):
			seznam = self.callbacks[name].itervalues()
			serazeno = sorted(seznam, key = self.k)
			for cb in serazeno:
				try:
					vysl = cb['method'](*args, **kwargs)
					if vysl == False:
						return
				except Exception, ex:
					log.msg('Plugin error: ' +unicode(ex))
					traceback.print_exc()
	
	def k(self, key):
		return key['prio']
