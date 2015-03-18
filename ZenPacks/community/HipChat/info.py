from zope.interface import implements

try:
    from Products.Zuul.infos.actions import ActionContentInfo
except ImportError:
    from Products.Zuul.infos import InfoBase as ActionContentInfo

from Products.Zuul.infos.actions import ActionFieldProperty

from ZenPacks.community.HipChat.interfaces import IHipChatActionContentInfo


class HipChatActionContentInfo(ActionContentInfo):
    implements(IHipChatActionContentInfo)

    hipChatUrl = ActionFieldProperty(IHipChatActionContentInfo, 'hipChatUrl')
    proxyUrl = ActionFieldProperty(IHipChatActionContentInfo, 'proxyUrl')
    proxyUsername = ActionFieldProperty(IHipChatActionContentInfo, 'proxyUsername')
    proxyPassword = ActionFieldProperty(IHipChatActionContentInfo, 'proxyPassword')

