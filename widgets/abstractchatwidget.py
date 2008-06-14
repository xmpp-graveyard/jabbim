try:
	from PyQt4 import QtCore, QtGui,QtWebKit
except:
	print "PyQt4 is not installed."


from configobj import ConfigObj
#from palette import *
import urllib,re,os
from twisted.web.microdom import *
from twisted.web.domhelpers import gatherTextNodes
import filetransfer
from pyxl import jid as jidT
import time
from include import utils
from emoticonswidget import *
from linkeditor import linkEditorDialog

class message(QtCore.QObject):
	def __init__(self,message):
		QtCore.QObject.__init__(self)
		self.message=message
		self.scr=1
		self.setObjectName("messageObject")

	@QtCore.pyqtSignature("",result="QString")
	def msg(self):
		return self.message
	
	@QtCore.pyqtSignature("",result="int")
	def scroll(self):
		return self.scr

class abstractTextView(QtGui.QTextEdit):
	"""
	Text view for chat conversation.
	"""
	def __init__(self,main,parent):
		QtGui.QTextEdit.__init__(self,parent)
		self.parent=main
		self.main=self.parent.main
		self.setMouseTracking(True)
		self.setReadOnly(True)
		self.data=[]
		self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
		self.setAcceptDrops(True)
		self.setObjectName("chatView")
		self.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)

	def dragEnterEvent(self, event):
		if event.mimeData().hasText():
			if self.main.getJid(unicode(event.mimeData().text())):
				event.acceptProposedAction()
			else:
				event.ignore()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

	def dropEvent(self, event):
		"""
		Called when something is dropped to this widget.
		If there is JID dropped, new MUC is created and the jid is invited to the room.
		"""
		if event.mimeData().hasText():
			# test if it is JID
			jid2=self.main.getJid(unicode(event.mimeData().text()))
			if not jid2:
				event.ignore()
				return

			room=str(int(time.time())) # define room name
			# find server when we can host the room
			mucjid = None
			for jid, node in self.main.client.disco.iteritems():
				if not node[None].has_key('identities'):
					continue
				for id in node[None]['identities'].itervalues():
					#print jid, id
					if id.get('category') == 'conference' and id.get('type') == 'text' and jid.startswith('c'):
						mucjid = jid
						break
				if mucjid:
					break
			room+="@"+mucjid # room jabber id
			
			name=self.parent.parent.tabName # get name of tab where is this widget showed
			rmIndex=int(self.main.chat.ui.chatTab.currentIndex()) # get index of this tab
			# join to the room and send invitation
			if self.main.chat.addGroupChatTab(room,self.main.client.jid.user,name=name):
				tab,index=self.main.chat.findTab(room)
				tab.chat.invitation=[unicode(jid2.full()),unicode(self.parent.jid)]
				self.main.client.joinGC(room, self.main.client.jid.user)
			# remove old user2user conversation tab
			self.main.chat.removeTab(rmIndex)
			event.acceptProposedAction()
		else:
			event.ignore()
		
	def mouseMoveEvent(self,event):
		"""
		Changes mouse pointer if it is above link.
		"""
		anchor = self.anchorAt(event.pos())
		if len(anchor)!=0:
			self.viewport().setCursor(QtCore.Qt.PointingHandCursor)
		else:
			self.viewport().setCursor(QtCore.Qt.ArrowCursor)
		return QtGui.QTextEdit.mouseMoveEvent(self,event)

	def mousePressEvent(self,event):
		"""
		Opens link under mouse pointer.
		"""
		anchor = self.anchorAt(event.pos())
		if event.button()==QtCore.Qt.LeftButton:
			if len(anchor)!=0:
				QtGui.QDesktopServices.openUrl(QtCore.QUrl(anchor))
		return QtGui.QTextEdit.mousePressEvent(self,event)
	
	#def createMimeDataFromSelection(self):
		#"""
		#Creates data for clipboard from selected text.
		#"""
		#text=unicode(self.textCursor().selection().toHtml())
		##print text
		#a=parseString(text)
		#for el in a.getElementsByTagName('img'):
			#path=el.attributes['src'].split('/')[-1]
			#p=os.path.dirname(self.parent.main.emoticonsWidget.smileys[self.parent.main.emoticonsWidget.smileys.keys()[0]])
			#path=p+"/"+path
			#for k,v in self.parent.main.emoticonsWidget.smileys.iteritems():
				#if v==path:
					#path=k
					#newnode = parseString("<div> "+path+"</div>").documentElement
					#el.parentNode.replaceChild(newnode,el)
					#break
		#b=a.getElementsByTagName('body')
		#try:
			#c=parseString(unicode(b[0].toxml(),'utf-8').replace("<!--EndFragment-->","").replace("<!--StartFragment-->",""))
		#except:
			#c=parseString(unicode(b[0].toxml()).replace("<!--EndFragment-->","").replace("<!--StartFragment-->",""))
		#for el in c.getElementsByTagName('br'):
			##if self.parent.main.skin['spaces_between_lines']=='1':
				##newnode = parseString("<div> "+unichr(2028)+unichr(2028)+"</div>").documentElement
			##else:
			#newnode = parseString("<div> 123456789123456789987654321</div>").documentElement
			#el.parentNode.replaceChild(newnode,el)
		#for el in c.getElementsByTagName('table'):
			#newnode = parseString(unicode("<div>123456789123456789987654321123456789123456789987654321</div>")).documentElement
			##print [newnode.toxml()]
			##el.parentNode.replaceChild(newnode,el)
			#el.appendChild(newnode)
			
		#text=gatherTextNodes(c)
		#u=False
		#text=text.replace("123456789123456789987654321","\n")
		#print [text]
		##print [text]
		#try:
			#text=unicode(text, 'utf-8')
			#u=True
		#except:
			#text=unicode(text)
		##if u:
		##print [text]
		##print unicode(text)

		#self.data.append(QtCore.QMimeData())
		#self.data[-1].setText(unicode(text).replace("&gt;",">").replace("&lt;","<").replace("&amp;","&").replace("&quot;","\""))
		#return self.data[-1]

