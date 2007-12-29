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
			(nameserver, type) = _winreg.QueryValueEx(self.tcpip_params_key, "DhcpNameServer")
			self.nameservers = nameserver.split(' ')	

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
