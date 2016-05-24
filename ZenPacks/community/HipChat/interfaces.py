######################################################################
#
# Copyright 2012 Zenoss, Inc.  All Rights Reserved.
#
######################################################################

from zope.interface import Interface
try:
    from Products.Zuul.interfaces.actions import IActionContentInfo
except ImportError:
    from Products.Zuul import IInfo as IActionContentInfo
from Products.Zuul.interfaces import IFacade
from Products.Zuul.form import schema
from Products.Zuul.utils import ZuulMessageFactory as _t
import textwrap

class IHipChatActionContentInfo(IActionContentInfo):

    hipChatUrl = schema.TextLine(
        title=_t(u'HipChat URL'),
        order=90,
    )

    proxyUrl = schema.TextLine(
        title=_t(u'Proxy URL'),
        order=100,
    )

    proxyUsername = schema.TextLine(
        title=_t(u'Proxy username'),
        order=110,
    )

    proxyPassword = schema.Password(
        title=_t(u'Proxy password'),
        order=120,
    )

    message_body = schema.Text(
	title=_t(u'Message Body'),
	description = _t(u'The template for the HipChat message'),
	order=130,
	default     = textwrap.dedent(text = u'''
        Device: ${evt/device}
        Component: ${evt/component}
        Severity: ${evt/severity}
        Time: ${evt/lastTime}
        Message:
        ${evt/message}
        <a href="${urls/eventUrl}">Event Detail</a>
        <a href="${urls/ackUrl}">Acknowledge</a>
        <a href="${urls/closeUrl}">Close</a>
        <a href="${urls/eventsUrl}">Device Events</a>
        ''')
    )
