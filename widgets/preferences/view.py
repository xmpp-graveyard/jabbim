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

def generateEmoticonsPreview(MainWindow,pack):
	src=unicode(os.getcwd(), sys.getfilesystemencoding())+'/emoticons/'
	#config=ConfigObj("emoticons/"+path,encoding='UTF8')
	loaded,config=MainWindow.loadJabbimExtraConfig("emoticons/"+pack,'emoticons/default/smileys.cfg')
	if len(config)==0 or not loaded:
		src=MainWindow.realHomeDir+'/emoticons/'
		#config=ConfigObj(MainWindow.mainWindow.realHomeDir+"/emoticons/"+path,encoding='UTF8')
		loaded,config=MainWindow.loadJabbimExtraConfig(MainWindow.realHomeDir+"/emoticons/"+pack,'emoticons/default/smileys.cfg')
		if not loaded:
			return None
	html=""
	html+=MainWindow.tr("Name: ")+unicode(config['header']['name'])+"<br/>"
	if config['header'].has_key('license'):
		html+=MainWindow.tr("License: ")+unicode(config['header']['license'])+"<br/><br/>"
	values=[]
	for k,v in config['emoticons'].iteritems():
		#MainWindow.smileys[k.replace("<","&lt;").replace(">","&gt;")]=v
		if not v in values:
			html+='<img src="file://'+src+os.path.dirname(pack)+'/'+v+'" />'
			values.append(v)
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

	html = generateEmoticonsPreview(MainWindow,config["emoticons"])
	if html:
		ret += "<h3>" + unicode(MainWindow.tr("Emoticons")) +"</h3>"
		ret += html
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
	return ret, (chatTheme, cPath), (groupchatTheme, gPath)
	
	
	
	
	