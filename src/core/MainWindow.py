'''
Created on 16.4.2010

@author: sef
'''
from PyQt4 import QtGui, QtCore
import widgets
from widgets.avatarLoader import AvatarLabel
from include import utils, safelog, userrating, rot13
#from utils import *
import wizards
from twisted.internet import reactor, threads
import os
from include.constants import RESOURCEPATH
from widgets import bookmarks, aboutDialog, avatarLoader
from twisted.python import log
from configobj import ConfigObj, ConfigObjError
import sys
from pyxl import storage
from genericpath import isfile
from twisted.web.microdom import parseString, Element
import random
import traceback
from twisted.internet.defer import DeferredList
from locale import strcoll

import gc
from widgets.scrollbar import scrollBar
from twisted.web.client import downloadPage
import re
import time
from pyxl import jid as jidT
from core.clientClass import clientClass
from imp import load_source
from urllib import quote, unquote
from os.path import basename,dirname, isfile

class mainWindow(QtGui.QMainWindow):
	def __init__(self,parent=None, app = None):
		apply(QtGui.QMainWindow.__init__,(self,parent))

		self.ui=widgets.mainWindow.Ui_MainWindow()
		self.ui.setupUi(self)
#		self.ui.Form.setWidget(self.ui.scrollAreaWidgetContents)
#		self.ui.Form.setWidgetResizable(True)
		self.setObjectName("Jabbim class")
		#self.setWindowFlags(QtCore.Qt.Tool)#|QtCore.Qt.FramelessWindowHint)
		#self.ui.toggleInvisible.hide()
		#self.ui.statusButton.hide()
		self.qtStyles=map(unicode,list(QtGui.QStyleFactory.keys()))
		self.qtStylesDefault=app.style()
		app.main=self
		layout=QtGui.QHBoxLayout(self.ui.selfAvatarWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.selfAvatar=AvatarLabel(self,self.ui.selfAvatarWidget)
		layout.addWidget(self.ui.selfAvatar)
		self.setAttribute(QtCore.Qt.WA_AlwaysShowToolTips,True)
		self.utils=utils
		self.app=app
		self.selfAvatar=None #: current avatar (QPixmap or None)
		self.selfStatus="" #: current show (string according to self.shows)
		self.log=None
		self.plugins = {}
		self.config=None #: config dict (loaded by configObj)
		self.cache=None
		self.connectStarted=0
		self.senddialog = None
		self.snarlMessages={}
		self.autoAdd={}
		self.version = '0.6 SVN' + utils.getSvnVersion() #: version string
		#self.setWindowOpacity (0.5)
		self.imageId=0
		self.isJabbimUser=False
		self.jabbimServers = ['jabbim.cz','jabbim.sk','jabbim.pl','jabbim.com','jabber.cz','njs.netlab.cz']

		QtCore.QObject.connect(app, QtCore.SIGNAL("sleep()"),self.systemSleep)
		QtCore.QObject.connect(app, QtCore.SIGNAL("wakeUp()"),self.systemWakeUp)

		# get homedir
		self.homeDir=utils.getHomeDir() #: Jabbim home directory + profile directory
		self.realHomeDir=unicode(self.homeDir) #: Jabbim home directory

		# check if there is existing profile
		profiles=utils.getProfiles(self.realHomeDir)
		if len(profiles)==0:
			self.startwiz=wizards.firststart.firstStartWizard(self,self)
			self.startwiz.show()

		self.reactor=reactor
		# load last profile according to ~/config
		utils.loadConfig(self,[])
		if not self.config['jid']+"-profile" in profiles:
			if len(profiles)!=0:
				self.homeDir=self.realHomeDir+"/"+profiles[0]
				utils.loadConfig(self,[])
			else:
				os.remove(self.realHomeDir+'/config')
				utils.loadConfig(self,[])
		else:
			self.homeDir=self.realHomeDir+"/"+self.config['jid']+"-profile"
			utils.loadConfig(self,[])

		self.loadThemePackage()
		self.loadRoster() # load roster widget
		self.loadRosterStyle()
		QtCore.QObject.connect(self.ui.rosterSearch, QtCore.SIGNAL(" textEdited ( const QString & )"),self.ui.roster.search)
		QtCore.QObject.connect(self.ui.rosterSearchClose, QtCore.SIGNAL("clicked()"),self.ui.roster.search)


		#self.ui.mainTabWidget.showTab=self.t
		self.ui.tabWidgetButton=QtGui.QToolButton(self.ui.mainTabWidget)
		self.ui.tabWidgetButton.setObjectName("jabbimButton")
		self.ui.tabWidgetButton.setIcon(QtGui.QIcon(RESOURCEPATH+"images/16x16/categories/transports.png"))
		self.ui.tabWidgetButton.setCheckable(True)
		#self.ui.tabWidgetButton.setMinimumSize(QtCore.QSize(29,29))
		QtCore.QObject.connect(self.ui.tabWidgetButton, QtCore.SIGNAL("toggled(bool)"), self.showTransportsWidget)
		#self.ui.tabWidgetButton.setPopupMode(QtGui.QToolButton.InstantPopup)
		#self.ui.tabWidgetButton.setArrowType(QtCore.Qt.NoArrow)
		self.ui.mainTabWidget.setCornerWidget(self.ui.tabWidgetButton)
		self.ui.tabWidgetButton.hide()

		# look & feel :)
		self.ui.gridlayout.setMargin(1)
		self.ui.gridlayout.setSpacing(1)
		self.ui.mainTabWidget.setTabText(0,"")
		self.ui.mainTabWidget.setTabText(1,"")
		self.ui.mainTabWidget.setTabText(2,"")
		self.ui.mainTabWidget.setTabText(3,"")
		self.ui.mainTabWidget.setTabText(4,"")
		self.ui.actionAdd_Contact.setEnabled(False)
		self.ui.actionJoin_groupchat.setEnabled(False)
		self.ui.actionService_Discovery.setEnabled(False)
		self.ui.actionStart_Chat.setEnabled(False)
#		self.ui.actionPrivacy_list_editor.setEnabled(False)
		self.ui.actionPrivacy_list_editor.setVisible(False)
		self.ui.actionIdentity.setEnabled(False)
		self.ui.registerButton.hide()
		self.ui.groupStyleWidget.hide()
		self.ui.userStyleWidget.hide()
		self.ui.selectedItemStyle.hide()
		#self.setMinimumWidth(200)
		self.ui.statusLine.hide()
		self.ui.statusLine.paintEvent=self.statusLinePaintEvent
		self.ui.statusLine.typ="statusChange"
		self.ui.statusLine.defaultText=unicode(self.tr("Enter status message"))
		self.ui.transportsWidget.l=QtGui.QHBoxLayout(self.ui.transportsWidget)
		self.ui.transportsWidget.l.setContentsMargins(0,0,0,0)
		self.ui.transportsToolbar=QtGui.QToolBar(self.ui.transportsWidget)
		self.ui.transportsToolbar.setIconSize(QtCore.QSize(16,16))
		self.ui.transportsWidget.layout().addWidget(self.ui.transportsToolbar)
		self.ui.transportsWidget.l.addStretch()
		self.ui.transportsWidget.button=QtGui.QToolButton(self.ui.transportsWidget)
		self.ui.transportsWidget.button.setPopupMode(QtGui.QToolButton.InstantPopup)
		self.ui.transportsWidget.button.setArrowType(QtCore.Qt.DownArrow)
		self.ui.transportsWidget.button.setMenu(self.ui.menuPlugins)
		self.ui.pluginsToolbar=QtGui.QToolBar(self.ui.transportsWidget)
		self.ui.pluginsToolbar.setIconSize(QtCore.QSize(16,16))
		self.ui.transportsWidget.layout().addWidget(self.ui.pluginsToolbar)
		self.ui.transportsWidget.layout().addWidget(self.ui.transportsWidget.button)

		#self.ui.bookmarks.setIndentation(0)

		# filetransfer
		#self.filetransferTimer=QtCore.QTimer()
		#QtCore.QObject.connect(self.filetransferTimer, QtCore.SIGNAL("timeout()"),self.refreshFT)
		self.filetransferDescriptions={}
		self.ftError={}
		self.filetransfer={}
		self.filetransferQueue={}
		self.allowedSids={}
		self.allowedJids={} # {jid:path_to_download_files}

		self.bookmarks=bookmarks.bookmarksClass(self.ui.bookmarks,self)

		# preparing chat window
		if self.config['oneWindow']=="True":
			self.workspace=QtGui.QWorkspace(self.ui.mdiWidget)
			layout=QtGui.QHBoxLayout(self.ui.mdiWidget)
			layout.addWidget(self.workspace)
			self.chat=widgets.chatwindow.chatWindow(self.workspace,self)
			self.workspace.addWindow(self.chat)
			self.chat.showMaximized() #: chat window
		else:
			self.ui.mdiWidget.hide()
			self.ui.mdiWidget.setParent(None)
			#self.setMaximumWidth(250)
			self.chat=widgets.chatwindow.chatWindow(self,self) #: chat window

		# variables
		self.moodIcons={}
		self.hosts={} #: {host:type_of_host}
		self.client=None #: Pyxl client instance
		self.events=widgets.events.events(self) #: events class
		self.preferencesWindow=widgets.preferences.preferencesWindow(self,self)
		self.aboutDialog = None  # will be created lazily
		self.styleSheetText=""
		self.profilesWindow=None
		self.mucbrowser=None
		self.addcontactdialog=None
		self.statusPath=RESOURCEPATH+"images/xxxxx/status/"
		self.transports={}
		self.setupShortcuts()
		self.delayedMessages = None
		#: {show:ID}
		self.shows={u"online":u"1",
					u"available":u"1",
					u"chat":u"0",
					u"away":u"3",
					u"xa":u"4",
					u"dnd":u"5",
					u"None":u"1",
					u"":u"1",
					u"offline":u"9",
					u"unavailable":u"9"
					}
		#: {ID:icon_text}
		self.icons={u"1":u"online",
					u"0":u"chat",
					u"3":u"away",
					u"4":u"xa",
					u"5":u"dnd",
					u"9":u"offline"
					}
		#: {show:translated_text}
		self.status={"online":self.tr("Online"),
					"available":self.tr("Online"),
					"chat":self.tr("Chatty"),
					"away":self.tr("Away"),
					"xa":self.tr("Extended away"),
					"dnd":self.tr("DND"),
					"None":self.tr("Online"),
					"offline":self.tr("Offline"),
					"invisible":self.tr("Invisible")
					}
		#mood:translation
		self.moods = {
					"none":self.tr("None"),
					"afraid":self.tr("afraid"),
					"amazed":self.tr("amazed"),
					"angry":self.tr("angry"),
					"annoyed":self.tr("annoyed"),
					"anxious":self.tr("anxious"),
					"aroused":self.tr("aroused"),
					"ashamed":self.tr("ashamed"),
					"bored":self.tr("bored"),
					"brave":self.tr("brave"),
					"calm":self.tr("calm"),
					"cold":self.tr("cold"),
					"confused":self.tr("confused"),
					"contented":self.tr("contented"),
					"cranky":self.tr("cranky"),
					"curious":self.tr("curious"),
					"depressed":self.tr("depressed"),
					"disappointed":self.tr("disappointed"),
					"disgusted":self.tr("disgusted"),
					"distracted":self.tr("distracted"),
					"embarrassed":self.tr("embarrassed"),
					"excited":self.tr("excited"),
					"flirtatious":self.tr("flirtatious"),
					"frustrated":self.tr("frustrated"),
					"grumpy":self.tr("grumpy"),
					"guilty":self.tr("guilty"),
					"happy":self.tr("happy"),
					"hot":self.tr("hot"),
					"humbled":self.tr("humbled"),
					"humiliated":self.tr("humiliated"),
					"hungry":self.tr("hungry"),
					"hurt":self.tr("hurt"),
					"impressed":self.tr("impressed"),
					"in_awe":self.tr("in_awe"),
					"in_love":self.tr("in_love"),
					"indignant":self.tr("indignant"),
					"interested":self.tr("interested"),
					"intoxicated":self.tr("intoxicated"),
					"invincible":self.tr("invincible"),
					"jealous":self.tr("jealous"),
					"lonely":self.tr("lonely"),
					"mean":self.tr("mean"),
					"moody":self.tr("moody"),
					"nervous":self.tr("nervous"),
					"neutral":self.tr("neutral"),
					"offended":self.tr("offended"),
					"playful":self.tr("playful"),
					"proud":self.tr("proud"),
					"relieved":self.tr("relieved"),
					"remorseful":self.tr("remorseful"),
					"restless":self.tr("restless"),
					"sad":self.tr("sad"),
					"sarcastic":self.tr("sarcastic"),
					"serious":self.tr("serious"),
					"shocked":self.tr("shocked"),
					"shy":self.tr("shy"),
					"sick":self.tr("sick"),
					"sleepy":self.tr("sleepy"),
					"stressed":self.tr("stressed"),
					"surprised":self.tr("surprised"),
					"thirsty":self.tr("thirsty"),
					"worried":self.tr("worried")
		}
		self.moodActions = {}
		self.activities = {
					"none":self.tr("None"),
					"buying_groceries":self.tr("buying_groceries"),
					"cleaning":self.tr("cleaning"),
					"cooking":self.tr("cooking"),
					"doing_maintenance":self.tr("doing_maintenance"),
					"doing_the_dishes":self.tr("doing_the_dishes"),
					"doing_the_laundry":self.tr("doing_the_laundry"),
					"gardening":self.tr("gardening"),
					"running_an_errand":self.tr("running_an_errand"),
					"walking_the_dog":self.tr("walking_the_dog"),
					"having_a_beer":self.tr("having_a_beer"),
					"having_coffee":self.tr("having_coffee"),
					"having_tea":self.tr("having_tea"),
					"having_a_snack":self.tr("having_a_snack"),
					"having_breakfast":self.tr("having_breakfast"),
					"having_dinner":self.tr("having_dinner"),
					"having_lunch":self.tr("having_lunch"),
					"cycling":self.tr("cycling"),
					"hiking":self.tr("hiking"),
					"jogging":self.tr("jogging"),
					"playing_sports":self.tr("playing_sports"),
					"running":self.tr("running"),
					"skiing":self.tr("skiing"),
					"swimming":self.tr("swimming"),
					"working_out":self.tr("working_out"),
					"at_the_spa":self.tr("at_the_spa"),
					"brushing_teeth":self.tr("brushing_teeth"),
					"getting_a_haircut":self.tr("getting_a_haircut"),
					"shaving":self.tr("shaving"),
					"taking_a_bath":self.tr("taking_a_bath"),
					"taking_a_shower":self.tr("taking_a_shower"),
					"day_off":self.tr("day_off"),
					"hanging_out":self.tr("hanging_out"),
					"on_vacation":self.tr("on_vacation"),
					"scheduled_holiday":self.tr("scheduled_holiday"),
					"sleeping":self.tr("sleeping"),
					"gaming":self.tr("gaming"),
					"going_out":self.tr("going_out"),
					"partying":self.tr("partying"),
					"reading":self.tr("reading"),
					"rehearsing":self.tr("rehearsing"),
					"shopping":self.tr("shopping"),
					"socializing":self.tr("socializing"),
					"sunbathing":self.tr("sunbathing"),
					"watching_tv":self.tr("watching_tv"),
					"watching_a_movie":self.tr("watching_a_movie"),
					"in_real_life":self.tr("in_real_life"),
					"on_the_phone":self.tr("on_the_phone"),
					"on_video_phone":self.tr("on_video_phone"),
					"commuting":self.tr("commuting"),
					"cycling":self.tr("cycling"),
					"driving":self.tr("driving"),
					"in_a_car":self.tr("in_a_car"),
					"on_a_bus":self.tr("on_a_bus"),
					"on_a_plane":self.tr("on_a_plane"),
					"on_a_train":self.tr("on_a_train"),
					"on_a_trip":self.tr("on_a_trip"),
					"walking":self.tr("walking"),
					"coding":self.tr("coding"),
					"in_a_meeting":self.tr("in_a_meeting"),
					"studying":self.tr("studying"),
					"writing":self.tr("writing")}

		self.activityGroups = {"doing_chores":[self.tr("doing_chores"),"buying_groceries","cleaning","cooking","doing_maintenance","doing_the_dishes","doing_the_laundry","gardening","running_an_errand","walking_the_dog"],
					"drinking":[self.tr("drinking"),"having_a_beer","having_coffee","having_tea"],
					"eating":[self.tr("eating"),"having_a_snack","having_breakfast","having_dinner","having_lunch"],
					"exercising":[self.tr("exercising"),"cycling","hiking","jogging","playing_sports","running","skiing","swimming","working_out"],
					"grooming":[self.tr("grooming"),"at_the_spa","brushing_teeth","getting_a_haircut","shaving","taking_a_bath","taking_a_shower"],
					# no substate... we don't allow it<= "having_appointment":self.tr("having_appointment"),
					"inactive":[self.tr("inactive"),"day_off","hanging_out","on_vacation","scheduled_holiday","sleeping"],
					"relaxing":[self.tr("relaxing"),"gaming","going_out","partying","reading","rehearsing","shopping","socializing","sunbathing","watching_tv","watching_a_movie"],
					"talking":[self.tr("talking"),"in_real_life","on_the_phone","on_video_phone"],
					"traveling":[self.tr("traveling"),"commuting","cycling","driving","in_a_car","on_a_bus","on_a_plane","on_a_train","on_a_trip","walking"],
					"working":[self.tr("working"),"coding","in_a_meeting","studying","writing"]}

		self.offline=False
		#self.ui.showOffline.hide()
		#self.ui.offlineButton.hide()

		# signals
		QtCore.QObject.connect(self.ui.login_connect, QtCore.SIGNAL("clicked()"),self.connect)
		#QtCore.QObject.connect(self.ui.toggleInvisible, QtCore.SIGNAL("clicked(bool)"),self.toggleInvisibility)
		QtCore.QObject.connect(self.ui.registerButton, QtCore.SIGNAL("clicked ()"),self.registerButtonClicked)
		QtCore.QObject.connect(self.ui.login_cancel, QtCore.SIGNAL("clicked ()"),self.connectCancel)
		QtCore.QObject.connect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)
		QtCore.QObject.connect(self.ui.mucBrowserButton, QtCore.SIGNAL("clicked ()"),self.mucBrowser)
		QtCore.QObject.connect(self.ui.statusWidget, QtCore.SIGNAL("clicked (bool)"),self.statusMessageClicked)
		#QtCore.QObject.connect(self.ui.statusLine, QtCore.SIGNAL("returnPressed ()"),self.statusLineFinished)
		QtCore.QObject.connect(self.ui.statusLine, QtCore.SIGNAL("editingFinished () "),self.statusLineFinished)
		#QtCore.QObject.connect(self.ui.offlineButton, QtCore.SIGNAL("clicked ( bool)"),self.hideOffline)

		QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered ( bool )"),self.about)
		QtCore.QObject.connect(self.ui.actionSupport, QtCore.SIGNAL("triggered ( bool )"),self.support)
		QtCore.QObject.connect(self.ui.actionSendJabbimLog, QtCore.SIGNAL("triggered ( bool )"),self.sendLog)
