from protocol import *

def getVcard(disp,jid):
	iq=Iq(to=jid,typ='get',xmlns=None)
	iq.addChild("vCard",{"xmlns":NS_VCARD})
	rep=disp.SendAndWaitForResponse(iq)
	vcard={}
	#print unicode(rep)
	for i in rep.getVCardPayload():
		vcard=parse(vcard,i)
	return vcard
	
def parse(vcard,i):
	if len(i.getChildren())==0:
		vcard[i.getName()]=unicode(i.getData())
	else:
		test={}
		for x in i.getChildren():
			vcard[i.getName()]=parse(test,x)
	return vcard