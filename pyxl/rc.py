#-*-encoding:UTF-8-*-

from xdata import *
from adhoc import Stage, CancelStage
from twisted.python import log
import os, sys

class fSetStatus(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "complete":SetStatus, "execute":SetStatus}
		self.execute = "complete"
	
		sc = self.main.client.roster['users'][self.main.client.jid.userhost()].resources[self.main.client.jid.resource]
		sshow = sc.show
		if sshow == "online":
			sshow = "available"
		show = Field("show", "list-single", self.main.tr("Show: "), options=[
			[self.main.status[status], status] for status in ["available","chat","away","xa","dnd","offline"]
				], values = [sshow])
		status = Field("status", "text-multi", self.main.tr("Status message: "), values = [sc.status or u""])
		priority = Field("priority", "text-single", self.main.tr("Priority"), values = [sc.priority])

		self.xform = Xform("form",fields=[show,status,priority]).buildElement()

class SetStatus(Stage):
	def exec_(self):
		self.status = "completed"
		self.actions = {}
		
		typ = None
		show = self.data["show"][0]
		if show =="available":
			show = None
			typ = show
			self.data["show"][0] = "online"
		if show == "offline":
			show = None
			typ = "unavailable"
		status = "\n".join(self.data["status"])
		self.main.client.sendPresence(
				typ = typ,
				show = show,
				status = status,
				priority = self.data["priority"][0],
				)
		icon = self.main.getIcon(self.data["show"][0], size="16x16")
		self.main.ui.statusButton.setIcon(self.main.getIcon(status=self.data["show"][0], size="16x16"))
		self.main.ui.showWidget.setText(status)
		
		sc = self.main.client.roster['users'][self.main.client.jid.userhost()].resources[self.main.client.jid.resource]
		sc.show = self.data["show"][0]

		for muc in self.main.client.groupchats.itervalues():
			self.main.client.sendPresence(show = unicode(show), status = unicode(self.data["status"][0]), to = '%s/%s'%(muc.jid, muc.nick))
		self.xform = Xform("result", instructions=[self.main.tr("Status changed.")]).buildElement()

class fLeaveGC(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "complete":LeaveGC, "execute":LeaveGC}
		self.execute = "complete"

		gcop = [[key, key] for key in self.main.client.groupchats.keys()]
		
		field = Field("groupchats", "list-multi", self.main.tr("Groupchats to leave: "), options=gcop)
		self.xform = Xform("form", fields=[field], title=self.main.tr("Leave groupchats"),instructions=[self.main.tr("Choose groupchats you want remote client to leave.")]).buildElement()

class LeaveGC(Stage):
	def exec_(self):
		self.status = "completed"
		self.actions = {}
		
		for gc in self.data["groupchats"]:
			tab,index=self.main.chat.findTab(gc) 
			if tab != None:
				self.main.chat.ui.chatTab.setCurrentIndex(index)
				self.main.chat.removeTab(ask=False)
		self.xform = Xform("result", instructions=[self.main.tr("Groupchats left.")]).buildElement()

class ResendFile(Stage):
	def exec_(self):
		self.status = "executing"
		self.actions = {"cancel":CancelStage, "next":ResendFile, "execute":ResendFile}
		self.execute = "next"

		files = []
		dirs = []

		if self.data == None:
			pwd = os.environ["PWD"]
		elif os.path.isdir(os.path.join(self.data["pwd"][0], self.data["file"][0])):
			if self.data["file"][0] == os.path.pardir:
				pwd = os.path.split(self.data["pwd"][0])[0]
			else:
				pwd = os.path.join(self.data["pwd"][0], self.data["file"][0])
		else:
			f = os.path.join(self.data["pwd"][0], self.data["file"][0])

			self.main.events.addFTUploadEvent(self.session.jid, [f], {f:unicode(self.main.tr("Sent via remote controlling"))})
			self.status = "completed"
			self.execute = None
			self.actions={}
			self.xform = None
			return
		for f in os.listdir(pwd):
			if os.access(os.path.join(pwd,f), os.R_OK):
				if os.path.isfile(os.path.join(pwd,f)):
					files.append([f, f])
				else:
					dirs.append(["%s%s" % (f, os.path.sep), f])
		files.sort()
		dirs.sort()
		dirs.insert(0, ["%s%s (%s)" % (os.path.pardir, os.path.sep, self.main.tr("One directory up")), os.path.pardir])
		dirs.extend(files)

		field = Field("file", "list-single", self.main.tr("Choose file or directory: "), required=True, options=dirs)
		field2 = Field("pwd", "hidden", values=[pwd])
		self.xform = Xform("form", fields=[field, field2], title=self.main.tr("Resend file"),instructions=[self.main.tr("Choose file you want to resend from remote system or directory you want to browse."),"PWD: %s" % pwd]).buildElement()

