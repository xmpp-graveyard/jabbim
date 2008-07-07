"""
Copyright (C) 2007 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2007	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

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
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""
try:
	from PyQt4 import QtCore, QtGui, QtWebKit
except:
	print "PyQt4 is not installed."
import os
import weakref

class searchWidget(QtGui.QWidget):
	def __init__(self,webkit,parent=None):
		QtGui.QWidget.__init__(self,parent)
		self.webkit=weakref.ref(webkit)
		
		l=QtGui.QHBoxLayout(self)

		label=QtGui.QLabel(self.tr("Search:"))
		l.addWidget(label)

		self.searchText=QtGui.QLineEdit(self)
		l.addWidget(self.searchText)
		
		self.closeButton=QtGui.QPushButton(QtGui.QIcon("images/icons/close.png"),"",self)
		l.addWidget(self.closeButton)
		
		QtCore.QObject.connect(self.searchText, QtCore.SIGNAL("returnPressed () "),self.searchTextFinished)
		QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked () "),self.hideMe)

		short=QtGui.QShortcut("escape",self.searchText)
		QtCore.QObject.connect(short, QtCore.SIGNAL("activated ()"),self.hideMe)

		self.hide()

	def showMe(self):
		self.show()
		self.searchText.selectAll()
		self.searchText.setFocus(QtCore.Qt.MouseFocusReason)

	def hideMe(self):
		self.hide()

	def searchTextFinished(self):
		self.find(unicode(self.searchText.text()))

	def find(self,text,flags=QtWebKit.QWebPage.FindWrapsAroundDocument):
	    self.webkit().findText(text,flags)

class message(QtCore.QObject):
	def __init__(self,message):
		QtCore.QObject.__init__(self)
		self.message=[]
		self.messages=[]
		self.messageCache=[]
		self.ft={}
		self.scr=1
		self.setObjectName("messageObject")

	@QtCore.pyqtSignature("QString")
	def acceptFT(self,sid):
		self.ft[unicode(sid)].submitClicked()

	@QtCore.pyqtSignature("QString")
	def rejectFT(self,sid):
		self.ft[unicode(sid)].closeClicked()

	@QtCore.pyqtSignature("",result="int")
	def messageDirection(self):
		if len(self.messageCache)!=0:
			ret=self.messageCache[-1][0]
			return ret
		return -1

	@QtCore.pyqtSignature("",result="QString")
	def msg(self):
		if len(self.messageCache)!=0:
			ret=self.messageCache.pop()[1]
			#print "RET",[ret]
			return ret
		return ""
	
	@QtCore.pyqtSignature("int",result="QString")
	def msg_(self,i):
		return self.messages[i]
	
	@QtCore.pyqtSignature("",result="int")
	def scroll(self):
		return self.scr

	@QtCore.pyqtSignature("")
	def ready(self):
		#self.emit(QtCore.SIGNAL("ready()"))
		#print "READY!"
		#self.main.client.reactor.callLater(1,self.main.messageObjectReady)
		#self.main.messageObjectReady()
		pass

	@QtCore.pyqtSignature("QString")
	def log(self,test):
		#self.emit(QtCore.SIGNAL("ready()"))
		print test
		#pass

class webkitChatWidget(QtWebKit.QWebView):
	def __init__(self,chatwidget,parent=None):
		QtWebKit.QWebView.__init__(self,parent)
		self.chatwidget=weakref.ref(chatwidget)
		# webkit configuration
		self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled,True)
		self.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
		# messageObject
		self.messageObject=message("")
		# signals
		QtCore.QObject.connect(self.messageObject,QtCore.SIGNAL("ready()"),self.messageObjectReady)
		QtCore.QObject.connect(self,QtCore.SIGNAL("loadFinished ( bool)"),self.webkitLoaded_)
		QtCore.QObject.connect(self.page().mainFrame(),QtCore.SIGNAL("javaScriptWindowObjectCleared ()"),self.webkitCleared)
		QtCore.QObject.connect(self,QtCore.SIGNAL("linkClicked ( const QUrl &)"),QtGui.QDesktopServices.openUrl)
		self.palette().setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight,QtGui.QColor(self.palette().color(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight)))
		#self.palette().setColor(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText,self.palette().highlightedText().color())

		self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding))

	def contextMenuEvent(self,event):
		menu=QtGui.QMenu(self)
		hit=self.page().mainFrame().hitTestContent(event.pos())
		if len(hit.linkText())!=0:
			action=menu.addAction(self.tr("Open"))
			action.setObjectName("open")
			action.setData(QtCore.QVariant(hit.linkUrl()))
			menu.addAction(action)
			action=self.pageAction(QtWebKit.QWebPage.CopyLinkToClipboard)
			action.setText(self.tr("Copy link to clipboard"))
			menu.addAction(action)
		if len(self.selectedText())!=0:
			action=self.pageAction(QtWebKit.QWebPage.Copy)
			action.setText(self.tr("Copy text"))
			menu.addAction(action)
		menu.addSeparator()
		action=menu.addAction(self.tr("Search"))
		action.setObjectName("search")
		menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"),self.contextMenuTriggered)
		menu.popup(event.globalPos())

	def contextMenuTriggered(self,action):
		cmd=action.objectName()
		if cmd=="open":
			QtGui.QDesktopServices.openUrl(action.data().toUrl())
		elif cmd=="search":
		    self.chatwidget().ui.searchWidget.showMe()

	def messageObjectReady(self):
		#print "messageObjectReady",self.messageObject.messageCache
		if len(self.messageObject.messageCache)!=0:
			self.page().mainFrame().evaluateJavaScript("addNextMessage();")
		
	def webkitCleared(self):
		self.page().mainFrame().addToJavaScriptWindowObject("messageObject",self.messageObject)

	def webkitLoaded_(self):
		self.page().mainFrame().evaluateJavaScript("showLastMessages();")
		self.webkitLoaded=True
		self.messageObjectReady()
		try:
			typ=self.chatwidget().typ
		except:
			typ="chat"
		if typ=="groupchat":
			self.chatwidget().refreshStats()

	def loadWebkit(self):
		self.webkitLoaded=False
		try:
			typ=self.chatwidget().typ
		except:
			typ="chat"
		if typ=="groupchat":
			stylesheet=self.chatwidget().main().webkitThemeFactory.genGroupchatStyleSheet()
			footer=self.chatwidget().main().webkitThemeFactory.genGroupchatFooter()
			header=self.chatwidget().main().webkitThemeFactory.genGroupchatHeader()
		else:
			stylesheet=self.chatwidget().main().webkitThemeFactory.genChatStyleSheet()
			footer=self.chatwidget().main().webkitThemeFactory.genChatFooter()
			header=self.chatwidget().main().webkitThemeFactory.genChatHeader(self.chatwidget().name,self.chatwidget().file)
		code=""
		self.messageObject.messages=[]
		i=0
		previousName=""
		if typ=="groupchat":
			for m in self.chatwidget().lastMessages:
				out=m[0]=="out"
				if out:
					if m[1]==previousName:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genGroupchatOutgoingNextContent(m[1],m[2],m[3],m[4]))
						code+="insertMessage(%s);\n" % str(i)
					else:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genGroupchatOutgoingContent(m[1],m[2],m[3],m[4]))
						code+="addMessage(%s);\n" % str(i)
				else:
					if m[1]==previousName:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genGroupchatIncomingNextContent(m[1],m[2],m[3],m[4]))
						code+="insertMessage(%s);\n" % str(i)
					else:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genGroupchatIncomingContent(m[1],m[2],m[3],m[4]))
						code+="addMessage(%s);\n" % str(i)
				previousName=unicode(m[1])
				i+=1
		else:
			for m in self.chatwidget().lastMessages:
				out=m[0]=="out"
				if out:
					if m[1]==previousName:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genOutgoingNextContent(m[1],m[2],m[3],m[4]))
						code+="insertMessage(%s);\n" % str(i)
					else:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genOutgoingContent(m[1],m[2],m[3],m[4]))
						code+="addMessage(%s);\n" % str(i)
				else:
					if m[1]==previousName:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genIncomingNextContent(m[1],m[2],m[3],m[4]))
						code+="insertMessage(%s);\n" % str(i)
					else:
						self.messageObject.messages.append(self.chatwidget().main().webkitThemeFactory.genIncomingContent(m[1],m[2],m[3],m[4]))
						code+="addMessage(%s);\n" % str(i)
				previousName=unicode(m[1])
				i+=1
		html="""
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<style type="text/css" media="screen,print"> @import url( "main.css" ); </style>
<style id="mainStyle" type="text/css" media="screen,print"> %s </style>
<script>
function addNextMessage() {
var b = messageObject.messageDirection();
if (b==1) addMessage(-1);
if (b==0) insertMessage(-1);
b = messageObject.messageDirection();
if (b!=-1) addNextMessage();
}