class lineEditWidget(QtGui.QTextEdit):
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main
		self.parent=parent
		self.setObjectName("line")



	def keyPressEvent(self,event):
		key=event.key()
		self.main.tabWord=None
		if (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and (event.modifiers() & QtCore.Qt.ControlModifier):
			if self.main.main.config['sendByCtrl']=="True":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
			if self.main.main.config['sendByCtrl']=="False":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		
		else:
			return QtGui.QTextEdit.keyPressEvent(self,event)
			text=unicode(self.toPlainText())
			for k,v in self.parent.smileys.iteritems():
				if text.find(" "+k)!=-1:
					html=self.toHtml()
					html.replace(k,'<img src="'+v+'"/> ')
					cur=self.textCursor()
					self.setHtml(html)
					self.setTextCursor(cur)

class normalLineEditWidget(QtGui.QTextEdit):
	"""
	QTextEdit widget for user input.
	"""
	def __init__(self,main,parent=None):
		apply(QtGui.QTextEdit.__init__,(self,parent))
		self.main=main #: MainWindow pointer
		self.parent=parent #: parent
		self.setObjectName("line")
		self.composing=False #: True if user is typing
		self.timer=QtCore.QTimer() # timer to determine if user paused typing
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.paused)
		self.text=""
		self.t=False
		self.bold=False
		self.italic=False
		self.underline=False
		self.color=None
		self.backgroundBrush=None
		self.fontSize=None
		self.changeFormat=True
		self.reformated=False
		if self.parent.xhtml:
			QtCore.QObject.connect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)
			#QtCore.QObject.connect(self,QtCore.SIGNAL("cursorPositionChanged ()"),self.setFormat)

	#def event(self,ev):
		#if ev.type()==QtCore.QEvent.Shortcut or ev.type()==QtCore.QEvent.ShortcutOverride:
			#sequence=unicode(ev.key().toString()).lower()
			#for shortcut in self.main.config['activeShortcuts']:
				#print self.main.config[shortcut].lower(),sequence
				#if self.main.config[shortcut].lower()==sequence:
					#return False
		#return QtGui.QTextEdit.event(self,ev)

	def setFormat(self,fmt=None):
		# detect format of current character
		f=fmt.font()
		if len(unicode(self.textCursor().selectedText()))==0:
			b=f.bold()
			if self.bold!=b:
				self.bold=b
				self.parent.ui.boldButton.setChecked(b)
			b=f.italic()
			if self.italic!=b:
				self.italic=b
				self.parent.ui.italicButton.setChecked(b)
			b=f.underline()
			if self.underline!=b:
				self.underline=b
				self.parent.ui.underlineButton.setChecked(b)
			b=fmt.foreground().color()
			if self.color!=b:
				self.color=b
				colorIcon=QtGui.QPixmap(16,16)
				colorIcon.fill(b)
				self.parent.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))
			b=fmt.background()
			if True:

				self.backgroundBrush=b
				colorIcon=QtGui.QPixmap(16,16)
				#for background color
				if fmt.background().isOpaque():
					colorIcon.fill(QtGui.QColor(b.color()))
				else:
					colorIcon.fill(QtGui.QColor(self.parent.defaultBackgroundColor))
				p=QtGui.QPixmap("images/16x16/actions/format-text-bold.png")
				painter=QtGui.QPainter(colorIcon)
				painter.drawPixmap(0,0,p)
				painter.end()
				self.parent.ui.backgroundButton.setIcon(QtGui.QIcon(colorIcon))

			#b=float(f.pointSize())
			#if self.fontSize!=b:
				#self.fontSize=b
				#self.parent.ui.fontSize.setCurrentIndex(self.parent.ui.fontSize.findText(str(int(self.fontSize))))

	#def focusInEvent(self,event):
		#r=QtGui.QTextEdit.focusInEvent(self,event)
		#self.blockSignals(True)
		#if self.parent.xhtml:
			#self.reformat(self.currentCharFormat())
			##QtCore.QObject.connect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)
		#self.blockSignals(False)
		#return r

	def formatChanged(self,format):
		if format.isAnchor() or self.signalsBlocked():
			print 'blocked'
			return
		self.blockSignals(True)
		#QtCore.QObject.disconnect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)
		if len(unicode(self.toPlainText()))==0:
			if not self.reformated:
				print "reformat"
				self.reformated=True
				self.reformat(format)
				#QtCore.QObject.connect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)
			else:
				self.reformated=False
			self.blockSignals(False)
			return
		print "setFormat"
		self.setFormat(format)
		self.blockSignals(False)
		#QtCore.QObject.connect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)

	def reformat(self,fmt=None):
		#QtCore.QObject.disconnect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)
		self.parent.underline(self.underline)
		self.parent.bold(self.bold)
		self.parent.italic(self.italic)
		#if self.fontSize:
			#self.parent.fontSize(self.fontSize)
			#self.parent.ui.fontSize.setCurrentIndex(self.parent.ui.fontSize.findText(str(int(self.fontSize))))
		if self.color:
			self.parent.color(unicode(self.color.name()))
		if self.backgroundBrush:
			if self.backgroundBrush.isOpaque():
				self.parent.background(unicode(self.backgroundBrush.color().name()))
			else:
				self.parent.background(unicode('no'))
		
		#QtCore.QObject.connect(self,QtCore.SIGNAL("currentCharFormatChanged ( const QTextCharFormat & )"),self.formatChanged)

	def paused(self):
		"""
		Detects if user stops typing and sends 'paused' message if user stops.
		"""
		try:
			self.timer.stop()
		except:pass
		if self.text==unicode(self.toPlainText()):
			# text from previous loop is the same as currently typed text => user stops typing
			if len(self.text)!=0:
				self.main.main.client.sendMessage(self.main.jid, "",composing="paused")
			self.composing=False
		else:
			# text from previous loop is diffrent from currently typed text => user is typing
			self.timer.start(2000)
			self.text=unicode(self.toPlainText())

		self.t=False
	
	def keyPressEvent(self,event):
		if event.matches(QtGui.QKeySequence.NextChild):
			self.main.main.chat.event(event)
			return
		elif event.matches(QtGui.QKeySequence.PreviousChild):
			self.main.main.chat.event(event)
			return
		if not self.composing:
			# user starts typing
			self.main.main.client.sendMessage(self.main.jid, "",composing="composing")
		key=event.key()
		if key!=QtCore.Qt.Key_Tab:
			self.main.tabWord=None
		if (key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter) and (event.modifiers() & QtCore.Qt.ControlModifier):
			if self.main.main.config['sendByCtrl']=="True":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		elif key==QtCore.Qt.Key_Return or key==QtCore.Qt.Key_Enter:
			if self.main.main.config['sendByCtrl']=="False":
				self.main.sendButtonClicked()
				event.accept()
			else:
				return QtGui.QTextEdit.keyPressEvent(self,event)
		elif key == QtCore.Qt.Key_Up and  self.main.hindex > 0 and (event.modifiers() & QtCore.Qt.ControlModifier): 
			self.main.hindex = self.main.hindex-1
			self.main.ui.line.setText(self.main.sent[self.main.hindex])
		elif key == QtCore.Qt.Key_Down and  self.main.hindex < len(self.main.sent) and (event.modifiers() & QtCore.Qt.ControlModifier): 

			self.main.hindex = self.main.hindex+1
			self.main.ui.line.setText(self.main.sent[self.main.hindex])
		elif key==QtCore.Qt.Key_Tab:
			self.main.tabPressed()
			return
		else:
			QtGui.QTextEdit.keyPressEvent(self,event)

		# user starts composing so we have to start checking if he doesn't stop
		# we have to start timer only once, so there is some type of locker self.t
		if not self.t and not self.composing:
			self.text=unicode(self.toPlainText())
			self.t=True
			self.timer.start(2000)
		if not self.composing:
			self.composing=True


