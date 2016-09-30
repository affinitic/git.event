# -*- coding: utf-8 -*-
from zope.interface import implements

from affinitic.git.hooks.utils import parse_commit_message
from .interfaces import IPullRequestEvent
from .interfaces import IPushEvent
from collections import OrderedDict
import ConfigParser


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
        commits_dict = {"affinitic_6060_refs": [commit1, commit2],
                        "arsia_2020_closes": [commit3]}
        tickets = [ticket1, ticket2]
        """
        commits_dict = OrderedDict()
        # sort array to have older commit first
        commits = self.request.commits

        for commit in commits:
            parseds = parse_commit_message(commit.message)
            # Do not push anything if nothing found in parsing
            if not parseds:
                continue

            for parsed in parseds:
                key = parsed['trac'] + '_' + parsed['ticket'] + '_' + parsed['command']

                # Initialize commit list
                if key not in commits_dict:
                    commits_dict[key] = []

                commits_dict[key].append(commit)
        tickets = []

        for key in commits_dict:
            tickets.append(Ticket(request=self.request,
                                  commits=commits_dict[key],
                                  key=key))
        return tickets


class Ticket(object):

    def __init__(self, request, commits, key):
        """
        key = 'affinitic_6060'
        """
        self.request = request
        self.commits = commits
        self.key = key

    @property
    def trac(self):
        return self.key.split('_')[0]

    @property
    def id(self):
        return int(self.key.split('_')[1])

    @property
    def command(self):
        return self.key.split('_')[2]

    @property
    def comment(self):
        comments = []
        for commit in self.commits:
            comments.append("%s\n%s" % (commit.message, commit.url))

        return "\n\n".join(comments)

    @property
    def user(self):
        return find_trac_user(self.request.author)

    @property
    def author_email(self):
        return self.request.author_email


def find_trac_user(author):
    """
    Return related trac user if found
    """
    config = ConfigParser.RawConfigParser()
    config.read('trac_hooks.cfg')
    nicknames = config.items('nicknames')

    for user, aliases in nicknames:
        for alias in aliases.split('\n'):
            if alias == author:
                return user

    return author
