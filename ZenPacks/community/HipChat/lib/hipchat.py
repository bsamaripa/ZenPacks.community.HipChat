# Updated from https://github.com/ssplatt/slack-zenoss
# adds arguments for event context and URL.
#
#!/usr/bin/env python
import json
import httplib2
import socks
from urlparse import urlparse

def sendHipChat(hipChatUrl='http://www.hipchat.com',proxyUrl=None,proxyUsername=None,proxyPassword=None,**data):
    evt=data['evt']
    device=evt.device
    component=evt.component
    severity=evt.severity
    message=evt.message
    summary=evt.summary
    cleared_by=evt.clearid

    detail_url = data['urls']['eventUrl']
    ack_url = data['urls']['ackUrl']
    close_url = data['urls']['closeUrl']
    dev_events_url = data['urls']['eventsUrl']
    reopen_url = data['urls']['reopenUrl']
    devUrl=data['urls']['deviceUrl'] 

    # setup the output
    # set the color based on severity
    if severity == 5:
        color = "red" #red
    elif severity == 4:
        color = "yellow" #yellow
    elif severity == 3:
        color = "yellow" #yellow
    elif severity == 2:
        color = "purple" #purple
    elif severity == 1:
        color = "gray" #gray
    elif severity == 0:
        color = "green" #green
    else:
        color = "green"
    
    if cleared_by is None:
	message="""<a href=%s>%s</a>: %s<br>
	<a href=%s>Event Details</a><BR>
	<a href=%s>Acknowledge</a><BR>
	<a href=%s>Close</a><BR>
	<a href=%s>View Device Events</a><BR>
	""" % (devUrl,device,summary,detail_url,ack_url,close_url,dev_events_url)
    else:
	color = 'green'
	message="""<a href=%s>%s</a>: %s<br>
	Cleared by: %s<br>
	<a href=%s>Reopen</a>""" %(devUrl,device,summary,cleared_by,reopen_url)
        

    # post to slack
    payload = json.dumps({
	"color":color,
	"message":message,
        "notify": 'false',
	'message_format': 'html' 
    })
   
    if proxyUrl:
	parsedUrl=urlparse(proxyUrl)
	proxyHost=parsedUrl.hostname
	proxyPort=parsedUrl.port
	h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, proxyHost, proxyPort)) 
    else:
    	h = httplib2.Http()
    h.disable_ssl_certificate_validation=True
    (resp, content) = h.request(hipChatUrl, "POST", body=payload, headers={'content-type':'application/json'} )
    
