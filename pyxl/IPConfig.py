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
	def __init__(self, interfaces_key, nic_uuid):
		try:
			tcpip_params_key = _winreg.OpenKey(interfaces_key, nic_uuid)
			(dhcp_enabled, type) = _winreg.QueryValueEx(tcpip_params_key, "EnableDHCP")
			(nameserver, type) = _winreg.QueryValueEx(tcpip_params_key, "NameServer")
			self.nameservers = nameserver.replace(',',' ').split(' ')

			if nameserver == '' and dhcp_enabled:
				(nameserver, type) = _winreg.QueryValueEx(tcpip_params_key, "DhcpNameServer")
				self.nameservers = nameserver.split(' ')
		except WindowsError:
			self.nameservers = []
	
	def get_dns(self):
		return self.nameservers

class IPConfig:
	def __init__(self):
		self.cards = []
		hklm = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
		interfaces_key = _winreg.OpenKey(hklm, r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces')
		i = 0
		try:
			while True:
				nic_uuid = _winreg.EnumKey(interfaces_key, i)
				i = i + 1
				card = Adapter(interfaces_key, nic_uuid)
				self.cards.append(card)
		except EnvironmentError:
			pass

	def get_dns(self):
		all_dns = []
		for c in self.cards:
			all_dns = all_dns + c.get_dns()
		return all_dns
