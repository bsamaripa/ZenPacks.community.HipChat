# HipChat - Zenoss Integration
A HipChat integrationo show events from Zenoss.

To use:
* Install the ZenPack using  zenpack--install=PATH_TO_EGG
* In HipChat, create a new integration 
* In Zenoss, click Events then Triggers, and then Notifications
* Create a new Notification by clicking the +, give it a name like "PushToHipChat" and choose "HipChat" from the Action pulldown
* click Submit to save
* Open the new notification and click content.
* Paste the HipChat Url (i.e., https://api.hipchat.com/v2/room/<ID>/notification?auth_token=<TOKEN>) in to the hipChatUrl field
* click Submit to save
