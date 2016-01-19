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

    @property
    def ticket_id(self):
        return 6364

    @property
    def comment(self):
        comments = []
        for commit in self.request.commits:
            comments.append("%s\n%s" % (commit.message, commit.url))

        return "\n\n".join(comments)

    @property
    def user(self):
        return self.request.author
