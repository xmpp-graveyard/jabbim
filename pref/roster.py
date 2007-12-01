class preferences:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['rosterMode']={'type':'boolean-radio','label':'','value':'normal','options':{},'groupbox':self.main.tr('Roster style')}
		self.config['rosterMode']['options']={'normal':self.main.tr('Normal'),'compact':self.main.tr('Compact')}
		self.config['showTransports']={'type':'boolean','label':self.main.tr('Show transports'),'value':'False'}
		self.config['__sort__']=['rosterMode','showTransports']