# Updated from https://github.com/ssplatt/slack-zenoss
# adds arguments for event context and URL.
#
#!/usr/bin/env python
import json
import httplib2
from ZenPacks.community.HipChat.lib import socks
from urlparse import urlparse

def sendHipChat(message_body,severity,hipChatUrl='http://www.hipchat.com',proxyUrl=None,proxyUsername=None,proxyPassword=None):

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
    
    # post to slack
    payload = json.dumps({
	"color":color,
	"message":message_body.replace('\n', '<br />\n'),
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
    
