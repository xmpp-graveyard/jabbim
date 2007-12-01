class preferences:
	def __init__(self,main):
		self.main=main
		self.config={}
		self.config['saveGeometry']={'type':'boolean','label':self.main.tr("Save Jabbim position on close"),'value':'1'}