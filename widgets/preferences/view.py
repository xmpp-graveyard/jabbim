"""
Copyright (C) 2009 	Jan 'Hanzz' Kaluza (hanzz at njs.netlab.cz)
Copyright (C) 2009	Jiri 'Sef' Gabrys	(sef at njs.netlab.cz)

This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
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
import os, sys
from widgets import webkitthemes
from PyQt4 import QtCore
import weakref

class webkitObject(QtCore.QObject):
	def __init__(self,preferences):
		QtCore.QObject.__init__(self)

		self.preferences = weakref.ref(preferences)
		self.setObjectName("webkitObject")
		self.emoticons = None
		self.chatTheme = None
		self.groupchatTheme = None

	def setConfig(self,config):
		self.emoticons = unicode(config["emoticons"])
		self.chatTheme = unicode(config["chatTheme"])
		self.groupchatTheme = unicode(config["groupchatTheme"])

	@QtCore.pyqtSignature("QString, QString")
	def selectChanged(self, typ, value):
		print "select changed", typ, value
		if typ == "emoticons":
			self.emoticons = unicode(value)
			frames = self.preferences().ui.themePackage.page().mainFrame().childFrames()
			for frame in frames:
				if frame.frameName() == "emoticonsFrame":
					frame.setHtml(generateEmoticonsPreview(self.preferences().main,unicode(value)))
		elif typ == "chatTheme":
			self.chatTheme = unicode(value)
			frames = self.preferences().ui.themePackage.page().mainFrame().childFrames()
			for frame in frames:
				if frame.frameName() == "chatThemeFrame":
					frame.setHtml(generateChatThemePreview(self.preferences().main,unicode(value)))
		elif typ == "groupchatTheme":
			self.groupchatTheme = unicode(value)
			frames = self.preferences().ui.themePackage.page().mainFrame().childFrames()
			for frame in frames:
				if frame.frameName() == "groupchatThemeFrame":
					frame.setHtml(generateChatThemePreview(self.preferences().main,unicode(value)))

def populateEmoticonsList(MainWindow,em):
#<form name="form1" title="Inaccessible form Example">
    #<label>Go to best practice topic
    #<select name="select1" size="1" onchange="gotourl(this)">
      #<option value="../standards/">Standards</option>
      #<option value="../nav/">Navigation</option>
      #<option value="../text/">Text Descriptions</option>
      #<option value="../auto/">Automation</option>
      #<option value="../styling/">Styling</option>
    #</select>
    #</label>
  #</form> 
	ret = '<form name="emoticonsForm"><label>' + unicode(MainWindow.tr("Name: ")) + '<select name="emoticons" size="1" onchange="webkitObject.selectChanged(\'emoticons\',this.options[this.selectedIndex].value);">'
	# emoticons from Jabbim root directory
	packs=os.listdir("emoticons/")
	for pack in packs:
		if os.path.isdir('emoticons/'+pack):
			emoticons=os.listdir('emoticons/'+pack+"/")
			for emoticon in emoticons:
				if emoticon.endswith('.cfg'):
					emo=pack+"/"+emoticon
					#config=ConfigObj("emoticons/"+emo,encoding='UTF8')
					loaded,config=MainWindow.loadJabbimExtraConfig("emoticons/"+emo,'emoticons/default/smileys.cfg')
					if loaded:
						if emo == em:
							ret += '<option selected value="' + emo + '" >' + unicode(config['header']['name']) + "</option>"
						else:
							ret += '<option value="' + emo + '">' + unicode(config['header']['name']) + "</option>"
						#if emo==currentEmoticons:
							#item=self.ui.emoticonsList.insertItem(0,QtGui.QIcon('emoticons/'+os.path.dirname(emo)+"/"+unicode(config['header']['frontImage'])),unicode(config['header']['name']),QtCore.QVariant(emo))
						#else:
							#item=self.ui.emoticonsList.addItem(QtGui.QIcon('emoticons/'+os.path.dirname(emo)+"/"+unicode(config['header']['frontImage'])),unicode(config['header']['name']),QtCore.QVariant(emo))
	
	# emoticons from users home directory
	packs=os.listdir(MainWindow.realHomeDir+"/emoticons")
	for pack in packs:
		if os.path.isdir(MainWindow.realHomeDir+"/emoticons/"+pack):
			emoticons=os.listdir(MainWindow.realHomeDir+"/emoticons/"+pack+"/")
			for emoticon in emoticons:
				if emoticon.endswith('.cfg'):
					emo=pack+"/"+emoticon
					#config=ConfigObj(MainWindow.realHomeDir+"/emoticons/"+emo,encoding='UTF8')
					loaded,config=MainWindow.loadJabbimExtraConfig(MainWindow.realHomeDir+"/emoticons/"+emo,'emoticons/default/smileys.cfg')
					if loaded:
						if emo == em:
							ret += '<option selected value="' + emo + '" >' + unicode(config['header']['name']) + "</option>"
						else:
							ret += '<option value="' + emo + '">' + unicode(config['header']['name']) + "</option>"

	ret += "</select></label></form>"
	return ret

def generateEmoticonsPreview(MainWindow,pack):
	src=unicode(os.getcwd(), sys.getfilesystemencoding())+'/emoticons/'
	#config=ConfigObj("emoticons/"+path,encoding='UTF8')
	loaded,config=MainWindow.loadJabbimExtraConfig("emoticons/"+pack,'emoticons/default/smileys.cfg')
	if len(config)==0 or not loaded:
		#config=ConfigObj(MainWindow.mainWindow.realHomeDir+"/emoticons/"+path,encoding='UTF8')
		src=MainWindow.realHomeDir+'/emoticons/'
		loaded,config=MainWindow.loadJabbimExtraConfig(MainWindow.realHomeDir+"/emoticons/"+pack,'emoticons/default/smileys.cfg')
		if not loaded:
			return None
	html="<html><head></head><body>"
	values=[]
	for k,v in config['emoticons'].iteritems():
		#MainWindow.smileys[k.replace("<","&lt;").replace(">","&gt;")]=v
		if not v in values:
			html+='<img src="file://'+src+os.path.dirname(pack)+'/'+v+'" />'
			values.append(v)
	html += "</body></html>"
	return html

def generateChatThemePreview(MainWindow,pack):
	factory=webkitthemes.webkitThemeFactory(pack,pack,MainWindow.realHomeDir)
	html="""