function addMessage(index) {
shouldScroll = nearBottom();
//Remove any existing insertion point
insert = document.getElementById("insert");
if(insert) insert.parentNode.removeChild(insert);
messageObject.ready();
var ni = document.getElementById('myDiv');
var numi = document.getElementById('theValue');
var num = (document.getElementById('theValue').value -1)+ 2;
numi.value = num;
var divIdName = "my"+num+"Div";
var newdiv = document.createElement('div');
newdiv.setAttribute("id",divIdName);
if (index==-1) newdiv.innerHTML = messageObject.msg();
else newdiv.innerHTML = messageObject.msg_(index);
ni.appendChild(newdiv);
if (shouldScroll) setTimeout("scrollToBottom()", 100);

}
function insertMessage(index) {
shouldScroll = nearBottom();
messageObject.ready();
                        //Locate the insertion point
                        var insert = document.getElementById("insert");

                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        if (index==-1) {newNode = range.createContextualFragment(messageObject.msg());}
						else {newNode = range.createContextualFragment(messageObject.msg_(index));}

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);
if (shouldScroll) setTimeout("scrollToBottom()", 100);

}

function removeById(index) {

                        //Locate the insertion point
                        var insert = document.getElementById(index);
                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        newNode = range.createContextualFragment('');

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);

}