class abstractChatWidget(QtGui.QWidget):
	def __init__(self,initClass,textEditClass,main,jid,xhtml=True,parent=None):
		apply(QtGui.QWidget.__init__,(self,parent))
		self.ui=initClass()
		self.ui.setupUi(self)
		self.main=main
		self.parent=parent
		self.xhtml=xhtml

		# chat view widget (self.ui.textEdit)
		l=QtGui.QHBoxLayout(self.ui.viewWidget)
		l.setMargin(0)
		l.setSpacing(0)
		self.ui.textEdit=textEditClass(self,self.ui.viewWidget)
		self.ui.textEdit.hide()
		self.ui.webkit=QtWebKit.QWebView(self)
		self.ui.webkit.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,True)
		try:
			typ=self.typ
		except:
			typ="chat"
		if typ=="groupchat":
			stylesheet=self.main.webkitThemeFactory.genGroupchatStyleSheet()
			footer=self.main.webkitThemeFactory.genGroupchatFooter()
			header=self.main.webkitThemeFactory.genGroupchatHeader()
		else:
			stylesheet=self.main.webkitThemeFactory.genChatStyleSheet()
			footer=self.main.webkitThemeFactory.genChatFooter()
			header=self.main.webkitThemeFactory.genChatHeader(self.name,self.file)
		html="""
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<style type="text/css" media="screen,print"> @import url( "main.css" ); </style>
<style id="mainStyle" type="text/css" media="screen,print"> %s </style>
<script>
function addMessage() {
shouldScroll = nearBottom();
//Remove any existing insertion point
insert = document.getElementById("insert");
if(insert) insert.parentNode.removeChild(insert);

var ni = document.getElementById('myDiv');
var numi = document.getElementById('theValue');
var num = (document.getElementById('theValue').value -1)+ 2;
numi.value = num;
var divIdName = "my"+num+"Div";
var newdiv = document.createElement('div');
newdiv.setAttribute("id",divIdName);
newdiv.innerHTML = messageObject.msg();
ni.appendChild(newdiv);
if (shouldScroll) scrollToBottom();

}
function insertMessage() {
shouldScroll = nearBottom();

                        //Locate the insertion point
                        var insert = document.getElementById("insert");

                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        newNode = range.createContextualFragment(messageObject.msg());

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);
if (shouldScroll) scrollToBottom();

}
//Auto-scroll to bottom.  Use nearBottom to determine if a scrollToBottom is desired.
function nearBottom() {
		return ( document.body.scrollTop >= ( document.body.offsetHeight - ( window.innerHeight * 1.2 ) ) );
}
function scrollToBottom() {
		document.body.scrollTop = document.body.offsetHeight;
}


</script>
</head>
<body>
<div id="Chat">
%s
<input type="hidden" value="0" id="theValue" />
<div id="myDiv"> </div>
%s
</div>
<a name='bottom'></a>
</body>
</html>
		""" % (stylesheet,header,footer)



		#f=open("/home/hanzz/svn/jabbim/trunk/test.html","w")
		#f.write(html)
		#f.close()

		#f=open(os.getcwd()+"/chatskins/candy/Incoming/Content.html","r")
		#self.incoming=f.read()
		#f.close()
		if typ=="groupchat":
			self.ui.webkit.page().mainFrame().setHtml(html,QtCore.QUrl(self.main.webkitThemeFactory.groupchatPath()))
		else:
			self.ui.webkit.page().mainFrame().setHtml(html,QtCore.QUrl(self.main.webkitThemeFactory.chatPath()))
		self.messageObject=message("")
		self.ui.webkit.page().mainFrame().addToJavaScriptWindowObject("messageObject",self.messageObject)

		#self.ui.webkit.load(QtCore.QUrl("file:///home/hanzz/svn/jabbim/trunk/test.html"))
		l.addWidget(self.ui.webkit)
		self.ui.webkit.show()
		self.ui.webkit.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
		QtCore.QObject.connect(self.ui.webkit,QtCore.SIGNAL("linkClicked ( const QUrl &)"),QtGui.QDesktopServices.openUrl)
		# chat editor widget (self.ui.line)
		layout=QtGui.QHBoxLayout(self.ui.lineWidget)
		layout.setMargin(0)
		layout.setSpacing(0)
		self.ui.line=normalLineEditWidget(self,self)
		self.ui.line.setAcceptRichText(False)
		layout.addWidget(self.ui.line)

		self.first=None #: True if first message arrived; False if arrived more than one message. Otherwise None.
		self.jid=jid #: users JID
		self.sent = []
		self.hindex = 0
		self.featuredWidget=[]

		# signals
		QtCore.QObject.connect(self.ui.sendButton, QtCore.SIGNAL("clicked ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.line, QtCore.SIGNAL("returnPressed ()"),self.sendButtonClicked)
		QtCore.QObject.connect(self.ui.smileys, QtCore.SIGNAL("toggled (bool)"),self.smileysClicked)
		QtCore.QObject.connect(self.ui.boldButton, QtCore.SIGNAL("clicked ( bool )"),self.bold)
		QtCore.QObject.connect(self.ui.italicButton, QtCore.SIGNAL("clicked (bool)"),self.italic)
		QtCore.QObject.connect(self.ui.underlineButton, QtCore.SIGNAL("clicked (bool)"),self.underline)
		QtCore.QObject.connect(self.ui.linkButton, QtCore.SIGNAL("clicked (bool)"),self.link)
		#QtCore.QObject.connect(self.ui.fontSize,QtCore.SIGNAL("activated(const QString &)"),self.fontSize)
		
		self.ui.textEdit.setAcceptRichText(False)
		# save init part from self.main.skin to the textEdit
		self.init=""
		if self.main.skin.has_key("on_init"):
			self.init=self.main.skin["on_init"]
		self.ui.textEdit.setHtml("<br/>"+self.init)
		
		self.unread=0 #: number of unread messages

		if not self.xhtml:
			self.ui.boldButton.hide()
			self.ui.italicButton.hide()
			self.ui.underlineButton.hide()
			self.ui.colorButton.hide()
			self.ui.fontSize.hide()
			self.ui.backgroundButton.hide()
			self.ui.linkButton.hide()
		else:
			self.ui.fontSize.hide()
			#db=QtGui.QFontDatabase()
			#for size in db.standardSizes():
				#self.ui.fontSize.addItem(str(size))
			#self.ui.fontSize.setCurrentIndex(self.ui.fontSize.findText(str(QtGui.QApplication.font().pointSize())))
			#self.ui.line.fontSize=float(str(QtGui.QApplication.font().pointSize()))

			self.defaultFormat=self.ui.line.currentCharFormat()
			self.defaultColor=self.ui.line.textColor()
			self.ui.line.color=self.defaultColor
			self.defaultBackgroundColor=QtGui.QColor(self.ui.line.palette().base().color())
			colorMenu=QtGui.QMenu(self.ui.colorButton)
			backgroundMenu=QtGui.QMenu(self.ui.backgroundButton)
			colorIcon=QtGui.QPixmap(16,16)
			
			colorIcon.fill(QtCore.Qt.white)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('White'))
			action.setData(QtCore.QVariant("#ffffff"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('White'))
			action.setData(QtCore.QVariant("#ffffff"))

			colorIcon.fill(QtCore.Qt.black)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Black'))
			action.setData(QtCore.QVariant("#000000"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Black'))
			action.setData(QtCore.QVariant("#000000"))

			colorIcon.fill(QtCore.Qt.red)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Red'))
			action.setData(QtCore.QVariant("#ff0000"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Red'))
			action.setData(QtCore.QVariant("#ff0000"))

			colorIcon.fill(QtCore.Qt.green)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Green'))
			action.setData(QtCore.QVariant("#00ff00"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Green'))
			action.setData(QtCore.QVariant("#00ff00"))

			colorIcon.fill(QtCore.Qt.blue)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Blue'))
			action.setData(QtCore.QVariant("#0000ff"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Blue'))
			action.setData(QtCore.QVariant("#0000ff"))

			colorIcon.fill(QtCore.Qt.magenta)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Pink'))
			action.setData(QtCore.QVariant("#ff00ff"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Pink'))
			action.setData(QtCore.QVariant("#ff00ff"))

			colorIcon.fill(QtCore.Qt.yellow)
			action=colorMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Yellow'))
			action.setData(QtCore.QVariant("#ffff00"))
			action=backgroundMenu.addAction(QtGui.QIcon(colorIcon),self.tr('Yellow'))
			action.setData(QtCore.QVariant("#ffff00"))

			colorMenu.addSeparator()

			action=colorMenu.addAction(self.tr('No color'))
			action.setData(QtCore.QVariant("no"))
			action=backgroundMenu.addAction(self.tr('No color'))
			action.setData(QtCore.QVariant("no"))

			QtCore.QObject.connect(colorMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.color)
			QtCore.QObject.connect(backgroundMenu, QtCore.SIGNAL("triggered ( QAction *)"),self.background)
			self.ui.colorButton.setMenu(colorMenu)
			self.ui.backgroundButton.setMenu(backgroundMenu)
			colorIcon.fill(self.defaultFormat.foreground().color())
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))
			
			#for background color
			colorIcon.fill(self.defaultBackgroundColor)
			p=QtGui.QPixmap("images/16x16/actions/format-text-bold.png")
			painter=QtGui.QPainter(colorIcon)
			painter.drawPixmap(0,0,p)
			painter.end()
			self.ui.backgroundButton.setIcon(QtGui.QIcon(colorIcon))

	def registerFeatureForWidget(self,feature,widget):
		self.featuredWidget.append([feature,widget])
		if self.main.client.hasFeature(self.jid,feature):
			widget.show()
		else:
			widget.hide()

	def unregisterFeatureForWidget(self,widget):
		for item in self.featuredWidget:
			if widget==item[1]:
				self.featuredWidget.remove(item)
				break

	def showFeaturedWidgets(self):
		for item in self.featuredWidget:
			feature=item[0]
			widget=item[1]
			print "checking ",feature," = ",self.main.client.hasFeature(self.jid,feature)
			if self.main.client.hasFeature(self.jid,feature):
				widget.show()
			else:
				widget.hide()

	def isLink(self,text):
		if text.find("://")!=-1:
			return True
		elif text.startswith("www."):
			return True
		return False

	def link(self,bool=None):
		text=unicode(self.ui.line.textCursor().selectedText())
		clipboardText=unicode(QtGui.QApplication.clipboard().text())
		url=None
		linktext=None
		if self.isLink(text):
			url=text
		elif self.isLink(clipboardText):
			url=clipboardText
			if len(text)!=0:
				linktext=text
		else:
			if len(text)!=0:
				linktext=text
		
		d=linkEditorDialog(self,url,linktext,self)
		d.exec_()
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		#self.ui.line.textCursor().insertHtml("<a href=\"%s\">%s</a>"%(text,text))
		
		

	def fontSize(self,size):
		size=float(size)
		self.ui.line.fontSize=size
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		#self.ui.line.setFontPointSize(size)
		fmt=QtGui.QTextCharFormat()
		fmt.setFontPointSize(size)
		cursor = self.ui.line.textCursor()
		cursor.mergeCharFormat(fmt)
		self.ui.line.setTextCursor(cursor)
		self.ui.line.mergeCurrentCharFormat(fmt)

	def color(self,action):
		"""
		Sets foreground color according to action.data(). Data should be color like #FFFFFF or string "no" for default system color.
		"""
		if isinstance(action,unicode) or isinstance(action,str):
			color=action
			if color.startswith('#'):
				self.ui.line.color=QtGui.QColor(color)
		else:
			color=unicode(action.data().toString())
			self.ui.line.color=QtGui.QColor(color)
			self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		
		if color.startswith("#") and QtGui.QColor(color)!=self.defaultColor:
			c=QtGui.QColor(color)
			self.ui.line.setTextColor(c)
			colorIcon=QtGui.QPixmap(16,16)
			colorIcon.fill(c)
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))
		else:
			format=self.defaultFormat
			format.setFontItalic(self.ui.line.fontItalic())
			format.setFontUnderline(self.ui.line.fontUnderline())
			format.setFontWeight(self.ui.line.fontWeight())
			fmt=self.ui.line.currentCharFormat()
			#print 'opaque',fmt.background().isOpaque()
			if fmt.background().isOpaque():
				format.setBackground(QtGui.QBrush(fmt.background()))
				self.ui.line.backgroundBrush=fmt.background()

			self.ui.line.setCurrentCharFormat(format)
			colorIcon=QtGui.QPixmap(16,16)
			colorIcon.fill(self.defaultFormat.foreground().color())
			self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))

	def background(self,action):
		"""
		Sets background color according to action.data(). Data should be color like #FFFFFF or string "no" for default system color.
		"""
		if isinstance(action,unicode) or isinstance(action,str):
			color=action
			self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
			#if color.startswith('#'):
				#self.ui.line.backgroundColor=QtGui.QColor(color)
		else:
			color=unicode(action.data().toString())
			#self.ui.line.backgroundColor=QtGui.QColor(color)
			self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		
		if color.startswith("#") and QtGui.QColor(color)!=self.defaultBackgroundColor:
			#c=QtGui.QColor(color)
			#self.ui.line.setTextColor(c)
			#colorIcon=QtGui.QPixmap(16,16)
			#colorIcon.fill(c)
			#self.ui.colorButton.setIcon(QtGui.QIcon(colorIcon))

			fmt=QtGui.QTextCharFormat()
			fmt.setBackground(QtGui.QBrush(QtGui.QColor(color)))
			self.ui.line.backgroundBrush=fmt.background()
			cursor = self.ui.line.textCursor()
			cursor.mergeCharFormat(fmt)
			self.ui.line.setTextCursor(cursor)
			self.ui.line.mergeCurrentCharFormat(fmt)
			colorIcon=QtGui.QPixmap(16,16)
			#for background color
			colorIcon.fill(QtGui.QColor(color))
			p=QtGui.QPixmap("images/16x16/actions/format-text-bold.png")
			painter=QtGui.QPainter(colorIcon)
			painter.drawPixmap(0,0,p)
			painter.end()
			self.ui.backgroundButton.setIcon(QtGui.QIcon(colorIcon))


		else:
			#format=self.defaultFormat
			#format.setFontItalic(self.ui.line.fontItalic())
			#format.setFontUnderline(self.ui.line.fontUnderline())
			#format.setFontWeight(self.ui.line.fontWeight())
			#format.setBackground(QtGui.QBrush(QtGui.QColor(QtCore.Qt.red)))
			#self.ui.line.setCurrentCharFormat(format)
			
			fmt=QtGui.QTextCharFormat()
			fmt.setFontItalic(self.ui.line.fontItalic())
			fmt.setFontUnderline(self.ui.line.fontUnderline())
			fmt.setFontWeight(self.ui.line.fontWeight())
			c=QtGui.QColor(self.ui.line.textColor())
			self.ui.line.backgroundBrush=fmt.background()
			self.ui.line.setCurrentCharFormat(fmt)
			#self.ui.line.backgroundBrush=self.ui.line.currentCharFormat().background()
			if c!=self.defaultColor:
				self.ui.line.setTextColor(c)

			colorIcon=QtGui.QPixmap(16,16)
			#for background color
			colorIcon.fill(self.defaultBackgroundColor)
			p=QtGui.QPixmap("images/16x16/actions/format-text-bold.png")
			painter=QtGui.QPainter(colorIcon)
			painter.drawPixmap(0,0,p)
			painter.end()
			self.ui.backgroundButton.setIcon(QtGui.QIcon(colorIcon))

	def clearLine(self):
		format=self.ui.line.currentCharFormat()
		self.ui.line.clear()
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)
		if format.isAnchor():
			self.ui.line.blockSignals(True)
			self.ui.line.reformat()
			self.ui.line.blockSignals(False)
		else:
			self.ui.line.setCurrentCharFormat(format)
		

	def italic(self,bool):
		"""
		Sets italic font according to bool.
		@type bool: boolean
		@param bool: True - italic font
		"""
		self.ui.line.italic=bool
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)

		fmt=QtGui.QTextCharFormat()
		fmt.setFontItalic(bool)
		cursor = self.ui.line.textCursor()
		cursor.mergeCharFormat(fmt)
		self.ui.line.setTextCursor(cursor)
		self.ui.line.mergeCurrentCharFormat(fmt)

	def qtHtmlToXhtml(self,xhtml,text):
		"""
		Converts html from QTextEdit to xhtml-im compatible text.
		@type xhtml: unicode
		@param xhtml: Qt html
		"""
		# remove <style>
		alinks=[]
		a=parseString(unicode(xhtml))
		for el in a.getElementsByTagName('p'):
			if el.hasAttribute("style"):
				el.removeAttribute("style")
		for el in a.getElementsByTagName('body'):
			if el.hasAttribute("style"):
				el.removeAttribute("style")
		for el in a.getElementsByTagName('a'):
			alinks.append(unicode(el.getAttribute('href')))
			alinks.append(unicode(gatherTextNodes(el)))
			for x in el.getElementsByTagName("span"):
				x.removeAttribute("style")
				#print unicode(x.toxml())
		# remove <body>
		b=a.getElementsByTagName('body')
		b=b[0]
		xhtml=b.toxml()
		# TODO: we must replace only first <body> and <p>... not tags in whole message
		xhtml=unicode(xhtml,'utf-8').replace("<body>","").replace("</body>","")#.replace("<p>","<span>").replace("</p>","</span>")
		# TODO: we must use something more secure and faster than replace and for... it's ugly but i don't know
		# better twisted based solution
		if len(xhtml.split("<p>"))==1:
			# only one <p>, so we have to change it to span.
			xhtml=xhtml.replace("<p>","<span>").replace("</p>","</span>")
		else:
			# there are more <p>, so we change </p> to <br/> and remove last <br/>
			xhtml=xhtml.replace("<p>","").replace("</p>","<br/>")
			br=xhtml.split('<br/>') # [a,b,c,d]
			t=""
			for i in range(len(br)):
				if i!=len(br)-1:
					t+=br[i]+"<br/>"
				else:
					t+=br[i]
			xhtml=t[:-5]
		# replace url by <a href="url"></url>
		same=False
		#print xhtml.replace("<br/>",'\n').replace("<br />",'\n')
		#print escape(text)
		if xhtml.replace("<br/>",'\n').replace("<br />",'\n')==escape(text):
			same=True
		links=[]
		print unicode(xhtml)
		print alinks
		temp=unicode(xhtml).replace(">","<")
		for word in temp.split("<"):
			for w in word.split(' '):
				alink=False
				for l in alinks:
					if w.find(l)!=-1:
						alink=True
						break
				if not w in links and not alink:
					print w
					if w.find("://")!=-1:
						links.append(w.strip())
					elif w.startswith("www."):
						links.append(w.strip())
		print links
		for link in links:
			xhtml=xhtml.replace(link,'<a href="'+link+'">'+link+'</a>')
		print xhtml
		return xhtml,same
	
	def smileysClicked(self, checked):
		"""
		Shows self.s (QFrame with emoticons).
		"""
		pos=self.ui.smileys.mapToGlobal(QtCore.QPoint(0,0))
		x=pos.x()
		y=pos.y()
		self.main.emoticonsWidget.acceptor=self
		self.main.emoticonsWidget.setGeometry(x-self.main.emoticonsWidget.pixmap.width()/2,y-self.main.emoticonsWidget.pixmap.height(), self.main.emoticonsWidget.pixmap.width(), self.main.emoticonsWidget.pixmap.height())

		self.main.emoticonsWidget.setVisible(checked) 
		
	def underline(self,bool):
		"""
		Sets underline font according to bool.
		@type bool: boolean
		@param bool: True - underline font
		"""
		self.ui.line.underline=bool
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)

		fmt=QtGui.QTextCharFormat()
		fmt.setFontUnderline(bool)
		cursor = self.ui.line.textCursor()
		cursor.mergeCharFormat(fmt)
		self.ui.line.setTextCursor(cursor)
		self.ui.line.mergeCurrentCharFormat(fmt)


	def bold(self,bool):
		"""
		Sets bold font according to bool.
		@type bool: boolean
		@param bool: True - bold font
		"""
		self.ui.line.bold=bool
		self.ui.line.setFocus(QtCore.Qt.OtherFocusReason)

		fmt=QtGui.QTextCharFormat()
		
		if bool==True:
			fmt.setFontWeight(QtGui.QFont.Bold)
		else:
			fmt.setFontWeight(QtGui.QFont.Normal)
		cursor = self.ui.line.textCursor()
		cursor.mergeCharFormat(fmt)
		self.ui.line.setTextCursor(cursor)
		self.ui.line.mergeCurrentCharFormat(fmt)

	def appendXhtml(self,xhtml):
		message=xhtml.replace("&quot;",'"')
		file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
		if not os.path.isfile(file):
			file="images/32x32/apps/jabbim.png"
		message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",message).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
		self.textEditWrite(message)

	def appendPlainText(self,text):
		text=unicode(text).replace("<","&lt;").replace(">","&gt;").replace("\n","<br/> ")
		text=utils.replace_url(text)
		text=text.replace("  ","&nbsp;&nbsp;").replace("\t","&nbsp;&nbsp;&nbsp;")
		file=self.main.homeDir+'/avatars/'+unicode(self.main.client.jid.userhost())
		if not os.path.isfile(file):
			file="images/32x32/apps/jabbim.png"
		if unicode(text).startswith("/me"):
			message=self.main.skin["my_me_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text[3:]).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
		else:
			message=self.main.skin["my_message"].replace("[time]",self.main.now()).replace("[user]",unicode(self.main.client.jid.user)).replace("[message]",text).replace("[avatar]","<img src=\""+file+"\" width=\"32\" height=\""+str(self.selfHeight)+"\" />")
		self.textEditWrite(message)

	
	def webkitWrite(self,text,insert=False):
		for k,v in self.main.emoticonsWidget.smileys.iteritems():
			text=text.replace(" "+k,'&nbsp;<img src="'+v+'"/>')
			text=text.replace("&nbsp;"+k,'&nbsp;<img src="'+v+'"/>')
			text=text.replace(">"+k,'><img src="'+v+'"/>')
		self.messageObject.message=unicode(text)
		if not insert:
			self.ui.webkit.page().mainFrame().evaluateJavaScript("addMessage();")
		else:
			self.ui.webkit.page().mainFrame().evaluateJavaScript("insertMessage();")

	def textEditWrite(self,text,insert=False):
		"""
		Appends formated message to the chat view (self.ui.textEdit).
		@type text: unicode
		@param text: formated message
		@type history: boolean
		@param history: True if text is history message (has delay). In this case self.first will not be updated.
		"""
		self.webkitWrite(text,insert)
		return 
		# update information about first message of this chat
		#if not history:
			#if self.first==True:
				#self.first=False
			#elif self.first==None:
				#self.first=True
		self.ui.textEdit.setUpdatesEnabled(False) # disable updates because of performance
		# move text cursor to the end of document
		cursor=QtGui.QTextCursor(self.ui.textEdit.document())
		cursor.beginEditBlock()
		cursor.movePosition(QtGui.QTextCursor.End)
		
		# if scrollbar is in the end, we have to scroll it to the end as well when we finish
		toEnd=False
		if self.ui.textEdit.verticalScrollBar().value()==self.ui.textEdit.verticalScrollBar().maximum():
			toEnd=True
		# replace emoticons by images
		for k,v in self.main.emoticonsWidget.smileys.iteritems():
			text=text.replace(" "+k,'&nbsp;<img src="'+v+'"/>')
			text=text.replace("&nbsp;"+k,'&nbsp;<img src="'+v+'"/>')
			text=text.replace(">"+k,'><img src="'+v+'"/>')
		# insert text to the self.ui.textEdit
		cursor.insertFragment(QtGui.QTextDocumentFragment.fromHtml(text))
		cursor.endEditBlock()
		if toEnd:
			# scroll to the end
			self.ui.textEdit.verticalScrollBar().setValue(self.ui.textEdit.verticalScrollBar().maximum())
		self.ui.textEdit.setUpdatesEnabled(True)

	def addEmoticon(self,action):
		"""
		Insert emoticon according to action.objectName() to the self.ui.line. Called when user choose one of emoticons.
		@type action: QAction
		@param action: emotion QAction
		"""
		if isinstance(action,unicode):
			data=action
		else:
			data=action.data()
			data=data.toString()
		if self.main.config['chatMode']=="normal":
			cur=self.ui.line.textCursor()
			cur.insertText(" "+data)
			self.ui.line.setTextCursor(cur)
		else:
			for k,v in self.smileys.iteritems():
				data=data.replace(k,' <img src="images/16x16/emotes/'+v+'" />')
			self.ui.line.insertHtml(data)
		self.ui.line.setFocus(QtCore.Qt.MouseFocusReason)
	
	def sendButtonClicked(self):
		pass
	
	def on_remove(self):
		pass

	def tabPressed(self):
		pass

