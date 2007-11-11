#-*-encoding:UTF-8-*-

from xdata import *
from adhoc import Stage, CancelStage

class fSetStatus(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "complete":SetStatus}
		self.execute = "complete"
		
		status = Field("status", "text-single", self.main.tr("Status message: "))
		self.xform = Xform("form",fields=[status]).buildElement()

class SetStatus(Stage):
	pass
