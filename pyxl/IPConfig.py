"""
IPConfig - finds out about DNS servers configured in Windows
Copyright (C) 2007  Michal "michich" Schmidt <mschmidt@redhat.com>

The registry keys were found in James Macfarlane's Win32::IPConfig CPAN module.

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
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import _winreg

class Adapter:
	def __init__(self, hklm, nicname):
		card_key = _winreg.OpenKey(hklm, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\NetworkCards\\%s" % nicname)
		(self.id, type) = _winreg.QueryValueEx(card_key, "ServiceName")
		self.tcpip_params_key = _winreg.OpenKey(hklm, "SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\\%s" % self.id)
		(self.dhcp_enabled, type) = _winreg.QueryValueEx(self.tcpip_params_key, "EnableDHCP")
		(nameserver, type) = _winreg.QueryValueEx(self.tcpip_params_key, "NameServer")
		self.nameservers = nameserver.replace(',',' ').split(' ')

		if nameserver == '' and self.dhcp_enabled:
			try:
				(nameserver, type) = _winreg.QueryValueEx(self.tcpip_params_key, "DhcpNameServer")
				self.nameservers = nameserver.split(' ')
			except WindowsError:
				self.nameservers = []
	
	def get_dns(self):
		return self.nameservers

class IPConfig:
	def __init__(self):
		self.cards = []
		hklm = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
		cards_key = _winreg.OpenKey(hklm, r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards')
		i = 0
		try:
			while True:
				card_name = _winreg.EnumKey(cards_key, i)
				i = i + 1
				card = Adapter(hklm, card_name)
				self.cards.append(card)
		except EnvironmentError:
			pass

	def get_dns(self):
		all_dns = []
		for c in self.cards:
			all_dns = all_dns + c.get_dns()
		return all_dns
