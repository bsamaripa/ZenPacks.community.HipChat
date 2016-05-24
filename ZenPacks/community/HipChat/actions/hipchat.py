import logging
log = logging.getLogger("zen.useraction.actions")

from zope.interface import implements

from Products.ZenModel.interfaces import IAction, IProvidesEmailAddresses
from Products.ZenModel.actions import IActionBase, TargetableAction
from Products.ZenModel.actions import processTalSource, _signalToContextDict
from Products.ZenUtils.guid.guid import GUIDManager

from ZenPacks.community.HipChat.interfaces import IHipChatActionContentInfo
from ZenPacks.community.HipChat.lib.hipchat import sendHipChat

class HipChatAction(IActionBase, TargetableAction):
    implements(IAction)

    id='hipchat'
    name='HipChat'
    actionContentInfo=IHipChatActionContentInfo

    def __init__(self):
        super(HipChatAction, self).__init__()

    def setupAction(self, dmd):
        self.guidManager = GUIDManager(dmd)

    def execute(self, notification, signal):
        log.debug("Executing %s action", self.name)
        self.setupAction(notification.dmd)
	
        data = _signalToContextDict(
            signal,
            self.options.get('zopeurl'),
            notification,
            self.guidManager
        )
	log.info('Event context :: %s' %(data.as_string()))
	message_body = processTalSource(notification.content['message_body'], **data)
	sendHipChat(message_body,data['evt'].severity,notification.content['hipChatUrl'],notification.content['proxyUrl'],notification.content['proxyUsername'],notification.content['proxyPassword'])


    def getActionableTargets(self, target):
        """
        @param target: This is an object that implements
            the IProvidesEmailAddresses interface.
        @type target: UserSettings or GroupSettings.
        """
        if IProvidesEmailAddresses.providedBy(target):
            return target.getEmailAddresses()

    def _stripTags(self, data):
        """A quick html => plaintext converter
           that retains and displays anchor hrefs

           stolen from the old zenactions.
           @todo: needs to be updated for the new data structure?
        """
        tags = re.compile(r'<(.|\n)+?>', re.I | re.M)
        aattrs = re.compile(
            r'<a(.|\n)+?href=["\']([^"\']*)[^>]*?>([^<>]*?)</a>',
            re.I | re.M
        )
        anchors = re.finditer(aattrs, data)
        for x in anchors:
            data = data.replace(
                x.group(),
                "%s: %s" % (x.groups()[2], x.groups()[1])
            )
        data = re.sub(tags, '', data)
        return data

    def updateContent(self, content=None, data=None):
        updates = dict()
	
        updates['hipChatUrl'] = data.get('hipChatUrl', 'http://www.hipchat.com')

        properties = [
            'hipChatUrl',
            'proxyUrl',
            'proxyUsername',
            'proxyPassword',
	    'message_body',
        ]
	
        for k in properties:
            updates[k] = data.get(k)

        content.update(updates)

