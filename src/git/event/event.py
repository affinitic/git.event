# -*- coding: utf-8 -*-
from zope.interface import implements

from git.event.parser import parse_commit_message
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
    def tickets(self):
        """
        One message per ticket, but tickets are grouped by commit reference
        commits_dict = {"affinitic6060": [commit1, commit2],
                        "arsia2021": [commit3]}
        tickets = [ticket1, ticket2]
        """
        commits_dict = {}
        for commit in self.request.commits:
            parsed = parse_commit_message(commit.message)
            # Do not push anything if nothing found in parsing
            if not parsed:
                continue

            key = parsed['trac']+parsed['ticket']

            # Initialize commit list
            if key not in commits_dict:
                commits_dict[key] = []

            commits_dict[key].append(commit)

        tickets = []
        for key in commits_dict:
            tickets.append(Ticket(request=self.request,
                                  commits=commits_dict[key]))
        return tickets


class Ticket(object):

    def __init__(self, request, commits):
        self.request = request
        self.commits = commits

    @property
    def _parsed(self):
        return parse_commit_message(self.commits[0].message)

    @property
    def id(self):
        return int(self._parsed["ticket"])

    @property
    def trac(self):
        return self._parsed["trac"]

    @property
    def comment(self):
        comments = []
        for commit in self.commits:
            comments.append("%s\n%s" % (commit.message, commit.url))

        return "\n\n".join(comments)

    @property
    def user(self):
        return self.request.author