#		QtCore.QObject.connect(self.ui.actionPrivacy_list_editor, QtCore.SIGNAL("triggered ( bool )"),self.privacyListEditor)
		QtCore.QObject.connect(self.ui.actionAdd_Contact, QtCore.SIGNAL("triggered ( bool )"),self.addContactMainWindow)
		QtCore.QObject.connect(self.ui.actionPreferences, QtCore.SIGNAL("triggered ( bool )"),self.preferencesClicked)
		QtCore.QObject.connect(self.ui.actionProfiles, QtCore.SIGNAL("triggered ( bool )"),self.profilesClicked)
		QtCore.QObject.connect(self.ui.actionJoin_groupchat, QtCore.SIGNAL("triggered ( bool )"),self.joinGroupchat)
		QtCore.QObject.connect(self.ui.actionBrowse_rooms, QtCore.SIGNAL("triggered ( bool )"),self.mucBrowser)
		QtCore.QObject.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered ( bool )"),self.trayQuit)
		QtCore.QObject.connect(self.ui.actionService_Discovery, QtCore.SIGNAL("triggered ( bool )"),self.serviceDiscovery)
		QtCore.QObject.connect(self.ui.actionIdentity, QtCore.SIGNAL("triggered ( bool )"),self.identityEditor)
		QtCore.QObject.connect(self.ui.actionStart_Chat, QtCore.SIGNAL("triggered ( bool )"), self.startChatDialog)
		QtCore.QObject.connect(self.ui.actionShow_offline,QtCore.SIGNAL("toggled ( bool )"), self.hideOffline)
		QtCore.QObject.connect(self.ui.actionShow_transports,QtCore.SIGNAL("toggled ( bool )"), self.showTransports)
		self.ui.actionSendJabbimLog.setVisible(False)
		QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self.ui.statusLine,self.statusLineCanceled)

		# set up stacked widget (0==login,1==roster, 2==events and etc..)
		self.ui.rosterStackedWidget.setCurrentIndex(0)

		self.loadSkin() # load chat skin
		self.loadSounds() # load chat skin
		self.loadTheme() # load theme
		self.loadMoods() # load user moods icon
		self.loadActivities() # load user moods icon
		self.ui.roster.reskin() # reskin roster
		self.selfResources=[] #: Resources which are connected from the same JID as user
		self.buildOfflineMenu() # build menu with 'show offline', 'show away'

		# open log file
		if self.config['log'] == 'true':
			logfile = open(self.homeDir + '/' + self.config['logfile'], 'w')
			self.log = safelog.SafeFileLogObserver(logfile)
			self.log.timeFormat = '%Y-%m-%d %H:%M:%S'
			log.startLoggingWithObserver(self.log.emit)

		# show tray icon
		self.tray=QtGui.QSystemTrayIcon(QtGui.QIcon(QtGui.QIcon(RESOURCEPATH+"images/16x16/apps/jabbim.png").pixmap(16,16,QtGui.QIcon.Disabled)))
		#def _event(ev):
			#print ev.type()
			#return QtGui.QSystemTrayIcon.event(self.tray,ev)
		#self.tray.event=_event

		self.app.connect(self.tray,QtCore.SIGNAL("activated (QSystemTrayIcon::ActivationReason)"),self.trayActivated)
		self.tray.show()

		# set mainwindow size and position
		w=self.config['windowGeometry'][2]
		h=self.config['windowGeometry'][3]
		if str(w)=='None' or str(h)=='None':
			if str(w)!='None':
				self.resize(int(w),self.height())
			self.move(int(self.config['windowGeometry'][0]),int(self.config['windowGeometry'][1]))
		else:
			self.setGeometry(int(self.config['windowGeometry'][0]),int(self.config['windowGeometry'][1]),int(w),int(h))
		# set chatWindow size and position
		w=self.config['chatGeometry'][2]
		h=self.config['chatGeometry'][3]
		if str(w)=='None' or str(h)=='None':
			if str(w)!='None':
				self.chat.resize(int(w),self.height())
			self.chat.move(int(self.config['chatGeometry'][0]),int(self.config['chatGeometry'][1]))
		else:
			self.chat.setGeometry(int(self.config['chatGeometry'][0]),int(self.config['chatGeometry'][1]),int(w),int(h))

		#self.setGeometry(rect.width()-250,rect.y(),250,rect.y()+rect.height())
