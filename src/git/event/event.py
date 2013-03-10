# -*- coding: utf-8 -*-
from zope.interface import implements
from .interfaces import IPullRequestEvent
from .interfaces import IPushEvent


class GitEvent(object):

    def __init__(self, request):
        self.request = request


class PullRequestEvent(GitEvent):
    """
    A pull request
    """
    implements(IPullRequestEvent)


class PushEvent(GitEvent):
    """
    A push
    """
    implements(IPushEvent)
