# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from git.event.event import PushEvent


@subscriber(PushEvent)
def PushEventSubscriber(request):
    """
    Git subscriber on push
    """
    pass
