from PyQt4 import QtCore, QtGui
from rostertooltip_ui import *
import weakref
import vcardeditor

class ToolTip(QtGui.QFrame):
	def __init__(self, roster):
		QtGui.QFrame.__init__(self, None, QtCore.Qt.ToolTip | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
		self.setFrameStyle(QtGui.QFrame.Plain|QtGui.QFrame.Box)
		self.ui = Ui_RosterToolTip()
		self.ui.setupUi(self)
		self.setMouseTracking(True)
		self.ui.status.setAutoFillBackground(True)
		p = QtGui.QPalette()
		p.setColor(QtGui.QPalette.Base, QtGui.QColor(self.palette().window().color()))
		self.ui.status.setPalette(p)
		self.roster = weakref.ref(roster)
		self.focus = False
		self.ui.mood.setMouseTracking(True)
		self.ui.mood.enterEvent = self.moodEnterEvent
		self.ui.mood.leaveEvent = self.moodLeaveEvent
		self.ui.activity.setMouseTracking(True)
		self.ui.activity.enterEvent = self.activityEnterEvent
		self.ui.activity.leaveEvent = self.moodLeaveEvent
		self.ui.tune.setMouseTracking(True)
		self.ui.tune.enterEvent = self.tuneEnterEvent
		self.ui.tune.leaveEvent = self.tuneLeaveEvent
		self.status = ""
		self.mood = ""
		self.activity = ""
		self.tune = ""
		self.ui.vcard.setPixmap(QtGui.QPixmap("images/16x16/categories/v-card.png"))
		self.ui.vcard.leaveEvent = self.tuneLeaveEvent
		self.ui.vcard.enterEvent = self.vcardEnterEvent
		self.ui.vcard.mousePressEvent = self.vcardMousePressEvent
		self.ui.status.setMaximumHeight(QtGui.QFontMetrics(self.ui.status.font()).height()*4)
		self.ui.metaWidget.hide()
		self.mlayout = QtGui.QHBoxLayout(self.ui.metaWidget)
		self.mlayout.setMargin(0)
		self.mlayout.setSpacing(0)

	def hideMetaContacts(self):
		for i in range(self.mlayout.count()):
			item = self.mlayout.itemAt(0)
			if item.widget():
				item.widget().setParent(None)
			else:
				self.mlayout.removeItem(item)
			#item.widget().deleteLater()
			#w=item.widget()
			#del w
			#item.deleteLater()
			#del item
		self.ui.metaWidget.hide()

	def showMetaContacts(self,meta):
		self.mlayout.addStretch()
		for item in meta:
			widget = QtGui.QLabel(self.ui.metaWidget)
			widget.setMouseTracking(True)
			widget.setCursor(QtCore.Qt.PointingHandCursor)
			widget.setPixmap(self.roster().main.getIcon(item, status=unicode('online'), size="16x16").pixmap(16,16))
			widget.leaveEvent = self.tuneLeaveEvent
			def gen_enterEvent(item):
				def enterEvent(event):
					self.ui.jid.setText(item)
				return enterEvent
			def gen_mousePressEvent(item):
				def mousePressEvent(event):
					if event.button() == QtCore.Qt.RightButton:
						it = self.roster().getUserItems(item)
						if len(it) == 0:
							it = self.roster().getMetaItems(item)
							it = it[0][0]
						else:
							it = it[0]
						group = it.group
						jid = it.jid
						#if self.main.client.roster['users'].has_key(jid):
						contactMenu = self.roster().buildContactMenu(unicode(jid), group)
						#contactMenu.move(event.globalX(),event.globalY())
						contactMenu.popup(QtCore.QPoint(event.globalX(), event.globalY()))
					else:
						self.roster().openChat(item)
				return mousePressEvent
			widget.enterEvent = gen_enterEvent(item)
			widget.mousePressEvent = gen_mousePressEvent(item)
			self.mlayout.addWidget(widget)
		self.ui.metaWidget.show()

	def vcardMousePressEvent(self, event):
		self.roster().ve = vcardeditor.vcardEditorDialog(self.roster().main, self.jid, self.roster().main, False)
		self.roster().ve.show()
		self.hide()

	def vcardEnterEvent(self, event):
		self.ui.jid.setText(self.tr("Show VCard"))

	def tuneEnterEvent(self, event):
		self.ui.jid.setText(self.tune)

	def tuneLeaveEvent(self, event):
		self.ui.jid.setText(self.jid)

	def activityEnterEvent(self, event):
		self.ui.jid.setText(self.activity)

	def moodEnterEvent(self, event):
		self.ui.jid.setText(self.mood)

	def moodLeaveEvent(self, event):
		self.ui.jid.setText(self.jid)

	def enterEvent(self, event):
		self.focus = True
