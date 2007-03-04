from protocol import *

def getVcard(disp,jid,func,onlyAvatar):
	iq=Iq(to=jid,typ='get',xmlns=None)
	iq.addChild("vCard",{"xmlns":NS_VCARD})
	rep=disp.SendAndCallForResponse(iq,func,args={"jid":jid,"onlyAvatar":onlyAvatar})
	#if not isResultNode(rep) or rep.getVCardPayload()==None or len(rep.getVCardPayload())==0:
		#return {}
	#vcard={}
	#for i in rep.getVCardPayload():
		#if not isinstance(i,unicode):
			#vcard=parse(vcard,i)
	#return vcard
	
#def parse(vcard,i):
	#if len(i.getChildren())==0:
		#vcard[i.getName()]=unicode(i.getData())
	#else:
		#test={}
		#for x in i.getChildren():
			#vcard[i.getName()]=parse(test,x)
	#return vcard