#		self.setWindowOpacity(0.5)

		# Connect to session and system DBus if possible.
		# Code must not assume DBus is available and must limit
		# functionality gracefully if *_dbus==None.
		self.session_dbus = None
		self.system_dbus = None
		try:
			import dbus
			from dbus.mainloop.qt import DBusQtMainLoop
			DBusQtMainLoop(set_as_default=True)
			self.session_dbus = dbus.SessionBus()
			log.msg("Connected to session DBus")
			self.system_dbus = dbus.SystemBus()
			log.msg("Connected to system DBus")
		except ImportError:
			log.err("This PyQt4 does not support DBus. Perhaps install python-qt4-dbus.")
		except:
			log.err("Could not connect to session or system DBus")

		self.reconnect = True # :# True = Jabbim will reconnect after disconnect
		self.active=True

		try:
			self.avatarDef = ConfigObj(self.realHomeDir+'/avatars/avatars.def',encoding='UTF8')
		except ConfigObjError, e:
			self.avatarDef = e.config
			self.avatarDef.write()

		self.fillLoginForm()
		# load cache and create tables
		if sys.platform != 'win32':
			self.cache = storage.Cache(db=utils.path(self.homeDir+u'/cache.db'))
		else:
			self.cache = storage.Cache(db=(unicode(self.homeDir)+u'/cache.db').encode('utf8')) #hack!
		self.cache.create_tables().addCallback(self.tables_created)
		self.ui.loginStatus.addItem(self.getIcon(status="online",size="16x16"), self.status["online"],QtCore.QVariant(QtCore.QStringList(["online",  ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="chat",size="16x16"), self.status["chat"],QtCore.QVariant(QtCore.QStringList(["chat", ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="away",size="16x16"), self.status["away"],QtCore.QVariant(QtCore.QStringList(["away", ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="xa",size="16x16"), self.status["xa"],QtCore.QVariant(QtCore.QStringList(["xa", ''])))
		self.ui.loginStatus.addItem(self.getIcon(status="dnd",size="16x16"), self.status["dnd"],QtCore.QVariant(QtCore.QStringList(["dnd", ''])))

		self.emoticonsWidget=widgets.emoticonswidget.emoticonsWidget(self,self)

		#if self.config['rosterMode'] == "compact":
		#	self.ui.roster.setRosterStyle(widgets.compactrosterstyle.rosterStyle)
		#else:
#			self.ui.roster.setRosterStyle(widgets.defaultrosterstyle.rosterStyle)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		QtCore.QObject.disconnect(self.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.ui.roster.sliderChanged)

		#self.loadRosterStyle() # load roster style
		self.userRating=userrating.RatingAssigner(self)
		#disabling fav and content tabs
		self.ui.mainTabWidget.removeTab(self.ui.mainTabWidget.indexOf(self.ui.favTab))
		self.ui.mainTabWidget.removeTab(self.ui.mainTabWidget.indexOf(self.ui.contentTab))

		# Jabbim Content
#		self.ui.contentView=QtWebKit.QWebView(self.ui.contentTab)
#		self.ui.contentView.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
#		QtCore.QObject.connect(self.ui.contentView,QtCore.SIGNAL("linkClicked ( const QUrl &)"),QtGui.QDesktopServices.openUrl)
#		l=QtGui.QVBoxLayout(self.ui.contentTab)
#		l.addWidget(self.ui.contentView)
#		l.setMargin(0)
#		l.setSpacing(0)
#		self.ui.contentView.show()
		# join if we can :)
		if self.config['autoJoin']=='True':
			self.connect()

#	def t(self,i):
#		print "showTab",i

	def statusLinePaintEvent(self,event):
		if len(unicode(self.ui.statusLine.text()))==0:
			QtGui.QLineEdit.paintEvent(self.ui.statusLine,event)
			panel=QtGui.QStyleOptionFrameV2()
			self.ui.statusLine.initStyleOption(panel)
			textRect = self.ui.statusLine.style().subElementRect(QtGui.QStyle.SE_LineEditContents,panel,self.ui.statusLine)
			#if QT_VERSION >= 0x040500
			#left = self.ui.statusLine.textMargin(QtGui.LineEdit.LeftSide)
			#right = self.ui.statusLine.textMargin(QtGui.LineEdit.RightSide)
			#textRect.adjust(left, 0, -right, 0)
			p=QtGui.QPainter(self.ui.statusLine)
			p.setPen(self.ui.statusLine.palette().brush(QtGui.QPalette.Disabled, QtGui.QPalette.Text).color())
			p.drawText(textRect, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter, self.ui.statusLine.defaultText+" ");
		else:
			QtGui.QLineEdit.paintEvent(self.ui.statusLine,event)

	def showTransportsWidget(self, show):
		if show:
			self.ui.transportsWidget.show()
		else:
			self.ui.transportsWidget.hide()

	def systemSleep(self):
		log.msg("sleep emitted, disconnecting")
		self.sendPresence(None,"offline",self.tr("System is suspended"))

	def systemWakeUp(self):
		log.msg("wakeUp emitted, connecting")
		self.connect()

	#{ Public functions

	def getJid(self,jid):
		"""
		Returns Twisted Jabber ID or None if JID is in bad format.
		@type jid: unicode
		@param jid: profiles Jabber ID
		@rtype: twisted JID
		@return: Twisted Jabber ID or None
		"""
		try:
			jidt=jidT.JID(jid)
		except:
			return None
		return jidt

	def sendFiles(self,jid):
		"""
		Opens dialog for sending files.
		@type jid: unicode
		@param jid: JID
		"""

		# get files
		dialog = QtGui.QFileDialog()
		dialog.setResolveSymlinks(True)
		dialog.setDirectory(self.config['lastUploadDir'])
		#dialog.setFileMode(QtGui.QFileDialog.ExistingFiles|QtGui.QFileDialog.Directory)
		#dialog.exec_()
		#file=dialog.selectedFiles()
		file=dialog.getOpenFileNames(self,self.tr("Choose files"), self.config['lastUploadDir'])
		file=list(file)
		#get last dir from result
		if len(file)>0:
			self.config['lastUploadDir'] = os.path.dirname(unicode(file[0]))

		new=[] # temp variable
		for f in file:
			if unicode(f).endswith('.lnk'):
				f = utils.getFilenameFromLnk(unicode(f))
			if isfile(unicode(f)):
				new.append(unicode(f))
		file=new # path to files
		if len(file)!=0:
			self.showFiletransferDialog(file,jid)

	def showFiletransferDialog(self,files,jid):
		"""
		Shows filetransfer dialog.
		@type files: list of unicode
		@param files: list of files (full path)
		@type jid: unicode
		@param jid: JID
		"""
		if len(files)!=0 and os.path.isdir(files[0]):
			fr = jidT.JID(jid).userhost()
			fajly = {}
			desc = {}
			for f in files:
				#addr = f.split('/')[0]
				fajly[os.path.basename(f)] = f
				desc[os.path.basename(f)] = '%s >> %s'%('Jabbim',fr)
			print fajly
			fajly2 = {}
			for rel,  abs in fajly.iteritems():
				if os.path.isdir(abs):
					del desc[rel]
					for root, dirs, files in os.walk(abs):
	#					print root, dirs, files
						dir = root.replace(abs, rel)
						for file in files:
							fajly2[dir+'/'+file] =root+'/'+file
							desc[dir+'/'+file] = '%s >> %s'%('Jabbim',fr)
				else:
					fajly2[rel] = abs
			print desc
			print fajly2
			if len(fajly2)>0:
				self.events.addFTUploadEvent(jid, fajly2, desc)
		else:
			if self.senddialog == None:
				self.senddialog=widgets.albumfiletransfer.albumFiletransferDialog(self,files,jid)
			else:
				self.senddialog._addFiles(files)
			self.senddialog.show()


	def getImage(self,file,size=None):
		"""
		Returns deffered where is QImage loaded.
		@type file: unicode
		@param file: path to file
		@type size: list of integers
		@param size: [width,height] which are used for resizing image
		"""
		d=threads.deferToThread(self._getImage,file,size)
		return d

	def getBOBImages(self,  msg):
		"""
		Replaces src of images with cid: link
		@type msg: Message instance
		@param msg: incoming message
		"""
		if msg.xhtml != None:
			dom = parseString('<p>'+msg.xhtml.encode('utf8')+'</p>')
			#seznam = {}
			changed = False

			for el in dom.getElementsByTagName('img'):
				src = el.getAttribute('src')
				if src != None and src.startswith('cid:'):

					cid = src.split(':')[1]
					i="bob"+str(self.imageId)+str(random.randint(0,100))
					log.msg("GET BOB DATA")
					d=self.client.getBOBData(msg.frm.full(),  cid)
					d.addCallback(self.refreshImage,i,msg.frm)
					if not self.client.bobDef.has_key(cid):
						log.msg("getBobImages error: no value for key")
						continue
					link = self.client.bobDef[cid].encode('utf8')
					#link = os.getcwd()+'/images/32x32/actions/ajax-animation.gif'
					el.setAttribute('src', 'link')
					el.setAttribute('id',i)
					changed = True
					frm=msg.frm
					if self.client.groupchats.has_key(frm.userhost()):
						tab,tabIndex=self.chat.findTab(frm.full(),True)
					else:
						tab,tabIndex=self.chat.findTab(frm.full())
					if tab:
						tab.chat.ui.webkit.messageObject.src[i] = link
						tab.chat.ui.webkit.messageObject.addHandler(i,tab.chat.ui.webkit.reloadImage,[i,link])

					self.imageId+=1
					changed = True
				elif src != None and src.startswith('xmpp:') and src.find('?recvfile;')>0:
					url = QtCore.QUrl(src)
					res = self.xmppUri(url, self.client.bobCacheDir)
					if len(res)>1:
						id = res[0]
						d = res[1]
						i="bob"+str(self.imageId)+str(random.randint(0,100))

						link = self.client.bobDef[id].encode('utf8')
						#link = os.getcwd()+'/images/32x32/actions/ajax-animation.gif'
						el.setAttribute('src', link)
						el.setAttribute('id',i)
						changed = True
						frm=msg.frm
						if self.client.groupchats.has_key(frm.userhost()):
							tab,tabIndex=self.chat.findTab(frm.full(),True)
						else:
							tab,tabIndex=self.chat.findTab(frm.full())
						if tab:
							tab.chat.ui.webkit.messageObject.src[i] = link
							tab.chat.ui.webkit.messageObject.addHandler(i,tab.chat.ui.webkit.reloadImage,[i,link])

						self.imageId+=1
						changed = True
						d.addCallback(self.refreshImage,i,msg.frm)
			if changed:
				msg.setXHTML(unicode(dom.toxml(), 'utf8'))
				print unicode(dom.toxml(), 'utf8')
		return msg

	def refreshImage(self,data,name,frm):
		log.msg("refreshing image after bob: "+ unicode(data) + name)
		if self.client.groupchats.has_key(frm.userhost()):
			tab,tabIndex=self.chat.findTab(frm.full(),True)
			if not tab:
				tab,tabIndex=self.chat.findTab(frm.full())
		else:
			tab,tabIndex=self.chat.findTab(frm.full())
		#print 'frmtab',tab,frm.full(),self.client.groupchats.has_key(frm.userhost())
		if tab:
			tab.chat.reloadImage(name,"file:///"+data)

	def removeChatElement(self, name, frm):
		if self.client.groupchats.has_key(frm.userhost()):
			tab,tabIndex=self.chat.findTab(frm.full(),True)
			if not tab:
				tab,tabIndex=self.chat.findTab(frm.full())
		else:
			tab,tabIndex=self.chat.findTab(frm.full())
		if tab:
			tab.chat.ui.webkit.removeElementById(name)

	def getToolTip(self,jid, name = None):
		"""
		returns html for setToolTip
		@type jid: unicode
		@param jid: jid of contact
		"""
		jidfull = jid
		jid = jidT.JID(jid).userhost()

		text='<table><tr>'
#		if self.userRating.users.has_key(jid):
#			text+="<td>rating: "+str(self.userRating.users[jid].rating)+"</td>"
		if self.avatarDef.get(jid, False):
			if self.client.avatarImg.has_key(self.avatarDef[jid]):
				if self.client.avatarImg[self.avatarDef[jid]] and self.avatarDef[jid]!="None":
					width=self.client.avatarImg[self.avatarDef[jid]][1]
					if width!=0:
						height=self.client.avatarImg[self.avatarDef[jid]][2]
						height=height/(float(width)/64.0)
						text+='<td><img src="'+self.realHomeDir+'/avatars/'+unicode(self.avatarDef[jid])+'" width="64" height="'+str(height)+'"/></td>'
		else:
			#if there is no avatar for given JID, then try to use avatar from any metacontact
			meta = self.ui.roster.getMetaItems(jid)

			for itm in meta:
				j = itm[1]

				if self.avatarDef.get(j, False):
					if self.client.avatarImg.has_key(self.avatarDef[j]):
						if self.client.avatarImg[self.avatarDef[j]] and self.avatarDef[j]!="None":
							width=self.client.avatarImg[self.avatarDef[j]][1]
							if width!=0:
								height=self.client.avatarImg[self.avatarDef[j]][2]
								height=height/(float(width)/64.0)
								text+='<td><img src="'+self.realHomeDir+'/avatars/'+unicode(self.avatarDef[j])+'" width="64" height="'+str(height)+'"/></td>'
								break

		if name != None:
			text+='<td><b>'+unicode(self.tr("Name:"))+'</b> '+name+'<br/>'
		else:
			text+='<td>'
		text+='<b>'+unicode(self.tr("JID:"))+'</b> '+jidfull+'<br/>'
		contact = self.client.getContactByJid(jid)
		if contact == None:
			contact = self.client.getMucContactByJid(jidfull)
			if contact != None:
				status = contact.status
				if not status:
					status = ""
				text+='<img src="images/16x16/status/jabber-%s.png">' % contact.show
				text+='<b>%s</b> '%unicode(self.status.get(contact.show, ''))
				if len(status) != 0:
					text+='<br /><font size="-1">%s</font>' % (status.replace('\n', '<br />'))
			text+="</td></tr></table>"
			return text

		if unicode(contact.subscription) == 'from':
			text+='<b>'+unicode(self.tr("Subscription:"))+'</b> '+unicode(self.tr(" from"))+'<br/>'
		elif unicode(contact.subscription) == 'to':
			text+='<b>'+unicode(self.tr("Subscription:"))+'</b> '+unicode(self.tr(" to"))+'<br/>'
		elif unicode(contact.subscription) == 'none':
			text+='<b>'+unicode(self.tr("Subscription:"))+'</b> '+unicode(self.tr(" none"))+'<br/>'
		n =0

		for res in contact.resources.keys():
			status = contact.resources[res].status
			if not status:
				status = ""
			priority = contact.resources[res].priority
			#if priority == None:
			#	priority = self.tr("Unknown")
			if priority != None:
				priority = "(%s: %s)" % (unicode(self.tr("Priority")),priority)
			else:
				priority = ""
			if n>0:
				text+='<br />'
			text+='<img src="images/16x16/status/jabber-%s.png">' % contact.resources[res].show # hodilo by se rozlisit k jakymu poatri transportu
			text+='<b>%s</b> ' % unicode(self.status.get(contact.resources[res].show, ''))
			if res != None:
#							text+='<b>%s</b> %s<br>' % ( res, priority)
				text+='%s' % (priority)
			identity = contact.resources[res].identity
			if identity != '' and identity != None and identity != 'client/pc' and identity.startswith('client'):
				text+=' %s' % (identity)
			if len(status) != 0:
				text+='<br /><font size="-1">%s</font>' % (status.replace('\n', '<br />'))
			n+=1
		tune = contact.getPEP('http://jabber.org/protocol/tune')
		if type(tune) == list:
			pass
		elif tune!=None:
			artist = title = ''
			for el in tune.elements():
				if el.name == 'artist':
					artist = unicode(el)
				elif el.name == 'title':
					title = unicode(el)
			t = '%s: %s'%(artist, title)
			if len(t.strip())>1:
				text+='<br /><img src="images/22x22/icons/headphones.png" /><font size="-1">%s</font>' % (t) #ikonka se este muze menit ;)

		mood = contact.getPEP('http://jabber.org/protocol/mood')
		if mood != None:
				if isinstance(mood,list):
					log.msg("mood is list " + unicode(mood))
					if len(mood)!=0:
			  			mood=mood[0]
					else:
						mood=None
				if mood:
					t = ''
					m = txt = icon = ''
					for el in mood.elements():
						if el.name == 'text':
							txt = unicode(el)
						else:
							m = unicode(self.moods.get(el.name))
							if self.moodIcons.has_key(el.name):
								icon="<img src=\"%s\" />" % self.moodIcons[el.name].src
							else:
								icon=""
					if txt != '':
						t = '%s - %s' % (m, txt)
					else:
						t = m
					text+='<br />%s<font size="-1">%s</font>' % (icon,t)

		activity = contact.getPEP('http://jabber.org/protocol/activity')
		if activity != None:
			txt = ''
			general = ''
			spec = ''
			for el in activity.elements():
				if el.name == 'text':
					txt = unicode(el)
				else :
					general = el.name
					if self.activityGroups.has_key(general):
						general=self.activityGroups[general][0]
					spec = el.firstChildElement()
					if spec:
						spec=spec.name
					if self.activities.has_key(spec):
						spec=self.activities[spec]

			text+='<br /><font size="-1"><b>%s</b> %s %s</font>' % (general, spec, txt)
		chat = contact.getPEP('http://www.xmpp.org/extensions/xep-0194.html#ns')
		if chat != None:
			if type(chat) == list:

				text+='<br /><b>'+unicode(self.tr('User is chatting in:'))+'</b>'
				for itm in chat:
					uri = name = ''
					for el in itm.elements():
						if el.name == 'uri':
							uri = unicode(el)
							if uri.startswith('xmpp:'):
								uri = uri.replace('xmpp:', '')
						elif el.name == 'name':
							name = unicode(el)
					text+= '<br /><font size="-1">%s %s</font>'%(name, uri)
			else:

				uri = name = ''
				if len(chat.children)>0:
					text+='<br /><b>'+unicode(self.tr('User is chatting in:'))+'</b>'
					for el in chat.elements():
						if el.name == 'uri':
							uri = unicode(el)
							if uri.startswith('xmpp:'):
								uri = uri.replace('xmpp:', '')
						elif el.name == 'name':
							name = unicode(el)
						text+= '<br /><font size="-1">%s %s</font>'%(name, uri)
		text+="</td></tr></table>"
		return text

	def sendPresence(self,jid,show,message="",pri=None):
		"""
		Sends presence and update GUI.
		@type jid: unicode
		@param jid: JID or None for sending presence to server
		@type show: unicode
		@param show: String from this list: ["online","chat","away","xa","dnd","offline"]
		@type message: unicode
		@param message: Status message
		@type pri: integer
		@param pri: Priority
		"""
		log.msg("sending presence "+unicode(jid)+' '+unicode(show))
		if not jid:
			# global presence => presence will be send to server
			if show=="offline":
				self.client.sendPresence(typ = "unavailable", status = unicode(message))
#				self.client.factory.stopTrying()
				self.reconnect = False
				self.client.disconnect()
				# update avatar tooltip and tray tooltip
				self.ui.selfAvatar.refreshToolTip()
			else:
				self.client.oldstatus = (show, message)
				if not pri:
					# get priority from config
					if self.config.has_key('autoPriority'):
						if self.config['autoPriority']=='True':
							#priors={"chat":"25","online":"20","away":"15","xa":"10","dnd":"5"}
							#'autoPriority_chat','autoPriority_online','autoPriority_away','autoPriority_xa','autoPriority_dnd'

							pri=str(self.config["autoPriority_"+str(show)])
						else:
							if self.config.has_key('priority'):
								pri=self.config['priority']
							else:
								pri="0"
					else:
						if self.config.has_key('priority'):
							pri=self.config['priority']
						else:
							pri="0"
				self.selfStatus=show
				# update tray icon
				icon=QtGui.QIcon("images/16x16/apps/jabbim.png")
				if self.selfStatus!='online':
					result=icon.pixmap(16,16)
					painter=QtGui.QPainter(result)
					icon=self.getIcon(status=unicode(self.selfStatus),size="16x16")
					painter.drawPixmap(0,0,icon.pixmap(16,16))
					painter.end()
				else:
					result=icon
				self.currentTrayIcon=QtGui.QIcon(result)
				self.tray.setIcon(self.getCurrentTrayIcon())
				# update avatar tooltip and tray tooltip
				self.ui.selfAvatar.refreshToolTip()

				# keep status in config file only if status is no from autoaway
				if  show != 'away':
					MainWindow.config['keepedStatus'] = unicode(message)

				# send presence to the server
				self.client.sendPresence(show = unicode(show), status = unicode(message),priority=pri)

				# send presence to groupchats
				for muc in self.client.groupchats.itervalues():
					self.client.sendPresence(show = unicode(show), status = unicode(message), to = '%s/%s'%(muc.jid, muc.nick))

				# send presence to all transports
				#for transport in self.transports.keys():
					#self.client.sendPresence(show = unicode(show), status = unicode(message), to = transport)

				# update statusWidget
				if len(message)==0:
					self.ui.statusWidget.setText(unicode(self.status[show]))
				else:
					m=QtGui.QFontMetrics(self.ui.statusWidget.font())
					self.ui.statusWidget.setText(unicode(m.elidedText(unicode(message),QtCore.Qt.ElideMiddle, self.ui.statusWidget.width()-50)))
				self.ui.statusWidget.setIcon(self.getIcon(status=show,size="16x16"))

		else:
			if self.transports[jid]!=None:
				self.transports[jid].setIcon(self.getIcon('1@'+jid,status=unicode(show),size="16x16"))

				text='<table><tr>'
				if os.path.isfile(self.homeDir+'/avatars/'+unicode(self.config['jid'])):
					pixmap=QtGui.QIcon(self.homeDir+'/avatars/'+unicode(self.config['jid'])).pixmap(64,64)
					text+='<td><img src="'+self.homeDir+'/avatars/'+unicode(self.config['jid'])+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				#text+='<td><b>'+self.tr("Name:")+'</b> '+item.escapedName+'<br/>'
				text+='<td><b>'+self.tr("JID:")+'</b> '+unicode(jid)+'<br/>'

				#status = unicode(message)
				#priority = pri
				#if priority != None:
					#priority = "(%s: %s)" % (self.tr("Priority"),priority)
				#else:
					#priority = ""
				usertype=unicode(self.client.getHostType(jid,jid))
				if os.path.isfile('images/16x16/status/'+usertype+"-"+show+".png"):
					text+='<img src="images/16x16/status/'+usertype+"-"+show+'.png" />'
				else:
					text+='<img src="images/16x16/status/jabber-%s.png">' % show
				#if len(priority)!=0:
					#text+='%s<br/>' % priority
				if message:
					text+='<font size="-1">%s</font>' % (message)
				text+="</td></tr></table>"
				self.transports[jid].setToolTip(text)

			# send presence
			self.client.sendPresence(to=jid,show = unicode(show), status = unicode(message),priority=pri)

	def runPluginCommand(self,command,args):
		"""
		Safely runs plugins command.
		@type command: pointer to function
		@param command: pointer to plugins function
		@type args: list
		@param args: list of arguments for function
		"""
		try:
			ret=command(*args)
			return ret
		except Exception, ex:
#	temporary bugfix by triak
#			log.msg('Plugin error: ' +unicode(ex))
			log.msg('In function:'+unicode(command))
			try:
				message = unicode(traceback.format_exc(), "utf-8")
				log.msg(message)
			except:
				try:
					message = unicode(traceback.format_exc(),"utf-8")
					log.msg(message)
				except:
					log.msg("can't decode traceback")


	def getAvatarSrc(self,jid):
		hash=""
		if self.avatarDef.has_key(jid):
			hash=self.avatarDef[jid]
		if hash=="":
			file=os.getcwd()+"/images/32x32/apps/jabbim.png"
		else:
			file=self.realHomeDir+'/avatars/'+unicode(hash)
		return file

	def getAvatar(self,pixmap,size="auto",frame=False,status=None,compare=""):
		"""
		Returns avatar of contact.
		@type pixmap: unicode or QtGui.QIcon or QtGui.QPixmap
		@param pixmap: unicode - Jabber ID of contact with "@" replaced with "%";
		@type size: unicode
		@param size: auto, 16x16, 32x32, 64x64, 128x128
		@type frame: boolean
		@param frame: True - Frame is painted around the avatar.
		@type status: unicode or None
		@param status: String from this list: ["online","chat","away","xa","dnd","offline"]. Status icon will be painted to the corner.
		@rtype: QtGui.QPixmap
		@return: avatar
		"""
		if not self.client:
			return None
		#keysToDel=[]
		#for key,avatar in self.client.avatarImg.iteritems():
			#if len(unicode(key).split('/'))!=1:
				#if sys.getrefcount(avatar)==4:
					#print "Unused chached avatar",key,avatar,sys.getrefcount(avatar)
					#keysToDel.append(str(key))
		#for key in keysToDel:
			#del self.client.avatarImg[key]
		if not pixmap:
			return None
		if isinstance(pixmap,unicode) or isinstance(pixmap,str):
			hash=""
			if self.avatarDef.has_key(pixmap):
				hash=self.avatarDef[pixmap]
			if hash=="":
				file=self.realHomeDir+'/avatars/'+unicode(pixmap)
			else:
				file=self.realHomeDir+'/avatars/'+unicode(hash)
			if file==compare:
				return True
			if not os.path.isfile(file):
				return None
			icon=QtGui.QIcon(file)
		elif isinstance(pixmap,QtGui.QPixmap):
			file=pixmap
			icon=QtGui.QIcon(pixmap)
		else:
			file=""
			icon=pixmap
		if size!="auto":
			x=int(size.split('x')[0])
			y=int(size.split('x')[1])

		if frame and size!='auto':
			if size=="128x128":
				avatar=icon.pixmap(100,100)
				if avatar.width()<=50 and avatar.height()<=50:
					size="64x64"
				x=int(size.split('x')[0])
				y=int(size.split('x')[1])
			elif size=="64x64":
				avatar=icon.pixmap(50,50)
			elif size=="32x32":
				avatar=icon.pixmap(25,25)
			else:
				return False

			result=QtGui.QPixmap(x,y)
			result.fill(QtCore.Qt.transparent)
			if os.path.exists("themes/"+self.config['theme']+"/frame-"+str(size)+".png"):
				frame1=QtGui.QPixmap("themes/"+self.config['theme']+"/frame-"+str(size)+".png")
			else:
				frame1=QtGui.QPixmap("images/"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			painter.drawPixmap((x-avatar.width())/2,(y-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame1)
			painter.end()
		elif size!="auto" and not frame:

			if size=="128x128":
				avatar=icon.pixmap(100,100)
				if avatar.width()<=50 and avatar.height()<=50:
					size="64x64"
				x=int(size.split('x')[0])
				y=int(size.split('x')[1])
			elif size=="64x64":
				avatar=icon.pixmap(50,50)
			elif size=="32x32":
				avatar=icon.pixmap(25,25)
			else:
				return False
			result=QtGui.QPixmap(x,y)
			result.fill(QtCore.Qt.transparent)
			painter=QtGui.QPainter(result)
			painter.drawPixmap((x-avatar.width())/2,(y-avatar.height())/2,avatar)
			if status:
				icon=self.getIcon(status=unicode(status),size="16x16")
				if icon:
					painter.drawPixmap(16,16,icon.pixmap(16,16))
			painter.end()
		elif size=="auto" and not frame:
			result=QtGui.QPixmap(file)
		result.file=file
		return result

	def getCurrentTrayIcon(self):
		"""
		Returns current tray icon according to show.
		@rtype: QtGui.QIcon
		@return: current tray icon
		"""
		return self.currentTrayIcon

	def getIcon(self,jid=None,typ=None,size="32x32",status=None,usertype=None):
		"""
		Returns status icon.
		@type jid: unicode
		@param jid: Jabber ID
		@type size: unicode
		@param size: 16x16 or 32x32
		@type status: unicode
		@param status: String from this list: ["online","chat","away","xa","dnd","offline"]
		@rtype: QtGui.QIcon
		@return: status icon
		"""
		if size=="22x22":
			size="32x32"
		# return status icon
		#print "geticon",jid,typ,size,status,usertype
		path=self.statusPath.replace("xxxxx",size)
		typ=unicode(typ)

		if usertype!=None:
			file=path+usertype+"-online.png"
			if os.path.exists(file):
				icon=QtGui.QIcon(file)
				return icon

		if status==None:
			status=self.icons[self.shows[typ]]
		if jid!=None:
			#file=path+self.getUserType(jid)+"-"+self.icons[self.show[typ]]+".png"
			if len(jid.split("@"))>1:
				host=jid.split("@")[1].split('/')[0]
			else:
				host=jid.split('/')[0]
			if self.client.disco.has_key(host):
				usertype=unicode(self.client.getHostType(host,jid))
				file=path+usertype+"-"+status+".png"
				if os.path.exists(file):
					icon=QtGui.QIcon(file)
				else:
					#print "File not exist",file," <-",jid,typ
					#print "using",path+"jabber-"+self.icons[self.shows[status]]+".png"
					icon=QtGui.QIcon(path+"jabber-"+self.icons[self.shows[status]]+".png")
			else:
				#print "using",path+"jabber-"+self.icons[self.shows[status]]+".png"
				icon=QtGui.QIcon(path+"jabber-"+self.icons[self.shows[status]]+".png")
		else:
			if status==None:
				icon=QtGui.QIcon(path+"jabber-online.png")
			else:
				icon=QtGui.QIcon(path+"jabber-"+status+".png")
		return icon

	def now(self,shift=0):
		"""
		Returns current time in format hh:mm:ss
		@rtype: unicode
		@return: current time in format hh:mm:ss
		"""
		h,m,s=time.localtime(time.time()+shift)[3:6]
		return "%02d:%02d:%02d" % (h,m,s)

	def joinGC(self,jid,nickname):
		"""
		Joins to groupchat.
		@type jid: unicode
		@param jid: Groupchats Jabber ID
		@type nickname: unicode
		@param nickname: users nickname
		"""
		if self.chat.addGroupChatTab(jid,nickname):
			self.client.joinGC(jid, nickname,sendRooms=self.config['sendRooms']=="True")

	def getSkinColors(self,i):
		"""
		Returns colors from chat skins. This is useful for using different colors for different nicknames in Groupchat.
		Every user in groupchat have his own ID and according to ID is choosen one color.
		@type i: integer
		@param i: ID of user (color)
		@rtype: list
		@return: list of colors [#000000,#FFFFFF,#EFEFEF]
		"""
		colors=[]
		for key,value in self.skin.iteritems():
			if key.startswith("color"):
				colors.append(value)
		if len(colors)==0:
			return None
		if len(colors)==1:
			return colors[0]
		if i>len(colors)-1:
			return colors[i%(len(colors)-1)]
		else:
			return colors[i]

	#{ Private functions

	def setupShortcuts(self):
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["nextTab"]), self.chat,self.chat.next)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["previousTab"]), self.chat,self.chat.previous)

 		QtGui.QShortcut(QtGui.QKeySequence(self.config["removeTab"]), self.chat,self.chat.removeTab)

 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabOne"]), self.chat,self.chat.tabOne)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabTwo"]), self.chat,self.chat.tabTwo)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabThree"]), self.chat,self.chat.tabThree)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabFour"]), self.chat,self.chat.tabFour)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabFive"]), self.chat,self.chat.tabFive)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabSix"]), self.chat,self.chat.tabSix)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabSeven"]), self.chat,self.chat.tabSeven)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabEight"]), self.chat,self.chat.tabEight)
 		QtGui.QShortcut(QtGui.QKeySequence(self.config["tabNine"]), self.chat,self.chat.tabNine)

 		QtGui.QShortcut(QtGui.QKeySequence(self.config["moveRight"]), self.chat,self.chat.moveRight,self.chat.moveRight)
		QtGui.QShortcut(QtGui.QKeySequence(self.config["moveLeft"]), self.chat,self.chat.moveLeft,self.chat.moveLeft)

	def statusLineCanceled(self):
		"""
		Called when user cancels to change topic by statusLine
		"""
		self.ui.statusLine.hide()
		self.ui.statusWidget.show()
		self.ui.moodButton.show()
		self.ui.statusLine.defaultText=unicode(self.tr("Enter status message"))
		self.ui.statusLine.typ="statusChange"

	def statusLineFinished(self,show=None,oldStatus="",calledByTimer=False):
		"""
		Called when user finish with changing status message by statusLine
		"""
		log.msg("statusLineFinished")
		status=unicode(self.ui.statusLine.text())
		if (oldStatus!=status and calledByTimer) or not self.ui.statusLine.isVisible():
			return
		contact = self.client.roster['users'][self.client.jid.userhost()]
		#print [status,contact.resources[self.client.jid.resource].status]
		if len(status)==0 and not contact.resources[self.client.jid.resource].status:
			status=""

		if (self.ui.statusLine.typ=="presence" and (self.ui.statusLine.data!=self.selfStatus or contact.resources[self.client.jid.resource].status!=status)) or (contact.resources[self.client.jid.resource].status!=status and self.ui.statusLine.typ=="statusChange"):
			if self.ui.statusLine.typ=="presence":
				self.sendPresence(self.ui.statusLine.data[0],self.ui.statusLine.data[1],status)
			elif self.ui.statusLine.typ=="statusChange":
				self.sendPresence(None,self.selfStatus,status)
		if self.ui.statusLine.typ=="mood":
			if self.ui.statusLine.data=="none":
				self.client.sendPEP('http://jabber.org/protocol/mood', self.client.getMoodPayload(None,status))
			else:
				self.client.sendPEP('http://jabber.org/protocol/mood', self.client.getMoodPayload(self.ui.statusLine.data,status))
		elif self.ui.statusLine.typ=="activity":
			self.client.sendPEP('http://jabber.org/protocol/activity', self.client.getActivityPayload(self.ui.statusLine.data[0], self.ui.statusLine.data[1],status))
		self.ui.statusLine.hide()
		self.ui.statusWidget.show()
		self.ui.moodButton.show()
		self.ui.statusLine.defaultText=unicode(self.tr("Enter status message"))
		self.ui.statusLine.typ="statusChange"

	def statusMessageClicked(self,b=None,text=None):
		"""
		Called when user click on statusMessage.
		"""
		self.ui.statusWidget.hide()
		self.ui.moodButton.hide()
		if text!=None:
			self.ui.statusLine.setText(text)
		else:
			contact = self.client.roster['users'][self.client.jid.userhost()]
			if contact.resources[self.client.jid.resource].status:
				self.ui.statusLine.setText(unicode(contact.resources[self.client.jid.resource].status))
			else:
				self.ui.statusLine.setText("")
		self.ui.statusLine.show()
		self.ui.statusLine.setFocus(QtCore.Qt.MouseFocusReason)

	def buildOfflineMenu(self):
		"""
		Builds menu with 'show offline', 'show away' etc. There are selfResources (if user is connected from more than one client) too.
		"""
		# make Show offline QAction
		if self.client is not None:
			self.offlineMenu= self.ui.roster.buildContactMenu(unicode(self.client.jid.userhost()),None)
		else:
			self.offlineMenu = QtGui.QMenu()
		# change vcard action
		self.showChangeAvatar=self.offlineMenu.addAction(self.tr("Change profile photo"))
		self.showChangeAvatar.setCheckable(False)
		self.showChangeAvatar.setObjectName('change_avatar')
		self.showChangeAvatar.setIcon(QtGui.QIcon("images/16x16/categories/v-card.png"))
		QtCore.QObject.connect(self.showChangeAvatar, QtCore.SIGNAL("triggered ( bool )"),self.identityEditor)
		self.offlineMenu.addSeparator()

		# show offline contacts action
		#self.showOfflineAction=self.offlineMenu.addAction(self.tr("Show Offline"))
		#self.showOfflineAction.setCheckable(True)
		#self.showOfflineAction.setObjectName('show_offline')
		#self.showOfflineAction.setChecked(self.offline)
		#QtCore.QObject.connect(self.showOfflineAction,QtCore.SIGNAL("toggled ( bool )"),self.hideOffline)

		# show transports action
		#action=self.offlineMenu.addAction(self.tr("Show transports"))
		#action.setCheckable(True)
		#action.setObjectName('show_transports')
		#if self.config['showTransports']=='True':
		#	action.setChecked(True)
		# make Toggle Invisibility QAction
		#self.toggleInv=self.offlineMenu.addAction(self.tr("Become invisible"))
		#self.toggleInv.setObjectName("toggle_invisible")

		# add resources connected to the our JID (selfResources)
		if len(self.selfResources)!=0:
			for resource in self.selfResources:
				if resource!=self.client.jid.resource:
					menu=QtGui.QMenu(unicode(resource),self.offlineMenu)
					# resource supports adhoc commands
					action=menu.addAction(self.tr("Commands"))
					action.setObjectName('commands')
					action.setData(QtCore.QVariant(unicode(resource)))
					# send file QAction
					action=menu.addAction(self.tr("Send file"))
					action.setObjectName('send_file')
					action.setData(QtCore.QVariant(unicode(resource)))

					self.offlineMenu.addMenu(menu)
			self.offlineMenu.addSeparator()

		#self.ui.showOffline.setMenu(self.offlineMenu)
		QtCore.QObject.connect(self.offlineMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.offlineMenuChanged)
		QtCore.QObject.connect(self.offlineMenu, QtCore.SIGNAL("hovered ( QAction *)"),self.offlineMenuHovered)

		# refresh selfAvatar tooltip, because some resource could be added
		self.ui.selfAvatar.refreshToolTip()
		#self.ui.tabWidgetButton.setMenu(self.offlineMenu)

	def offlineMenuHovered(self, action):
		"""
		Called when offline menu is hovered.
		"""
		cmd=unicode(action.objectName())
		if cmd=='commands' and action.menu() == None:
			# show adhoc menu
			self.cmds = widgets.commands.Commands(self, unicode(self.client.jid.userhost())+"/"+unicode(action.data().toString()), action)

	def showTransports(self, show):
		self.config['showTransports'] = unicode(show)
		self.ui.actionShow_transports.setChecked(show)
		self.ui.roster.setSize()
		self.ui.roster.repaint()

	def offlineMenuChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.offlineMenu, which si created by self.buildOfflineMenu().
		@type action: QAction
		@param action: QAction from self.offlineMenu
		"""
		cmd=action.objectName()
		if cmd=='send_file':
			jid=unicode(self.client.jid.userhost())+"/"+unicode(action.data().toString()) # make jid from users jid + selected resource
			file=QtGui.QFileDialog.getOpenFileNames(self,"Choose file") # get filenames
			file=list(file)
			if len(file)!=0:
				new=[]
				for f in file:
					new.append(unicode(f))
				file=new
				# show filetransfer dialog, which sends files
				self.dialog=widgets.filetransfer.filetransferDialog(self,file,jid)
				self.dialog.show()
		#elif cmd=="show_transports":
		#	self.showTransports(action.isChecked())
		elif cmd=="toggle_invisible":
			if self.toggleInv.text() == self.tr("Become invisible"):
				self.toggleInv.setText(self.tr("Become visible"))
				self.toggleInvisibility(True)
			else:
				self.toggleInv.setText(self.tr("Become invisible"))
				self.toggleInvisibility(False)

	def tables_created(self,data):
		"""
		Called on __init__ when new sqlite tables were created. If tables were empty, adds default values (default status messages etc.), otherwise calls self.buildStatusWidgetMenu() and other functions to get data from tables.
		"""
		log.msg("tables_created")
		d = None
		for result in data:
			assert result[0]
			log.msg("table '%s' was %s" % (result[1]['table_name'], ('loaded','created')[result[1]['created']]))
			if result[1]['created'] and result[1]['table_name'] == 'status':
				t1=self.cache.set_status('online',self.tr("I'm here"))
				t2=self.cache.set_status('dnd',self.tr("Doing something important. Message me later."))
				t3=self.cache.set_status('chat',self.tr("Chat with me!"))
				t4=self.cache.set_status('xa',self.tr("Leave a message. Beep"))
				t5=self.cache.set_status('away',self.tr("Doing something else for a moment."))
				d = DeferredList([t1,t2,t3,t4,t5], consumeErrors = False)
				d.addCallback(self.status_table_updated).addErrback(self._error)
		if d == None:
			self.buildStatusWidgetMenu()
			# load rating for userRating

	def loadUserRatingFailed(self,data=None):
		self.client.createRatingList()

	def loadUserRating(self,data=None):
		if not data:
			print "asking for userrating"
			self.client.getUserRating().addCallback(self.loadUserRating).addErrback(self.loadUserRatingFailed)
		else:
			print "userrating arrived",data
			self.userRating.last_reward=float(data['lastReward'])
			del data['lastReward']
			for user in self.userRating.users.values():
				if user.jid in data.keys():
					self.userRating.users[user.jid].messages=int(data[user.jid]['messages'])
					self.userRating.users[user.jid].rating=float(data[user.jid]['val'])

	def status_table_updated(self, data=None):
		"""
		Called when status table is modified. Calls self.buildStatusWidgetMenu().
		"""

		self.buildStatusWidgetMenu()

	def _error(self,result):
		"""
		Called if there was some error with using DB.
		"""
		log.err( 'CHYBA V DATABAZI?!!!: %s' % result)


	def _getImage(self,file,size):
		image=QtGui.QImage(file)
		if size:
			image=image.scaled(size[0],size[1],QtCore.Qt.KeepAspectRatio)#,QtCore.Qt.SmoothTransformation)
		return image

	def buildTrayMenu(self):
		"""
		Builds system tray menu.
		"""
		menu=QtGui.QMenu(self)
		if self.client:
			menu.addMenu(self.statusWidgetMenu)
			self.statusWidgetMenu.setIcon(QtGui.QIcon(RESOURCEPATH+'images/16x16/status/jabber-online.png'))
		else:
			menu.addAction(QtGui.QIcon(RESOURCEPATH+'images/16x16/status/jabber-online.png'), self.tr("Connect"),self.connect)
		if len(self.config['commandsInTray'])!=0 and self.client:
			menu.addSeparator()
			for jid in self.config['commandsInTray']:
				action=menu.addAction(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/exec.png'), self.ui.roster.getNameByJID(jid))
				action.setObjectName("cmd"+unicode(jid))
				action.setData(QtCore.QVariant(jid))
		menu.addSeparator()
		action=menu.addAction(self.tr("Hide / Show"),self.trayActivated)
		menu.addAction(QtGui.QIcon(RESOURCEPATH+'images/16x16/actions/gtk-quit.png'), self.tr("Quit"),self.trayQuit)
		menu.connect(menu, QtCore.SIGNAL("hovered ( QAction * )"),self.trayMenuHovered)
		self.tray.setContextMenu(menu)

	def trayMenuHovered(self,action):
		cmd=unicode(action.objectName())
		if cmd.startswith("cmd") and action.menu() == None:
			jid=unicode(action.data().toString())
			self.cmdMenu = widgets.commands.Commands(self, jid, action)

	def buildMoodMenuAction(self, m, current_mood):
		action = self.moodMenu.addAction(self.moods[m])
		if m != 'none' and self.moodIcons.has_key(m):
			action.setIcon(self.moodIcons[m])
		action.setData(QtCore.QVariant(m))
		action.setObjectName('mood')
 		if current_mood == m:
 			font = QtGui.QFont()
 			font.setBold(True)
 		else:
 			font = QtGui.QFont()
 			font.setBold(False)
 		action.setFont(font)
		self.moodActions[m] = action
		return action

	def buildStatusWidgetMenu(self,data=None):
		"""
		Rebuilds (updates) status menu. Must be called without parametrs.
		"""
		if data==None:
			# get status messages from DB
			d=self.cache.get_status()
			d.addCallback(self.buildStatusWidgetMenu)
			d.addErrback(self._error)
			return
		else:
			# resort status messages
			config={}
			config['online']=[]
			config['offline']=[]
			config['chat']=[]
			config['away']=[]
			config['xa']=[]
			config['dnd']=[]
			for status in data:
				config[status[0]].append([status[1],str(status[2])])

		self.statusWidgetMenu=QtGui.QMenu(self.tr("Status"),self.ui.statusWidget)
		if not self.client:
			self.statusWidgetMenu.setEnabled(False)
		# make global menu. If some show has custom message, add seperator between last custom message and next show
		separator=False
		for key in ['online','chat','away','xa','dnd']:
			if separator and len(config[key])!=0:
				self.statusWidgetMenu.addSeparator()
			action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),self.status[key])
			action.setData(QtCore.QVariant(key))
			if len(config[key])!=0:
				for val in config[key]:
					status=val[0]
					index=val[1]
					if len(status)>20:
						action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),unicode(status)[:20]+"...")
					else:
						action=self.statusWidgetMenu.addAction(self.getIcon(status=key,size="16x16"),unicode(status))
					action.setData(QtCore.QVariant(key+"_"+unicode(index)))
					font=action.font()
					font.setItalic(True)
					action.setFont(font)
				self.statusWidgetMenu.addSeparator()
				separator=False
			else:
				separator=True
		if separator:
			self.statusWidgetMenu.addSeparator()


		if self.client != None and self.client.pep :
			self.ui.moodButton.show()
			#self.ui.moodButton.hide()
			# User Mood hack
			#self.moodMenu = self.statusWidgetMenu.addMenu(self.tr('Mood'))
			self.moodMenu = QtGui.QMenu(self.tr('Mood'))
 			items = self.moods.items()
 			items.sort(cmp=lambda a,b: strcoll(unicode(a[1]),unicode(b[1])))
 			keys = [ k for k,_ in items ]
 			current_mood = 'none'
			# XXX: getPEP always returns None here for me. I only receive
			# the initial mood later in on_pep. If it's always like that,
			# we can remove the following code and simplify some more.
			contact = self.client.getContactByJid(self.client.jid.userhost())
 			if contact != None:
 				moods = contact.getPEP('http://jabber.org/protocol/mood')
 				log.msg("buildStatusWidgetMenu getPEP moods=%s" % str(moods))
 				if moods != None:
 					for el in moods.elements():
 						if el.name in self.moods.keys():
 							current_mood = el.name
 							break

			current_action = self.buildMoodMenuAction('none', current_mood)
			self.moodMenu.addSeparator()
			for m in keys:
				if m != "none":
					action = self.buildMoodMenuAction(m, current_mood)
					if current_mood == m:
						current_action = action

			self.moodMenu.currentAction=current_action
			if self.moodIcons.has_key(current_mood):
				self.ui.moodButton.setIcon(self.moodIcons[current_mood])
			self.app.connect(self.moodMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.moodChanged)
			moodButtonRoot=QtGui.QMenu(self.ui.moodButton)
			moodButtonRoot.addMenu(self.moodMenu)
			activity =  QtGui.QMenu(self.tr('Activity'),moodButtonRoot)
			#activity =  self.statusWidgetMenu.addMenu(self.tr('Activity'))
			self.app.connect(activity, QtCore.SIGNAL("triggered ( QAction *)"),self.activityChanged)
			t = self.activities['none']
			action = activity.addAction(t)
			action.setObjectName('activity')
			action.setData(QtCore.QVariant(QtCore.QStringList(['none'])))
			activity.addSeparator()
			for group, txt in self.activityGroups.iteritems():
				menu = activity.addMenu(txt[0])
				if self.activityIcons.has_key(group):
					menu.setIcon(self.activityIcons[group])
				#keys = self.activities.keys()
				#keys.sort()
				for a in txt[1:]:
					t = self.activities[a]
					action = menu.addAction(t)
					if self.activityIcons.has_key(a):
						action.setIcon(self.activityIcons[a])
					action.setObjectName('activity')
					action.setData(QtCore.QVariant(QtCore.QStringList([group, a])))
			moodButtonRoot.addMenu(activity)
			self.ui.moodButton.setMenu(moodButtonRoot)
		else:
			self.ui.moodButton.hide()

		# make menu for transports
		if len(self.transports)!=0:
			function_dict = {}
			#self.ui.line1.show()
			#self.ui.transportsWidget.show()
			self.ui.tabWidgetButton.setChecked(True)
			self.ui.tabWidgetButton.show()
			print self.transports
			for transport in list(self.transports.keys()):
				# make transports QMenu and use icon according to transports type and show
				show=self.client.roster['users'][transport].status
				if len(show)==0:
					show='offline'
				else:
					show=show[0]
				#debug=unicode(self.transports)
				# We have to use status icon from previous instance of QMenu,
				# because transport doesn't need to have the same show in roster as we send him before
				# So FE we sent away, but in roster we have still online...
				if self.transports[transport]:
					continue
					#ic=QtGui.QIcon(self.transports[transport].icon())
					#self.ui.hboxlayout4.removeWidget(self.transports[transport])
					#self.transports[transport].setParent(None)
					#self.transports[transport].deleteLater()
				else:
					ic=self.getIcon("1@"+transport,status=show,size="16x16")
				#self.tray.showMessage("debug "+self.now(),"adding transport "+unicode(transport))

				#self.transports[transport].setMaximumSize(QtCore.QSize(16777215,20))
				#self.transports[transport].setMinimumSize(QtCore.QSize(32,32))
				#self.transports[transport].setIconSize(QtCore.QSize(16,16))
				#self.transports[transport].setIcon(ic)

				text='<table><tr>'
				if os.path.isfile(self.homeDir+'/avatars/'+unicode(self.config['jid'])):
					pixmap=QtGui.QIcon(self.homeDir+'/avatars/'+unicode(self.config['jid'])).pixmap(64,64)
					text+='<td><img src="'+self.homeDir+'/avatars/'+unicode(self.config['jid'])+'" width="'+str(pixmap.width())+'" height="'+str(pixmap.height())+'"/></td>'
				#text+='<td><b>'+self.tr("Name:")+'</b> '+item.escapedName+'<br/>'
				text+='<td><b>'+self.tr("JID:")+'</b> '+unicode(transport)+'<br/>'

				usertype=unicode(self.client.getHostType(transport,transport))
				if os.path.isfile('images/16x16/status/'+usertype+"-offline.png"):
					text+='<img src="images/16x16/status/'+usertype+'-offline.png" />'
				else:
					text+='<img src="images/16x16/status/jabber-offline.png">'
				#text+='<font size="-1">%s</font>' % (status)
				text+="</td></tr></table>"

				menu=QtGui.QMenu(transport,self.ui.transportsToolbar)
				menu.setIcon(self.getIcon(status=show,size="16x16"))
				# add custom messages and shows QActions to the transports QMenu
				# it's the same code (principle) as above, but it uses different QAction.data(),
				# so we can recognize if user wants to send presence to the transport instead of server
				separator=False
				for key in ['online','chat','away','xa','dnd']:
					if separator and len(config[key])!=0:
						menu.addSeparator()
					action=menu.addAction(self.getIcon("1@"+transport,status=key,size="16x16"),self.status[key])
					print 'transport status: ', key,unicode(transport)
					action.setData(QtCore.QVariant(QtCore.QStringList([key,unicode(transport)])))
					if len(config[key])!=0:
						for val in config[key]:
							status=val[0]
							index=val[1]
							if len(status)>20:
								action=menu.addAction(self.getIcon("1@"+transport,status=key,size="16x16"),unicode(status)[:20]+"...")
							else:
								action=menu.addAction(self.getIcon("1@"+transport,status=key,size="16x16"),unicode(status))
							# [show_idOfMessage,jidOfTransport]
							action.setData(QtCore.QVariant(QtCore.QStringList([key+"_"+unicode(index),unicode(transport)])))
							font=action.font()
							font.setItalic(True)
							action.setFont(font)
						menu.addSeparator()
						separator=False
					else:
						separator=True
				action=menu.addAction(self.getIcon('1@'+transport,status="offline",size="16x16"),self.tr("Log out"))
				action.setData(QtCore.QVariant(QtCore.QStringList(['offline',unicode(transport)])))
				if separator:
					menu.addSeparator()

				# updates transport menu in self.transports and add it to the self.statusWidgetMenu
				#self.transports[transport]=menu


				#self.transports[transport].setPopupMode(QtGui.QToolButton.InstantPopup)
				#self.transports[transport].setArrowType(QtCore.Qt.NoArrow)
				self.app.connect(menu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusWidgetChanged)
				def tempfunc(tt=transport):
					self.showTransportMenu(self.transports[tt])
				function_dict[transport] = tempfunc
				del tempfunc
				self.transports[transport]=self.ui.transportsToolbar.addAction(ic,"",function_dict[transport])#QtGui.QToolButton(self.ui.transportsWidget)
				#QtCore.QObject.connect(self.transports[transport],QtCore.SIGNAL("triggered()"),self.transports[transport].toggle)
				self.transports[transport].setToolTip(text)
				self.transports[transport].setMenu(menu)
				#self.ui.transportsWidget.layout().insertWidget(0,self.transports[transport])
				#self.statusWidgetMenu.addMenu(menu)
			#self.statusWidgetMenu.addSeparator()
		else:
			#self.ui.line1.hide()
			self.ui.transportsWidget.hide()
			self.ui.tabWidgetButton.show()
			self.ui.tabWidgetButton.setChecked(False)

		# other actions
		action=self.statusWidgetMenu.addAction(self.getIcon(status="online",size="16x16"),self.tr("Add message"))
		action.setData(QtCore.QVariant("custom_message"))
		action=self.statusWidgetMenu.addAction(self.getIcon(status="online",size="16x16"),self.tr("Manage messages"))
		action.setData(QtCore.QVariant("manage_messages"))
		action=self.statusWidgetMenu.addAction(self.getIcon(status="offline",size="16x16"),self.tr("Log out"))
		action.setData(QtCore.QVariant("offline"))

		self.ui.statusWidget.setMenu(self.statusWidgetMenu)
		self.app.connect(self.statusWidgetMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.statusWidgetChanged)
		self.buildTrayMenu()

	def showTransportMenu(self,action):
		action.menu().popup(QtGui.QCursor.pos())

	def moodChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.mood menu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu.
		"""
		data=action.data()
		cmd = action.objectName()

		if cmd == 'mood':
			m = unicode(data.toString())
			log.msg('setting mood to '+m)
			#if m=="none":
				#self.client.sendPEP('http://jabber.org/protocol/mood', self.client.getMoodPayload(None))
			#else:
				#self.client.sendPEP('http://jabber.org/protocol/mood', self.client.getMoodPayload(m))
			self.ui.statusLine.defaultText=unicode(self.tr("Enter mood message"))
			self.ui.statusLine.typ="mood"
			self.ui.statusLine.data=m
			self.statusMessageClicked(text="")
			self.reactor.callLater(4,self.statusLineFinished,m,"",True)
			if self.moodIcons.has_key(m):
				self.ui.moodButton.setIcon(self.moodIcons[m])
			if self.moodMenu.currentAction:
				font=self.moodMenu.currentAction.font()
				font.setBold(False)
				self.moodMenu.currentAction.setFont(font)
			self.moodMenu.currentAction=action
			font=self.moodMenu.currentAction.font()
			font.setBold(True)
			self.moodMenu.currentAction.setFont(font)

	def activityChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.mood menu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu.
		"""
		data=action.data()
		cmd = action.objectName()

		if cmd == 'activity':
			data = data.toList()
			group = unicode(data[0].toString())
			if group == "none":
				a = group = None
			else:
				a = unicode(data[1].toString())
			log.msg('setting activity to %s/%s'%(group, a))
			#self.client.sendPEP('http://jabber.org/protocol/activity', self.client.getActivityPayload(group, a))
			self.ui.statusLine.defaultText=unicode(self.tr("Enter activity message"))
			self.ui.statusLine.typ="activity"
			self.ui.statusLine.data=[group,a]
			self.statusMessageClicked(text="")
			self.reactor.callLater(4,self.statusLineFinished,a,"",True)

	def statusWidgetChanged(self,action):
		"""
		Executes command according to action.objectName(). Called when user choose one of QAction from self.statusWidgetMenu, which si created by self.buildStatusWidgetMenu().
		@type action: QAction
		@param action: QAction from self.statusWidgetMenu. if QAction.data() is string, presence is sent to the server or one of other commands is executed. If it's list, then it's in format [show,JID] and presence is sent to the JID. Show is in format "show_idOfStatusMessage" or just "show".
		"""
		data=action.data()
		cmd = action.objectName()

		if cmd=="mood":
			return
		if cmd == 'activity':
			return

		if len(data.toList())==0:
			# We are sending presence to the server
			data=unicode(data.toString())
			jid=None
		else:
			# We are sending presence to the transport
			data=data.toList()
			jid=unicode(data[1].toString())
			data=unicode(data[0].toString())

		if data=='custom_message':
			# show 'add custom message' dialog
			cs = widgets.statuseditor.statusWidgetWindow(None,self,self)
			cs.exec_()
		elif data=='manage_messages':
			# show 'manage messages' dialog
			cs = widgets.statuseditor.statusEditorWindow(self,self)
			cs.exec_()
		else:
			data=data.split("_")
			if len(data)==2:
				# get statusMessage according to ID and call self._gotStatus when we have it
				show=data[0]
				messageIndex=data[1]
				log.msg("get status by id")
				d=self.cache.get_status_by_id(str(messageIndex))
				d.addCallback(self._gotStatus,jid)
				return
			elif len(data)==1:
				show=data[0]
				message=""
				self.ui.statusLine.defaultText=unicode(self.tr("Enter status message"))
				self.ui.statusLine.data=[jid,show]
				self.ui.statusLine.typ="presence"
				self.statusMessageClicked(text="")
				log.msg("setup timeout for statusLineFinished")
				self.reactor.callLater(4,self.statusLineFinished,show,"",True)
			## send presence
			#self.sendPresence(jid,show,message)

	def _gotStatus(self,result,jid):
		"""
		Called from self.statusWidgetChange when we got statusMessage. Sends presence with message from result to JID.
		"""
		if not result:
			return
		if len(result)==0:
			return
		log.msg("got status... calling sendPresence")
		self.sendPresence(jid,result[0][0],result[0][1])

	def profileChanged(self,jid):
		"""
		Changes profile. Called when user changes profile in Login Window. Profile can be changed only if Jabbim is not connected.
		@type jid: unicode
		@param jid: profiles Jabber ID
		"""
		self.homeDir=unicode(self.realHomeDir+"/"+jid+"-profile") # get new homedir
		utils.loadConfig(self,[]) # load profiles config
		# change log files
		if self.config['log'] == 'true':
			logfile = open(self.homeDir+'/'+self.config['logfile'], 'w')
			start=True
			if self.log:
				start=False
				log.removeObserver(self.log.emit)
			self.log = safelog.SafeFileLogObserver(logfile)
			log.addObserver(self.log.emit)
			if start:
				log.startLoggingWithObserver(self.log.emit, setStdout=0)
		# change GUI according to new config
		self.loadTheme()
		self.loadSkin()
		self.ui.roster.reskin()
		#if self.config['rosterMode'] == "compact":
		#	self.ui.roster.setRosterStyle(widgets.compactrosterstyle.rosterStyle)
		#else:
		#	self.ui.roster.setRosterStyle(widgets.defaultrosterstyle.rosterStyle)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
		QtCore.QObject.disconnect(self.scroll.verticalScrollBar(),QtCore.SIGNAL("valueChanged ( int )"),self.ui.roster.sliderChanged)
		self.loadRosterStyle() # load roster style
		# change cache
		if self.cache:
			self.cache.close()
			del self.cache
		# load cache and create tables
		if sys.platform != 'win32':
			self.cache = storage.Cache(db=utils.path(self.homeDir+u'/cache.db'))
		else:
			self.cache = storage.Cache(db=(unicode(self.homeDir)+u'/cache.db').encode('utf8')) #hack!
		self.cache.create_tables().addCallback(self.tables_created)
		self.fillLoginForm()


	def fillLoginForm(self):
		"""
		Fill login form according to config file and existing profiles
		"""
		profiles=utils.getProfiles(self.realHomeDir)
		# show profiles only if their count is more than 1
		if len(profiles)<=1:
			self.ui.profilesList.hide()
			self.ui.profilesLine.hide()
			self.ui.profilesHeader.hide()
		else:
			self.ui.profilesList.show()
			self.ui.profilesLine.show()
			self.ui.profilesHeader.show()

		# update profiles QComboBox
		if self.ui.profilesList.count()!=len(profiles):
			QtCore.QObject.disconnect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)
			self.ui.profilesList.clear()
			for profile in profiles:
				jid=profile.replace('-profile','')
				# load profile avatar
				file=""
				if self.avatarDef.has_key(unicode(jid)):
					file=self.realHomeDir + "/avatars/" + self.avatarDef[unicode(jid)]
				if os.path.isfile(file):
					avatar=QtGui.QPixmap(file)
					if avatar.isNull():
						result=QtGui.QIcon("images/22x22/apps/jabbim.png")
					else:
						avatar=avatar.scaled(22,22,QtCore.Qt.KeepAspectRatio)
						result=QtGui.QPixmap(22,22)
						result.fill(QtCore.Qt.transparent)
						painter=QtGui.QPainter(result)
						painter.drawPixmap((22-avatar.width())/2,(22-avatar.height())/2,avatar)
						painter.end()
						result=QtGui.QIcon(result)
				else:
					#result=QtGui.QIcon(self.getAvatar(unicode(jid),size="32x32",frame=False))
					#if not result:
					result=QtGui.QIcon("images/22x22/apps/jabbim.png")

				if self.config['jid']==jid:
					self.ui.profilesList.insertItem(0,result,jid)
				else:
					self.ui.profilesList.addItem(result,jid)
			self.ui.profilesList.setCurrentIndex(0)
			QtCore.QObject.connect(self.ui.profilesList, QtCore.SIGNAL("currentIndexChanged ( const QString & )"),self.profileChanged)

		# fill login form
		self.ui.login_password.setText(rot13.scramble(self.config['passwd']))
		self.ui.login_jid.setText(self.config['jid'])
		if len(unicode(self.config['passwd']))== 0:
			self.ui.login_password.setFocus(QtCore.Qt.MouseFocusReason)
		else:
			self.ui.login_connect.setFocus()
		if self.config['autoJoin']=="True":
			self.ui.login_autoconnect.setChecked(True)
		else:
			self.ui.login_autoconnect.setChecked(False)
		if self.config['savePasswd']=="True":
			self.ui.login_savePassword.setChecked(True)
			self.ui.login_autoconnect.setEnabled(True)
		else:
			self.ui.login_savePassword.setChecked(False)
			self.ui.login_autoconnect.setEnabled(False)
		file=""
		if self.avatarDef.has_key(self.config['jid']):
			file=self.realHomeDir + "/avatars/" + self.avatarDef[self.config['jid']]
		if os.path.isfile(file):
			pixmap=QtGui.QIcon(file)
			avatar=pixmap.pixmap(100,112)
			if avatar.width()<=58 and avatar.height()<=58:
				size=64
			else:
				size=128
			result=QtGui.QPixmap(size,size)
			result.fill(QtCore.Qt.transparent)
			frame=QtGui.QPixmap("images/"+str(size)+"x"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			#painter.fillRect(0,0,size,size,QtGui.QBrush(self.ui.login.palette().color(QtGui.QPalette.Window)))
			painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame)
			painter.end()
			self.ui.loginAvatar.setPixmap(result)
		else:
			pixmap=QtGui.QIcon("images/48x48/apps/jabbim.png")
			avatar=pixmap.pixmap(128,112)
			if avatar.width()<=58 and avatar.height()<=58:
				size=64
			else:
				size=128
			result=QtGui.QPixmap(size,size)
			result.fill(QtCore.Qt.transparent)
			frame=QtGui.QPixmap("images/"+str(size)+"x"+str(size)+"/frame.png")
			painter=QtGui.QPainter(result)
			#painter.fillRect(0,0,size,size,QtGui.QBrush(self.ui.login.palette().color(QtGui.QPalette.Window)))
			painter.drawPixmap((size-avatar.width())/2,(size-avatar.height())/2,avatar)
			painter.drawPixmap(0,0,frame)
			painter.end()
			self.ui.loginAvatar.setPixmap(result)
		self.ui.loginAvatar.setMaximumSize(QtCore.QSize(size,size))
		self.ui.loginAvatar.setMinimumSize(QtCore.QSize(size,size))
		self.ui.loginAvatar.setAlignment(QtCore.Qt.AlignCenter)
		# set showOffline
		if self.config['showOffline']=='True':
			self.offline=False
			#self.buildOfflineMenu()
			self.hideOffline(True)
		if self.config['showTransports']=='True':
			self.showTransports(True)
		# unload plugins of old plugins
		for i in self.plugins.keys():
			self.unloadPlugin(i)
		# load plugins of this user
		self.findPlugins()
		self._reloadPlugins()



	def _reloadPlugins(self):
		self.loadPlugins()
		for plug in self.plugins.itervalues():
			if plug['module']:
				self.runPluginCommand(plug['module'].userChanged,[self.config["jid"]])

	def isConnected(self):
		return self.client and self.client.connection

	def registerButtonClicked(self):
		# depracted
		self.regwiz=wizards.registration.registrationWizard(self,self)
		self.regwiz.show()

	def serviceDiscovery(self,b):
		"""
		Shows Service Discovery Dialog. Called by QAction from main menu.
		"""
		if self.isJabbimUser:
			self.discovery2=wizards.jabbimservicemanager.jabbimServiceManager(self,self)
			self.discovery2.show()
		else:
			self.discovery=widgets.servicediscovery.serviceDiscoveryDialog(self,self)
			self.discovery.show()

	def event(self,ev):
		# depracted
		# WindowActivated
		if int(ev.type())==24:
			if self.active!=True:
				self.active=True
				if self.client:
					self.client.dispatcher.publishEvent('onActivity')

			self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
			#self.timer.stop()
		elif int(ev.type())==25:
			if self.active:

				self.active=False
				self.chat.timer.start(30000)
		return QtGui.QMainWindow.event(self,ev)

#	def privacyListEditor(self,bool=False):
#		"""
#		Shows Privacy List Editor. Called by QAction from main menu.
#		"""
#		self.ple=widgets.privacy.PrivacyListEditorDialog(self,self)
#		self.ple.show()

	def startChatDialog(self, b=False):
		message=jid=""
		while 1:
			items=QtCore.QStringList ()
			items.append(jid)
			pole=self.config['chatDialogHistory']
			pole.reverse()
			for j in pole:
				items.append(j)
			jid,b=QtGui.QInputDialog.getItem(self,self.tr("Chat with new user"),message+self.tr("Enter Jabber ID:"), items, 0, True)
			#jid,b=QtGui.QInputDialog.getText(self,self.tr("Chat with new user"),message+self.tr("Enter Jabber ID:"), QtGui.QLineEdit.Normal, jid)
			jid=unicode(jid)
			if b==True and len(jid)!=0:
				try:
					isJid=jidT.JID(jid)
				except:
					isJid=None
					message=jid+" "+self.tr("is not valid Jabber ID")+"\n"
				if isJid:
					self.chat.addChatTab(jid,jid,self.getIcon(jid,status='offline',size="16x16"))
					if isJid.userhost() not in self.config['chatDialogHistory']:
						self.config['chatDialogHistory'].append(isJid.userhost())
					self.chat.activate()
					break
			else:
				break

	def identityEditor(self,bool=False):
		"""
		Shows Vcard Editor. Called by QAction from main menu.
		"""
		widgets.vcardeditor.vcardEditorDialog(self, self.client.jid.userhost(), self).show()

	def mucBrowser(self,bool=False):
		"""
		Shows MUC Browser.
		"""
		#if not self.mucbrowser:
			#self.mucbrowser=widgets.mucbrowser.MUCBrowserDialog(self,self)
			#self.mucbrowser.show()
		#else:
			#if self.mucbrowser.isHidden()==True:
				#self.mucbrowser=widgets.mucbrowser.MUCBrowserDialog(self,self)
				#self.mucbrowser.show()
		self.joinGroupchat(bool)

	def about(self,bool):
		"""
		Shows About Jabbim dialog.
		"""
		if not self.aboutDialog:
			self.aboutDialog = aboutDialog(self)
		self.aboutDialog.show()

	def support(self, bool):
		if self.client:
			self.joinGC("jabbim@conf.netlab.cz", self.client.jid.user)
		else:
			anchor="http://live.jabbim.cz/muckl/muckl.html?conf_room=jabbim&nick="
			QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))

	def sendLog(self, bool):
		from twisted.web.microdom import unescape
		if self.client:
			try:
				log=open(self.homeDir+'/'+self.config['logfile'], 'r')
			except:
				log.err("can't open "+ self.homeDir+'/'+self.config['logfile'])
				return
			text=unicode(log.read())
			log.close()
			text=unescape(text)
			self.client.sendMessage("paste@jabbim.cz",self.config['jid'].replace("@",".")+" Jabbim.log\n"+text)

	def sendCustomStatus(self, jid, show = None):
		cs = customStatusWindow(jid, show)
		cs.exec_()

	def showInvitation(self, jid, room, reason, cont = False):
		"""
		Shows invitation to room in events.
		@type jid: unicode
		@param jid: Jabber ID of user who sends invitation
		@type room: unicode
		@param room: Jabber ID of room
		@type reason: unicode
		@param reason: Reason
		@type cont: boolean
		@param cont: True if the invitation was sent to invite third person to the 1to1 chat (chat -> groupchat)
		"""
		log.msg("%s %s %s" %(jid, room, reason))

		maintext =unicode(jid)+self.tr(" invites you to conference ")+unicode(room)+"."
		if reason != None:
			maintext += " <br/> " + self.tr("Reason: ") + unicode(reason)
		event=self.events.addLineEditEvent()
		event.setAcceptHandler(self.joinGC,[room])
		event.setRejectHandler(self.client.declineInvitation,[jid, room])
		widget=event.getWidgets()[0]
		widget.setText(maintext)
		widget.setLineEditText(self.client.jid.user)
		widget.setLabel(self.tr("Nickname:"))
		widget.setAcceptText(self.tr("Join"))
		widget.setRejectText(self.tr("Decline"))
		widget.ui.accept.setIcon(QtGui.QIcon('images/16x16/actions/ok.png'))

	def findPlugins(self):
		"""
		Finds plugins in plugins/ and ~/plugins and saves informations about them to the self.plugins
		"""
		if len(self.plugins) != 0:
			return  # we've done this already
		plugin_paths = [unicode(os.getcwd(), sys.getfilesystemencoding())+'/plugins/', self.realHomeDir + '/plugins/']
		for plugin_path in plugin_paths:
			for plugin_name in os.listdir(plugin_path):
				dir = '%s/%s' % (plugin_path, plugin_name)
				if plugin_name == '.svn' or isfile(dir):
					continue
				path = '%s/%s.py' % (dir, plugin_name)

				try:
					f = open(utils.path(path))
					module = load_source(plugin_name, path.encode(sys.getfilesystemencoding()), f)
					f.close()
					plug = module.Plugin(False, self.homeDir, dir)
					version = float(plug.version)
				except Exception, ex:
					log.msg(path + ': BAD PLUGIN!')
					log.msg(traceback.format_exc())
					continue

				if not self.plugins.has_key(plugin_name) or version > self.plugins[plugin_name]['version']:
					self.plugins[plugin_name] = { 'dir': dir, 'version': version, 'module': None }

	def startExtraDonwload(self,file):
		d=extraDialog("",self,self,file)
		d.exec_()

	def getPlugin(self, plugin):
		if self.plugins.has_key(plugin):
			return self.plugins[plugin]['module']
		else:
			return None

	def loadPlugins(self):
		"""
		Loads plugins according to config file (self.config['plugins'])
		"""
		print "loadplugins"
		for plugin_name in self.plugins.keys():
			if plugin_name in self.config['plugins']:
				try:
					self.loadPlugin(plugin_name)
				except Exception, ex:
					print "1"
					log.msg(plugin_name+': '+unicode(ex))
		if self.client:
			self.client.dispatcher.publishEvent('on_pluginsLoaded')
		#log.msg("PLUGINS:"+unicode(self.plugins))

	def loadPlugin(self,plugin):
		"""
		Loads plugin. Plugin is loaded to the self.plugins[name]['module'].
		@type plugin: unicode
		@param plugin: plugins name
		"""
		dir = self.plugins[plugin]['dir']
		path = utils.path('%s/%s.py' % (dir, plugin))
		log.msg("loading "+unicode(plugin)+" plugin")

		try:
			f=open((path))
		except:
			log.msg('plugin load error: '+plugin)
			return
		try:
			if not self.plugins[plugin]['module']:
				#plug =  # load plugin module
				module = load_source(plugin, path, f)
				f.close()
				self.plugins[plugin]['module']=module.Plugin(self, self.homeDir, dir)
				self.runPluginCommand(self.plugins[plugin]['module'].buildMainWindowMenu,[]) # build menu for plugin
				self.runPluginCommand(self.plugins[plugin]['module'].buildMainWindowToolBar,[])
			else:
				log.msg("plugin already loaded")
				f.close()
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass
		#log.msg("PLUGINS:"+unicode(self.plugins))

	def unloadPlugin(self,plugin):
		"""
		Unloads plugin. Plugin module is deleted and self.plugins[plugin]=None
		@type plugin: unicode
		@param plugin: plugins name
		"""
		if self.plugins[plugin]['module']:
			self.ui.menuPlugins.clear() # clear plugins menu
			self.runPluginCommand(self.plugins[plugin]['module']._remove,[]) # inform plugin that it will be removed

			l=gc.get_referents(self.plugins[plugin]['module'])
			for x in range(len(l)):
				del l[0]
			l=gc.get_referrers(self.plugins[plugin]['module'])
			for x in range(len(l)):
				del l[0]
			#del self.plugins[plugin]['module']
			self.plugins[plugin]['module']=None
			#del self.plugins[plugin]
			gc.collect()
			del gc.garbage[:] # delete plugin from python
			# rebuild plugins menu
			for plug in self.plugins.itervalues():
				if plug['module']:
					self.runPluginCommand(plug['module'].buildMainWindowMenu,[])
		#else:
			#print "plugin is not loaded:",plugin
		#log.msg("PLUGINS:"+unicode(self.plugins))

	def closeEvent(self,event):
		"""
		Hides window to the tray or quit if tray is not visible. Called by WM when windows is closed.
		"""
		log.msg( "TRAY VISIBLE MAIN:"+unicode(self.tray.isVisible()))
		if self.tray.isVisible():
			self.hide()
			event.accept()
			return
		self.trayQuit()
		event.accept()

	def trayQuit(self,bool=True):
		"""
		Exits Jabbim.
		"""
		try:
			privacy=self.client.privacy.active
			#privacy=True
		except:
			privacy=False
		if privacy:

			self.client.privacy.active.unsetInvisible(available=False) # hack
		for i in MainWindow.plugins.keys():
			MainWindow.unloadPlugin(i)
		self.saveConfigBeforeQuit()

		# close windows, hide tray :)
		try:
			self.cache.close()
		except:
			pass
		self.app.shutdown=True
		self.app.closeAllWindows()
		self.tray.hide()
		# stop reactor

		#app.exit()
		reactor.stop()

	def saveConfigBeforeQuit(self):
		if os.path.isfile(self.config.filename):
			# save windows geometry and sizes of splitters in chat window
			if str(self.config["saveGeometry"])=="True":
				rect=self.geometry()
				x=int(rect.x())
				y=int(rect.y())
				width=int(rect.width())
				height=int(rect.height())
				self.config["windowGeometry"]=[x,y,width,height]
				rect=self.chat.geometry()
				x=int(rect.x())
				y=int(rect.y())
				width=int(rect.width())
				height=int(rect.height())
				self.config["chatGeometry"]=[x,y,width,height]
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if w.typ=="chat":
						self.config['chatSplitterSizes']=list(w.chat.ui.splitter.sizes())
						#self.config['chatSplitter2Sizes']=list(w.chat.ui.splitter_2.sizes())
						break
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if w.typ=="groupchat":
						try:
							self.config['groupchatSplitSizes3']=list(w.chat.ui.splitter_3.sizes())
							self.config['groupchatSplitSizes1']=list(w.chat.ui.splitter.sizes())
							self.config['groupchatSplitSizes2']=list(w.chat.ui.splitter_2.sizes())
						except:
							pass

						break
				#self.config.write()
			# save expanded groups
			if str(self.config['saveExpandedGroups'])=='True':
				expanded=[]
				if self.client!=None:
					if len(self.client.roster['groups'])!=0:
						for name,item in self.client.roster['groups'].iteritems():
							if item.expanded==True:
								expanded.append(name)
						self.config['expandedGroups']=expanded
					#self.config.write()
			self.config.write()
		# save config to the ~/.jabbim/
		# we cat detect last loged user (=> last used profile) from it
		f=open(self.realHomeDir+"/config",'w')
		self.config.write(f)
		f.close()
		# save avatar cache index
		self.avatarDef.write()
	def trayActivated(self,reason=QtGui.QSystemTrayIcon.Trigger):
		"""
		Shows or hides mainWindow. Called when is tray activated.
		"""
		if reason==QtGui.QSystemTrayIcon.Trigger:
			if not self.events.trayClicked():
				if self.isHidden():
					self.show()
					self.raise_()
					self.activateWindow()
					self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
					self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
				else:
					if self.windowState() & QtCore.Qt.WindowMinimized:
						self.show()
						self.raise_()
						self.activateWindow()
						self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
						self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
					else:
						self.hide()
		elif reason==QtGui.QSystemTrayIcon.MiddleClick:
			self.ui.mainTabWidget.setCurrentIndex(4)
			if self.isHidden():
				self.show()
				self.raise_()
				self.activateWindow()
				self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
				self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
			else:
				if self.windowState() & QtCore.Qt.WindowMinimized:
					self.show()
					self.raise_()
					self.activateWindow()
					self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
					self.ui.roster.setFocus(QtCore.Qt.MouseFocusReason)
				else:
					self.hide()

	def loadTheme(self,text=None,file=None):
		"""
		Loads theme. If text==None, self.config['theme'] is used. Otherwise is stylesheet sets to `text`.
		@type text: unicode
		@param text: stylesheet css
		"""
		self.setStyleSheet("") # windows hack

		if self.config['theme']=="None" and not text:
			# theme isn't used
			text=""
			self.ui.roster.theme=False
			self.app.setStyle(self.qtStylesDefault)
		else:
			self.ui.roster.theme=True
		if text==None:
			# open theme according to self.config
			try:
				conf=ConfigObj(RESOURCEPATH+"themes/"+self.config['theme']+"/theme.ini",encoding='UTF8')
				style=False
				if conf!=None and len(conf)!=0:
					if conf.has_key('style'):
						if conf['style'] in self.qtStyles:
							self.app.setStyle(QtGui.QStyleFactory.create(conf['style']))
							style=True
				if not style:

					self.app.setStyle(self.qtStylesDefault)
				theme=open(RESOURCEPATH+"themes/"+self.config['theme']+"/style.css")
				text=theme.read()
				self.setStyleSheet(text)
				self.chat.setStyleSheet(text)
				theme.close()
			except IOError:
				# theme isn't used
				text=""
				self.ui.roster.theme=False
				self.app.setStyle(self.qtStylesDefault)
		else:
			# use text for stylesheet css
			if file:
				conf=ConfigObj(RESOURCEPATH+"themes/"+file+"/theme.ini",encoding='UTF8')
				style=False
				if conf!=None and len(conf)!=0:
					if conf.has_key('style'):
						if conf['style'] in self.qtStyles:
							self.app.setStyle(QtGui.QStyleFactory.create(conf['style']))
							style=True
				if not style:

					self.app.setStyle(self.qtStylesDefault)
			self.setStyleSheet(text)
			self.chat.setStyleSheet(text)
			if text:
				if len(text)==0:
					self.ui.roster.theme=False
		self.styleSheetText=text
		self.ui.roster.reskin(text) # reskin roster

	def addContactMainWindow(self,jid=""):
		"""
		Shows Add Contact Dialog.
		"""
		if self.isJabbimUser:
			if not self.addcontactdialog:
				self.addcontactdialog=widgets.addcontactng.addContactDialog(self,self,jid=jid)
				self.addcontactdialog.show()
			else:
				if self.addcontactdialog.isHidden()==True:
					self.addcontactdialog=widgets.addcontactng.addContactDialog(self,self,jid=jid)
					self.addcontactdialog.show()
		else:
			if not self.addcontactdialog:
				self.addcontactdialog=widgets.addcontact.addContactDialog(self,self,jid=jid)
				self.addcontactdialog.show()
			else:
				if self.addcontactdialog.isHidden()==True:
					self.addcontactdialog=widgets.addcontact.addContactDialog(self,self,jid=jid)
					self.addcontactdialog.show()

	def buildBookmarks(self,data=False):
		"""
		Adds bookmarks items to self.ui.bookmarks (QTreeWidget)
		"""
		self.bookmarks.buildBookmarks()


	def autoJoinGroupchat(self):
		"""
		Joins to groupchats which have autojoin flag.
		"""
		for k,v in self.client.bookmarks['conference'].iteritems():
			if (v.autojoin==True or unicode(v.autojoin).lower()=="true") or (v.autojoin==1 or v.autojoin=="1"):
				jid=unicode(v.jid.full())
				nickname=v.nick
				if self.chat.addGroupChatTab(jid,nickname):
					self.client.joinGC(jid, nickname, v.password,self.config['sendRooms']=="True")

	def joinGroupchat(self,bool):
		"""
		Called when user activate Join Groupchat QAction from main menu.
		"""
		#self.mucBrowser(bool)
		self.joingroupchatwizard=widgets.joingroupchat.joinGroupChatWindow(self,parent=self)
		self.joingroupchatwizard.show()

	def profilesClicked(self,bool):
		if not self.profilesWindow:
			self.profilesWindow=widgets.profiles.profilesWindow(self,self)
			self.profilesWindow.show()
		else:
			if self.profilesWindow.isHidden()==True:
				self.profilesWindow=widgets.profiles.profilesWindow(self,self)
				self.profilesWindow.show()

	def preferencesClicked(self,bool=False,page=None,viewTab=None):
		if self.preferencesWindow.isHidden()==True:
			self.preferencesWindow.show()
			self.preferencesWindow.reloadPreferences()
		if page:
			self.preferencesWindow.ui.listWidget.setCurrentRow(page)
		if viewTab:
			self.preferencesWindow.ui.tabWidget.setCurrentIndex(viewTab)

	def isValidExtraPart(self,config):
		if not config.has_key('header'):
			#log.err("error, config doesn't have 'header' section")
			return False
		if not config['header'].has_key('type'):
			#log.err("error, config doesn't have 'type' key in 'header' section")
			##############################################################
			# We're tolerant for RPC emoticons, so I have to enable them #
			##############################################################
			typ='emoticons' # will be commented
			#return False # will be uncommented
		else: # will be commented
			typ=unicode(config['header']['type']) # will be commented
		keys=['name','license','author','version','description']
		if typ=="moodIcons":
			keys.append('frontImage')
			if not config.has_key('moods'):
				#log.err("error, config doesn't have 'moods' section")
				return False
		elif typ=="emoticons":
			keys.append('frontImage')
			##############################################################
			# We're tolerant for RPC emoticons, so I have to enable them #
			##############################################################
			keys=[] # will be commented
			if not config.has_key('emoticons'):
				#log.err("error, config doesn't have 'emoticons' section")
				return False
		elif typ=='chatskin':
			if not config.has_key('chatskin'):
				#log.err("error, config doesn't have 'chatskin' section")
				return False
		for key in keys:
			if not config['header'].has_key(key):
				#log.err("error, config doesn't have '"+key+"' key in 'header' section")
				return False
		return True

	def loadJabbimExtraConfig(self,config,fallback):
		#log.err('loading JabbimExtra config '+ unicode(config))
		# try to load config
		try:
			config=ConfigObj(config,encoding='UTF8')
			loaded=True
		except:
			loaded=False
		# check config validity
		if loaded:
			loaded=self.isValidExtraPart(config)
		# config is valid
		if loaded:
			return True,config
		else:
			# try to load fallback config
			try:
				config=ConfigObj(fallback,encoding='UTF8')
				loaded=True
			except:
				loaded=False
			# check config validity
			if loaded:
				loaded=self.isValidExtraPart(config)
			if loaded:
				return False,config
			else:
				return None,None

	def loadMoods(self):
		"""
		Loads user mood icons
		"""
		loaded,config=self.loadJabbimExtraConfig(RESOURCEPATH+'moods/'+self.config['moods'],'moods/default/default.cfg')
		if loaded!=None:
			if loaded:
				src=dirname(RESOURCEPATH+"moods/"+self.config["moods"])+"/"
			else:
				src=dirname(RESOURCEPATH+"moods/default/")
			self.ui.moodButton.setIcon(QtGui.QIcon(src+config['header']['frontImage']))
			self.moodIcons=config['moods']
			for mood in self.moodIcons.keys():
				path=unicode(src+self.moodIcons[mood])
				self.moodIcons[mood]=QtGui.QIcon(path)
				self.moodIcons[mood].src=unicode(os.getcwd(), sys.getfilesystemencoding())+"/"+path
			self.moodIcons["none"]=QtGui.QIcon(self.moodIcons[mood].pixmap(16,16,QtGui.QIcon.Disabled))

	def loadActivities(self):
		"""
		Loads user mood icons
		"""
		loaded,config=self.loadJabbimExtraConfig(RESOURCEPATH+'activities/'+self.config['activities'],'activities/default/default.cfg')
		#print "ACTIVITIES",loaded,config
		if loaded!=None:
			if loaded:
				src=dirname(RESOURCEPATH+"activities/"+self.config["activities"])+"/"
			else:
				src=dirname(RESOURCEPATH+"activities/default/")
			#self.ui.moodButton.setIcon(QtGui.QIcon(src+config['header']['frontImage']))
			self.activityIcons=config['activities']
			for mood in self.activityIcons.keys():
				path=unicode(src+self.activityIcons[mood])
				self.activityIcons[mood]=QtGui.QIcon(path)
				self.activityIcons[mood].src=unicode(os.getcwd(), sys.getfilesystemencoding())+"/"+path
			self.activityIcons["none"]=QtGui.QIcon(self.activityIcons[mood].pixmap(16,16,QtGui.QIcon.Disabled))
		#print "ACTIVITIES",self.activityIcons

	def loadSounds(self):
		src=dirname(RESOURCEPATH +"sounds/"+self.config["soundPack"])
		self.sounds=ConfigObj(RESOURCEPATH+"sounds/"+self.config["soundPack"],encoding='UTF8')
		if len(self.sounds)==0:
			self.sounds=ConfigObj(self.realHomeDir+"/sounds/"+self.config["soundPack"],encoding='UTF8')
			src=dirname(self.realHomeDir+"/sounds/"+self.config["soundPack"])
		src+="/"
		self.sounds=self.sounds['sounds']
		for sound in self.sounds.keys():
			self.sounds[sound]=src+self.sounds[sound]

	def playsound(self,sound):
		if self.sounds.has_key(sound):
			if sys.platform == 'linux2': # linux sounds are produced using aplay
				os.system('aplay -q "'+self.sounds[sound].strip('\n')+'" &')
			else:
				QtGui.QSound.play(self.sounds[sound].strip('\n'))
			return True
		return False

	def loadThemePackage(self):
		self.themePackage = None
		if len(self.config['themePackage'])==0:
			self.config['themePackage']="default/default.cfg"
			self.config.write()
		theme = RESOURCEPATH+"themepackages/" + unicode(self.config['themePackage'])
		if not isfile(theme):
			theme = self.realHomeDir + "/themepackages/" + unicode(self.config['themePackage'])
			if not isfile(theme):
				theme=RESOURCEPATH+"themepackages/default/default.cfg"
		
		self.themePackage = ConfigObj(theme,encoding='UTF8')
		if len(self.themePackage)!=0:
			for key in ["chatTheme","groupchatTheme","soundPack","mood","emoticons","activities","rosterStyle","theme"]:
				if self.themePackage.has_key(key):
					if len(self.themePackage[key]["value"])!=0:
						if len(self.config[key])==0:
							self.config[key] = self.themePackage[key]["value"]
		
		

	def loadRosterStyle(self):
		self.rosterStyle=None
		if self.config['rosterStyle']==None or len(self.config['rosterStyle'])==0:
			self.config['rosterStyle']="ng/config.cfg"
			self.config.write()
		path=RESOURCEPATH+"rosterstyles/"+unicode(self.config['rosterStyle'].split("/")[0])+"/style.py"
		if not isfile(path):
			path=self.realHomeDir+"/rosterstyles/"+unicode(self.config['rosterStyle'].split("/")[0])+"/style.py"
			if not isfile(path):
				path=RESOURCEPATH+"rosterstyles/ng/style.py"


		variant=self.realHomeDir+"/rosterstyles/"+unicode(self.config['rosterStyle'])
		if not isfile(variant):
			variant=RESOURCEPATH+"rosterstyles/"+unicode(self.config['rosterStyle'])
			if not isfile(variant):
				variant=RESOURCEPATH+"rosterstyles/ng/config.cfg"

		try:
			f=open(unicode(path))
		except:
			return
		try:
			#plug =  # load plugin module
			module = load_source('rosterStyle', path, f)
			f.close()
			self.ui.roster.setRosterStyle(module.rosterStyle,variant)
		except Exception, ex:
					#log.msg(unicode(plugin)+u': '+unicode(ex))
					traceback.print_exc()
					f.close()
					pass

	def loadSkin(self):
		"""
		Loads chat skin. Skin is loaded to self.skin.
		"""
		#loaded,self.skin=self.loadJabbimExtraConfig("chatskins/"+self.config['chatSkin'],"chatskins/cool/cool.cfg")
		self.skin={}
		#if not self.skin.has_key("spaces_between_lines"):
		#	self.skin["spaces_between_lines"]='0'
		self.webkitThemeFactory=widgets.webkitthemes.webkitThemeFactory(self.config['chatTheme'],self.config['groupchatTheme'],self.realHomeDir)
		for i in range(self.chat.ui.chatTab.count()):
			w=self.chat.ui.chatTab.widget(i)
			w.chat.loadWebkit()

	def hideOffline(self,bool):
		"""
		Hides or shows offline users
		@type bool: boolean
		@param bool: True == offline users are shown, False offline users are hidden
		"""
		#self.events.addAddUserEvent('hanzz@njs.netlab.cz','offline users are shown, False offline users are hidden')
		self.config['showOffline']=unicode(bool)
		self.ui.actionShow_offline.setChecked(bool)
		#self.ui.offlineButton.setChecked(bool)
		self.offline=bool
		self.ui.roster.showOffline=bool
		self.ui.roster.reshow=True
		#if self.ui.roster.item:
			#if self.ui.roster.item.typ=="user":
				#if int(self.ui.roster.item.status)==9 and not bool:
					#self.ui.roster.statusLabel.hide()
		self.ui.roster.sortItems()
		self.ui.roster.repaint()

	def toggleInvisibility(self, bool):
		# depracted these days because ejabberd doesn't support invisibility (there are bugs fixed in svn)
		# Should be ok these days :-)
		if self.client.privacy.active:
			if bool:
				self.client.privacy.active.setInvisible()
				for gc in self.client.groupchats.keys():
					tab, indextab = self.chat.findTab(gc)
					self.ui.chatTab.removeTab(indextab)
			else:
				self.client.privacy.active.unsetInvisible()

	def loadRoster(self):
		"""
		Loads roster widget.
		"""
		layout=QtGui.QVBoxLayout(self.ui.rosterWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.scroll=scrollBar(self.ui.rosterWidget)
		self.scroll.setWidgetResizable (True)
		layout.addWidget(self.scroll)
		self.ui.roster=widgets.rosterLiveWidget.rosterWidget(self,self)
		self.scroll.setWidget(self.ui.roster)
		self.ui.mainTabWidget.tabbar.roster = self.ui.roster

	def _connected(self):
		"""
		Shows roster, changes tray icon, enable menu items etc... Called by Pyxl when we are connected.
		"""

		self.ui.roster.reskin()
		self.ui.actionAdd_Contact.setEnabled(True)
		self.ui.actionJoin_groupchat.setEnabled(True)
		self.ui.actionService_Discovery.setEnabled(True)
		self.ui.actionStart_Chat.setEnabled(True)
#		self.ui.actionPrivacy_list_editor.setEnabled(True)
		self.ui.actionIdentity.setEnabled(True)
		self.buildStatusWidgetMenu()
		try:
			self.statusWidgetMenu.setEnabled(False)
		except:
			pass
		self.ui.selfName.setText("<h3>"+unicode(self.client.jid.userhost()).split("@")[0]+"</h3>")
		self.ui.selfName.hide()
		self.selfName=unicode(self.client.jid.userhost()).split("@")[0]
		self.client.getVCard(unicode(self.client.jid.userhost()))
		#self.ui.showOffline.hide()
#		self.tray.showMessage(self.tr("Jabbim"),self.tr("Jabbim is ready! You are connected! :) "))
		self.tray.setIcon(QtGui.QIcon(RESOURCEPATH+"images/16x16/apps/jabbim.png"))
		pixmap=self.getAvatar(self.client.jid.userhost(),frame=False,status=None)
		if pixmap:
			avatar=self.getAvatar(pixmap,size="32x32",frame=True)
			self.selfAvatar=pixmap
			self.ui.selfAvatar.setPixmap(avatar)
			self.ui.selfAvatar.setMinimumWidth(avatar.width()+3)



	def disconnect(self):
		"""
		Stops reactor
		"""
		#if self.client!=None:
		reactor.stop()
		#pass

	def newProfile(self,jid,password,savePassword):
		self.homeDir=self.realHomeDir+"/"+jid+"-profile"
		#if not os.path.isdir(self.homeDir):
			#os.mkdir(self.homeDir)
		utils.makeHomeDir(self.homeDir)
		f=open(self.homeDir+"/config",'w')
		self.config.write(f)
		f.close()
		utils.loadConfig(self,[]) # load config files
		self.config['savePasswd']=unicode(savePassword)
		if savePassword==True:
			self.config['passwd']=rot13.scramble(password)
		else:
			self.config['passwd']=""
		self.config['jid']=jid
		self.config.write()

	def connectCancel(self):

		if self.client:
			if self.client.factory:
				self.client.factory.stopTrying()
		self.reconnect = False
		if self.client:
			self.client.disconnect()
		self._disconnect()

	def getImages(self, xhtml,frm):
		dom = parseString(unicode('<p>'+xhtml+'</p>'))
		#seznam = {}
		for el in dom.getElementsByTagName('img'):
			src = el.getAttribute('src')
			if src != None and src.startswith('http'):
				novy = self.realHomeDir+'/temp/'+sha1(src).hexdigest()
				el.setAttribute('src', novy)
				if not el.hasAttribute('width') or not el.hasAttribute('height'):
					el.setAttribute('width', '64')
					el.setAttribute('height', '64')
				#newnode = parseString("<a href=\"http://seznam.cz\">"+unicode(el.toxml(),'utf-8')+"</a>").documentElement
				newnode=Element('a')
				newnode.setAttribute('href', unicode(src))
				newnode.appendChild(el.cloneNode())
				log.msg( unicode(newnode.toxml(),'utf-8'))
				el.parentNode.replaceChild(newnode,el)
				fp = open(novy,'wb')
				fp.close()
				fp = open(novy+"_copy",'wb')
				d = downloadPage(str(src), fp)
				d.addCallback(self._imageReceived, fp,novy,frm)
		try:
			ret=unicode(dom.toxml(), 'utf-8').replace("<:img","<img")
		except:
			ret = None
		return ret

	def _imageReceived(self,neco,fp,file,frm):

		fp.close()
		os.rename(file+"_copy",file)
		for i in range(self.chat.ui.chatTab.count()):
			w=self.chat.ui.chatTab.widget(i)
			if unicode(w.jid) == frm:
				# update viewport to refresh image
				w.chat.ui.textEdit.viewport().update()

	def xmppUri(self,  url,  path = None):
		# path is used to save auto-accepted files
		#if path == None: no auto-accept
		url.setQueryDelimiters('=',';')
		q = url.queryItems()
		query ={}
		jid = jidT.JID(unicode(url.path()))
		try:
			query['type'] = q.pop(0)[0]
		except IndexError:
			query['type'] = 'message'
		for i in q:
			query[unicode(i[0])] = unicode(i[1])

		if query['type'] == 'message':
			#open tab here
			status = 'offline' # HACK! doplnit aktualni stav kvuli ikonky
			self.chat.addChatTab(jid.full(),self.ui.roster.getNameByJID(jid.userhost()),self.getIcon(jid.full(),status = status,size="16x16"))
			self.chat.activate()
			return True
		elif query['type'] == 'recvfile':
			id = query.get('sid')
			if path != None:
				path = path + '/'+id
			return (id, self.client.getSIPUBFile(jid.full(),  id,  path))
			pass
		elif query['type'] == 'join':
			jd  = unicode(jid)
			nickname = self.selfName
			if self.chat.addGroupChatTab(jd,nickname):
				self.client.joinGC(jd, nickname, None,self.config['sendRooms']=="True")


	def connect(self,delay=None):
		# Connect to the server
		if delay:
			reactor.callLater(delay,self.connect)
			return
		self.ui.roster.emptyRosterWidget.hide()
		self.connectStarted=int(time.time())
		jid=unicode(self.ui.login_jid.text()).strip()
		if not re.match(r'.+@.+', jid):
			self.ui.login_jid.setFocus(QtCore.Qt.OtherFocusReason)
			if jid.find('@') == -1:
				self.ui.login_jid.setText(jid + '@')
			return
		if len(unicode(self.ui.login_password.text())) == 0:
			self.ui.login_password.setFocus(QtCore.Qt.OtherFocusReason)
			reactor.callLater(0,self.passError)
			return
		if not self.getJid(jid):
			reactor.callLater(0,self.jidError)
			return
		self.ui.selfAvatar.setPixmap(QtGui.QPixmap('images/32x32/apps/jabbim.png'))
		self.ui.rosterStackedWidget.setCurrentIndex(2)
		self.ui.login_headerLabel.hide()
		self.ui.splashImage.show()
		self.ui.login_connect.setEnabled(False)
		self.ui.profilesList.setEnabled(False)
		self.ui.loginInfo.setText(self.tr("Connecting to the server..."))
		reactor.callLater(0,self.connect__)

	def jidError(self):
		QtGui.QMessageBox.critical(self, self.tr("Bad JID"),self.tr("You have an error in your Jabber ID."))

	def passError(self):
		QtGui.QMessageBox.critical(self, self.tr("Empty password"),self.tr("Your password is empty."))

	def connect__(self):
		if self.config['usePsyco'] == 'True':
			try:
				import psyco
				#psyco.log()
				#psyco.profile()
				#psyco.full(memory=1000)
				#psyco.profile(0.05, time = 20)
				#psyco.profile(0.15, memory = 5000)
				#psyco.background()
				psyco.full()
				#psyco.runonly()
			except ImportError:
				log.err('Psyco not installed..')

		start=time.time()
		# get variables
		jid=unicode(self.ui.login_jid.text()).strip()
		password=unicode(self.ui.login_password.text())
		# get profiles
		profiles=utils.getProfiles(self.realHomeDir)

		# this profile exists
		if jid+"-profile" in profiles:
			self.homeDir=self.realHomeDir+"/"+jid+"-profile"
			utils.loadConfig(self,[]) # load config files
			# login informations have been updated
			if (jid!=self.config['jid'] or (unicode(self.ui.login_savePassword.isChecked())=="True" and unicode(rot13.scramble(password))!=unicode(self.config['passwd']))) or (unicode(self.config['savePasswd'])!=unicode(self.ui.login_savePassword.isChecked()) or unicode(self.ui.login_autoconnect.isChecked())!=self.config['autoJoin']):
				ret=QtGui.QMessageBox.question(self,self.tr("Login information"), self.tr("Save current login information?"),3,4)
				if ret==3:
					# update config file
					self.config['savePasswd']=self.ui.login_savePassword.isChecked()
					if self.ui.login_savePassword.isChecked()==True:
						self.config['passwd']=rot13.scramble(password)
					else:
						self.config['passwd']=""
					self.config['jid']=jid
					if self.ui.login_autoconnect.isEnabled():
						self.config['autoJoin']=unicode(self.ui.login_autoconnect.isChecked())
					else:
						self.config['autoJoin']="False"
					self.config.write()
		# this profile not exists, so we have to create it
		else:
			#ret=QtGui.QMessageBox.question(self,self.tr("New profile"), self.tr("Profile for this JID doesn't exist. Do you want to create it?"),3,4)
			#if ret==3:
			self.homeDir=self.realHomeDir+"/"+jid+"-profile"
			utils.makeHomeDir(self.homeDir)
			# copy actual config to new profile dir
			f=open(self.homeDir+"/config",'w')
			self.config.write(f)
			f.close()
			# load config file
			utils.loadConfig(self,[])
			# update config file
			self.config['savePasswd']=self.ui.login_savePassword.isChecked()
			if self.ui.login_savePassword.isChecked()==True:
				self.config['passwd']=rot13.scramble(password)
			else:
				self.config['passwd']=""
			self.config['jid']=jid
			if self.ui.login_autoconnect.isEnabled():
				self.config['autoJoin']=unicode(self.ui.login_autoconnect.isChecked())
			else:
				self.config['autoJoin']="False"
			self.config.write()

		# save last used config to real homedir (no profile homedir)
		f=open(self.realHomeDir+"/config",'w')
		self.config.write(f)
		f.close()

		# create clientClass
		if self.config.has_key('resource'):
			resource=''.join(self.config['resource'])
		else:
			resource='jabbim'
		if self.client==None:
			#print "creating client class"
			self.client = clientClass(unicode(jid).lower()+"/"+resource, password, jid.split("@")[1], 5222,self,reactor)
			print self.plugins
			for plug in self.plugins.itervalues():
				if plug['module']:
					#print "calling client created"
					self.runPluginCommand(plug['module'].clientCreated,[])


		path = self.realHomeDir+'/avatars/'
		if self.avatarDef.has_key(self.client.jid.userhost()):
			if self.avatarDef[self.client.jid.userhost()]:
				self.client.avatarImg[self.avatarDef[self.client.jid.userhost()]] = self.loadAvatar(self.avatarDef[self.client.jid.userhost()])
		img=self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"))
		img.file=None
		self.client.avatarImg[None]=[img,32,32]
		img.file="None"
		self.client.avatarImg[u'None']=[img,32,32]
		#d=threads.deferToThread(self.loadAvatars,unicode(path),dict(self.avatarDef))
		#d.addCallback(self.gotAvatars)

		# sets None for all avatars
		hashe = []
		for hash in self.avatarDef.itervalues():
			if not hash in hashe and hash and hash!="None":
				hashe.append(hash)
		for key in hashe:
			self.client.avatarImg[key]=None
		# load avatars
		self.imageLoader=avatarLoader.avatarLoader(self,unicode(path),dict(self.avatarDef))
		QtCore.QObject.connect(self.imageLoader,QtCore.SIGNAL("imageLoaded(QString,QImage,int,int)"),self.avatarLoaded,QtCore.Qt.QueuedConnection)
		self.imageLoader.start(QtCore.QThread.LowestPriority)

		#self.gotAvatars(self.loadAvatars(unicode(path),dict(self.avatarDef)))
		try:
			self.client.xmlLang= unicode(QtCore.QLocale.system().name())[:2]
		except:
			try:
				self.client.xmlLang = unicode(os.environ["LANG"][:2])
			except:
				log.err('error in setting locale')
		self.client.log=True

		# connect
		self.reconnect = True
		if self.config['specifyHost'] == 'True':
			self.client.connect(self.config['connectHost'], self.config['connectPort'],JID=unicode(jid).lower()+"/"+resource,password=password,server=jid.split("@")[1])
		elif self.config['boshURL'] != '':
			self.client.connect(boshURL = self.config['boshURL'],JID=unicode(jid).lower()+"/"+resource,password=password,server=jid.split("@")[1])
		else:
			self.client.connect(JID=unicode(jid).lower()+"/"+resource,password=password,server=jid.split("@")[1])

		self.isJabbimUser = jid.split("@")[1] in self.jabbimServers

	#def _loadAvatar(self,file, hash, jid):
		#if os.path.isfile(unicode(file)):
			#jid=jidT.JID(jid).userhost()
			#pixmap=QtGui.QPixmap(unicode(file))
			#for item in self.ui.roster.getUserItems(jid):
				#item.setAvatar(QtGui.QIcon(pixmap))
			#for item in self.ui.roster.getMetaItems(jid):
				#item[0].setAvatar(QtGui.QIcon(pixmap))
		#else:
			#log.msg("BAD FILE FOR AVATAR:"+unicode(file))
		#self.client.roster['users'][jid].setAvatar(file, hash)

	def avatarLoaded(self,key,image,width,height):
		"""
		Called by avatarLoader when image with hash 'key' is loaded.
		"""
		img = QtGui.QPixmap.fromImage(image)
		img.file=key
		if self.client != None:
			self.client.avatarImg[unicode(key)]=[img,int(width),int(height)]
		del img

	#def loadAvatars(self,path,avatarDef):
		#avatarImg={}

		#hashe = []
		#try:
			#for hash in avatarDef.itervalues():
				#if not hash in hashe and hash and hash!="None":
					#hashe.append(unicode(str(hash)))
		#except:
			#message = unicode(traceback.format_exc(), 'utf-8')
			#print message
##		path = self.main.homeDir+'/avatars/'
		#print "loadAvatars",hashe
		#frame=QtGui.QImage("images/32x32/frame.png")
		#for hash in hashe:
			#try:
				##self.avatarImg[hash] = self.main.getAvatar(hash)
				#avatar=QtGui.QImage(path+'/'+hash)
				#width=int(avatar.width())
				#height=int(avatar.height())
				#avatar=avatar.scaled(25,25,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
				#result=QtGui.QImage(32,32,QtGui.QImage.Format_ARGB32)
				#result.fill(QtCore.Qt.transparent)
				##if os.path.exists("themes/"+self.config['theme']+"/frame-32.png"):
					##frame=QtGui.QImage("themes/"+self.config['theme']+"/frame-32.png")
				##else:
				#painter=QtGui.QPainter(result)
				#painter.drawImage((32-avatar.width())/2,(32-avatar.height())/2,avatar)
				#painter.drawImage(0,0,frame)
				#painter.end()
				#avatarImg[hash] = [result,width,height]
			#except:
				#avatarImg[hash] = None
				#message = unicode(traceback.format_exc(), 'utf-8')
				#print message
		#return avatarImg

	def loadAvatar(self,hash):
		path=self.realHomeDir+"/avatars"
		avatar=QtGui.QImage(path+'/'+hash)
		width=int(avatar.width())
		height=int(avatar.height())
		avatar=avatar.scaled(25,25,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation)
		result=QtGui.QImage(32,32,QtGui.QImage.Format_ARGB32)
		result.fill(QtCore.Qt.transparent)
		#if os.path.exists("themes/"+self.config['theme']+"/frame-32.png"):
			#frame=QtGui.QImage("themes/"+self.config['theme']+"/frame-32.png")
		#else:
		frame=QtGui.QImage("images/32x32/frame.png")
		painter=QtGui.QPainter(result)
		painter.drawImage((32-avatar.width())/2,(32-avatar.height())/2,avatar)
		painter.drawImage(0,0,frame)
		painter.end()
		img = QtGui.QPixmap.fromImage(result)
		img.file=hash
		return [img,width,height]

	#def gotAvatars(self,avatarImg):
		#self.client.avatarImg=avatarImg
		#for key in self.client.avatarImg.keys():
			#self.client.avatarImg[key][0]=QtGui.QPixmap.fromImage(self.client.avatarImg[key][0])
			##print 'avatarSize',self.client.avatarImg[key].width(),self.client.avatarImg[key][0].height()
		#self.client.avatarImg[None]=[self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"),size="32x32",frame=True),32,32]
		#self.client.avatarImg[u'None']=[self.getAvatar(QtGui.QPixmap("images/32x32/apps/jabbim.png"),size="32x32",frame=True),32,32]
		#print 'LOADED AVATARS',self.client.avatarImg


	def _addGroup(self, group):
		item=self.ui.roster.addGroup(unicode(group))
		if group in self.config['expandedGroups']:
			item.setExpanded(True)
			#self.ui.roster.repaint()
		return item

	def _addUser(self, itemjid, name, grp):
		return self.ui.roster.addUser(itemjid,name,grp)

	def _badJabberPassword(self):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Bad Jabber ID or password.")),0,1)

	def _serverNotFound(self):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Server is not found.")),0,1)
	def _connectionFailed(self):
		QtGui.QMessageBox.warning(self,self.tr("Error"),unicode(self.tr("Connection to server failed. Check your Jabberd ID and try it again.")),0,1)

	def _disconnect(self, error = None): # error = None | dns | lost | auth | failed
		log.msg('disconnect reason '+unicode(error))
		self.tray.setIcon(QtGui.QIcon(QtGui.QIcon(RESOURCEPATH+"images/16x16/apps/jabbim.png").pixmap(16,16,QtGui.QIcon.Disabled)))
		if self.client:
			if error=="auth":
				reactor.callLater(0,self._badJabberPassword)
				self.reconnect = False
			elif error=="dns":
				reactor.callLater(0,self._serverNotFound)
				self.reconnect = False
			elif error=="failed":
				reactor.callLater(0,self._connectionFailed)
				self.reconnect = False
			if self.client.factory:
				self.client.factory.stopTrying()
		else:
			return
		self.config.write()
		MainWindow.ui.rosterStackedWidget.setCurrentIndex(0)
		MainWindow.ui.login_headerLabel.show()
		MainWindow.ui.splashProgress.setValue(0)
		#MainWindow.ui.showOffline.hide()
		MainWindow.ui.actionAdd_Contact.setEnabled(False)
		MainWindow.ui.actionJoin_groupchat.setEnabled(False)
		MainWindow.ui.actionService_Discovery.setEnabled(False)
		MainWindow.ui.actionStart_Chat.setEnabled(False)
#		MainWindow.ui.actionPrivacy_list_editor.setEnabled(False)
		MainWindow.ui.actionIdentity.setEnabled(False)
#		self.client=None
		self.selfResources=[]
		if self.client.oldstatus:
			self.ui.loginStatus.setItemData(MainWindow.ui.loginStatus.findText(MainWindow.status[self.client.oldstatus[0]]),  QtCore.QVariant(QtCore.QStringList([self.client.oldstatus[0], self.client.oldstatus[1]])))
			self.ui.loginStatus.setCurrentIndex(MainWindow.ui.loginStatus.findText(MainWindow.status[self.client.oldstatus[0]]))

		try:
			self.statusWidgetMenu.setEnabled(False)
		except:
			pass
		self.ui.login_cancel.show()
		self.ui.profilesList.setEnabled(True)

		MainWindow.ui.roster.sortedGroups=[]
		MainWindow.ui.roster.sorted={}
		MainWindow.ui.roster.users=[]
		MainWindow.ui.roster.disconnect()
		MainWindow.ui.login_connect.setEnabled(True)
		#self.ui.eventsListWidget.clear()
		self.events.removeAll()
		self.ui.transportsToolbar.clear()
		#for transport in self.transports.keys():
			#if self.transports[transport]:
				#self.ui.transportsWidget.layout().removeWidget(self.transports[transport])
				#self.transports[transport].setParent(None)
				#self.transports[transport].deleteLater()
		self.transports={}

		if self.client:
			for jid in self.client.groupchats.keys():
				for i in range(self.chat.ui.chatTab.count()):
					w=self.chat.ui.chatTab.widget(i)
					if unicode(w.jid) == jid:
						w.chat.ui.line.setEnabled(False)
						w.chat.ui.users.clear()
						w.chat.addRoles()
						message=self.webkitThemeFactory.genChatStatus(unicode(self.tr("You are now offline.")),self.now())
						w.chat.textEditWrite(message)
						w.chat.lastMessageFrom=""
		if error == 'lost' and MainWindow.reconnect:
#			self.client.oldstatus = self.client.getContactByJid(self.client.jid.full()).status
			self.reconnect = False
			msg = None
			try:
				MainWindow.client.xping.stop()

			except:
				log.err('can\'t stop xping')
 			# connection lost, let's wait for a while and then reconnect
			MainWindow.tray.showMessage(self.tr("Connection lost! "),self.tr("Trying to reconnect ..  ") , QtGui.QSystemTrayIcon.Warning, 5000)
 			#MainWindow.plugins={}
# 			MainWindow.client = None
			log.err('Connection Lost')
			if msg != None and len(msg)>0:
				MainWindow.delayedMessages = msg
 			reactor.callLater(5, MainWindow.connect)
		else:
			self.client=None
			 #= None
			for i in MainWindow.plugins.keys():
				MainWindow.unloadPlugin(i)
			self._reloadPlugins()
		self.buildTrayMenu()

	def on_network_state_up(self):
		# XXX
		log.msg("on_network_state_up")
	def on_network_state_down(self):
		# XXX
		self.connectCancel()
		log.msg("on_network_state_down")