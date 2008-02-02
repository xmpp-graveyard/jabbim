class preferences:
	def __init__(self,preferencesWindow):
		self.config={}
		self.config['rosterMode']={'type':'boolean-radio','label':'','value':'normal','options':{},'groupbox':preferencesWindow.tr('Roster style')}
		self.config['rosterMode']['options']={'normal':preferencesWindow.tr('Normal'),'compact':preferencesWindow.tr('Compact')}
		self.config['showTransports']={'type':'boolean','label':preferencesWindow.tr('Show transports'),'value':'False'}
		self.config['bigOnClick']={'type':'boolean','label':preferencesWindow.tr('Display user info on click'),'value':'True'}
		self.config['__sort__']=['rosterMode','showTransports','bigOnClick']