function showImage(imageId,link) {
shouldScroll = nearBottom();

                        //Locate the insertion point
                        var insert = document.getElementById(imageId);
                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        newNode = range.createContextualFragment('<div id="'+imageId+'"><a href="'+link+'" title="'+link+'">'+link+'</a> <a href="javascript:;" onclick="hideImage(\\''+imageId+'\\',\\''+link+'\\');")>[Hide Image]</a></div><div id="loaded'+imageId+'"><a href="'+link+'"><img src="'+link+'" /></a></div>');

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);
if (shouldScroll) setTimeout("scrollToBottom()", 100);

}

function reshowImage(imageId,link) {
shouldScroll = nearBottom();
document.getElementById('loaded'+imageId).style.display = 'inline';
                        //Locate the insertion point
                        var insert = document.getElementById(imageId);
                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        newNode = range.createContextualFragment('<div id="'+imageId+'"><a href="'+link+'" title="'+link+'">'+link+'</a> <a href="javascript:;" onclick="hideImage(\\''+imageId+'\\',\\''+link+'\\');")>[Hide Image]</a></div>');

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);
if (shouldScroll) setTimeout("scrollToBottom()", 100);

}

function hideImage(imageId,link){
   document.getElementById('loaded'+imageId).style.display = 'none';
                        //Locate the insertion point
                        var insert = document.getElementById(imageId);

                        //make new node
                        range = document.createRange();
                        range.selectNode(insert.parentNode);
                        newNode = range.createContextualFragment('<div id="'+imageId+'"><a href="'+link+'" title="'+link+'">'+link+'</a> <a href="javascript:;" onclick="reshowImage(\\''+imageId+'\\',\\''+link+'\\');")>[Show Image]</a></div>');

                        //swap
                        insert.parentNode.replaceChild(newNode,insert);
}

//Auto-scroll to bottom.  Use nearBottom to determine if a scrollToBottom is desired.
function nearBottom() {
		return ( (document.body.scrollTop+100) >= ( document.body.offsetHeight - ( window.innerHeight * 1.2 ) ) );
}
function scrollToBottom() {
		document.body.scrollTop = document.body.offsetHeight;
}

function showLastMessages(){
%s
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
		""" % (stylesheet,code,header,footer)

		self.chatwidget().imageId=0

		# debug... we don't need it anymore
		#f=open(self.chatwidget().main().webkitThemeFactory.chatPath()+"/test.html","w")
		#f.write(html)
		#f.close()
		if typ=="groupchat":
			self.page().mainFrame().setHtml(html,QtCore.QUrl("file:///"+self.chatwidget().main().webkitThemeFactory.groupchatPath()))
		else:
			self.page().mainFrame().setHtml(html,QtCore.QUrl("file:///"+self.chatwidget().main().webkitThemeFactory.chatPath()))
		
		
		