<html xmlns="http://www.w3.org/1999/xhtml">
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<style type="text/css" media="screen,print"> @import url( "main.css" ); </style>
<style id="mainStyle" type="text/css" media="screen,print"> %s </style>
</head>
<body>
<div id="Chat">
<div id="myDiv"> </div>
	""" % factory.genChatStyleSheet()

	html+="""
</div>
<a name='bottom'></a>
</body>
</html>
	"""

	jabbim_icon = unicode(os.getcwd(), sys.getfilesystemencoding()) + "/images/32x32/apps/jabbim.png"
	html+=factory.genIncomingContent(unicode(MainWindow.tr("User")),unicode(MainWindow.tr("Message for me")),MainWindow.now(),jabbim_icon)
	html+=factory.genIncomingNextContent(unicode(MainWindow.tr("User")),unicode(MainWindow.tr("Second message for me")),MainWindow.now(),jabbim_icon)
	html+=factory.genChatStatus(unicode(MainWindow.tr("User is now away")),MainWindow.now())
	html+=factory.genOutgoingContent(unicode(MainWindow.tr("Me")),unicode(MainWindow.tr("Message for user")),MainWindow.now(),jabbim_icon)
	html+=factory.genOutgoingNextContent(unicode(MainWindow.tr("Me")),unicode(MainWindow.tr("Second message for user")),MainWindow.now(),jabbim_icon)
	
	return html, factory.cPath

def generateThemePackagePreview(MainWindow,config):
	ret = "<html><head></head><body>"

	emoticons = generateEmoticonsPreview(MainWindow,config["emoticons"])
	if emoticons:
		ret += "<h3>" + unicode(MainWindow.tr("Emoticons")) +"</h3>"
		ret += populateEmoticonsList(MainWindow,config["emoticons"])
		ret += '<iframe src="blank" width="100%" height="120" frameborder="0" name="emoticonsFrame"></iframe>'
	else:
		ret += "<h3>" + unicode(MainWindow.tr("Emoticons")) +"</h3>"
		ret += "<b>" + MainWindow.tr("Emoticons package %1 is not installed").arg(config["emoticons"]) + "</b><br/>"

	chatTheme, cPath = generateChatThemePreview(MainWindow,config["chatTheme"])
	if chatTheme:
		ret += "<h3>" + unicode(MainWindow.tr("Chat theme")) +"</h3>"
		ret += unicode(MainWindow.tr("Name: ")) + config["chatTheme"].split("/")[0] + "<br/>"
		ret += unicode(MainWindow.tr("Style: ")) + config["chatTheme"].split("/")[1] + "<br/><br/>"
		ret += '<iframe src="blank" width="100%" height="120" frameborder="0" name="chatThemeFrame"></iframe>'
	else:
		ret += "<h3>" + unicode(MainWindow.tr("Chat theme")) +"</h3>"
		ret += "<b>" + MainWindow.tr("Chat theme %1 is not installed").arg(config["chatTheme"]) + "</b><br/>"

	groupchatTheme, gPath = generateChatThemePreview(MainWindow,config["groupchatTheme"])
	if groupchatTheme:
		ret += "<h3>" + unicode(MainWindow.tr("Groupchat theme")) +"</h3>"
		ret += unicode(MainWindow.tr("Name: ")) + config["groupchatTheme"].split("/")[0] + "<br/>"
		ret += unicode(MainWindow.tr("Style: ")) + config["groupchatTheme"].split("/")[1] + "<br/><br/>"
		ret += '<iframe src="blank" width="100%" height="120" frameborder="0" name="groupchatThemeFrame"></iframe>'
	else:
		ret += "<h3>" + unicode(MainWindow.tr("Groupchat theme")) +"</h3>"
		ret += "<b>" + MainWindow.tr("Groupchat theme %1 is not installed").arg(config["groupchatTheme"]) + "</b><br/>"

	ret += "</body></html>"
	return ret, (chatTheme, cPath), (groupchatTheme, gPath), emoticons
	
	
	
	
	